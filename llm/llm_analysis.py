import json
import logging
import os
import re
import time
from typing import Any, Dict, Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field, field_validator

load_dotenv()

logger = logging.getLogger(__name__)

INTERPRETATION_KEYS = (
    "avg_price",
    "volatility",
    "trend",
    "buy_signals",
    "sell_signals",
)

SYSTEM_PROMPT = """You are a trading analytics assistant. You ONLY interpret pre-computed metrics.
You must not invent numbers; base explanations strictly on the JSON input.
Respond with a single JSON object and nothing else (no markdown, no prose outside JSON).
Required keys: summary, trend_explanation, risk_level, strategy, confidence.
risk_level must be exactly one of: low, medium, high.
confidence MUST be exactly one of: low, medium, high (qualitative certainty). Never use a number, fraction, or percentage for confidence."""

USER_PROMPT = """Pipeline metrics (JSON):
{metrics_json}
{retry_note}"""


class InterpretationResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    summary: str = Field(..., min_length=1)
    trend_explanation: str = Field(..., min_length=1)
    risk_level: Literal["low", "medium", "high"]
    strategy: str = Field(..., min_length=1)
    confidence: Literal["low", "medium", "high"]

    @field_validator("risk_level", mode="before")
    @classmethod
    def normalize_risk(cls, v: Any) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
            if v in ("low", "medium", "high"):
                return v
        raise ValueError("risk_level must be low, medium, or high")

    @field_validator("confidence", mode="before")
    @classmethod
    def normalize_confidence(cls, v: Any) -> str:
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("low", "medium", "high"):
                return s
        raise ValueError("confidence must be low, medium, or high")


def _metrics_for_prompt(metrics: dict) -> dict:
    out = {}
    for k in INTERPRETATION_KEYS:
        if k not in metrics:
            raise KeyError(f"Missing metric field required for LLM input: {k}")
        out[k] = metrics[k]
    return out


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text


def _confidence_numeric_to_band(value: float) -> str:
    if value < 0.4:
        return "low"
    if value < 0.7:
        return "medium"
    return "high"


def _coerce_confidence_field(data: dict) -> dict:
    """Map numeric confidence to low/medium/high before Pydantic (LLMs often return 0.0–1.0)."""
    out = dict(data)
    conf = out.get("confidence")
    if type(conf) in (int, float):
        out["confidence"] = _confidence_numeric_to_band(float(conf))
        return out
    if isinstance(conf, str):
        stripped = conf.strip()
        try:
            numeric = float(stripped)
        except ValueError:
            return out
        out["confidence"] = _confidence_numeric_to_band(numeric)
    return out


def _parse_llm_json(raw: str) -> dict:
    if raw is None:
        raise ValueError("Empty LLM response")
    text = str(raw).strip()
    if not text:
        raise ValueError("Empty LLM response")
    text = _strip_code_fences(text)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e
    if not isinstance(obj, dict):
        raise ValueError("JSON root must be an object")
    return obj


def _validate_interpretation(data: dict) -> dict:
    fixed = _coerce_confidence_field(data)
    model = InterpretationResult.model_validate(fixed)
    return model.model_dump()


def _interpretation_chain(llm: ChatOpenAI):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT),
        ]
    )
    return prompt | llm | StrOutputParser()


def _run_chain_with_retry(chain, metrics_json: str) -> dict:
    retry_note = ""
    last_error = None
    for attempt in range(2):
        raw = chain.invoke({"metrics_json": metrics_json, "retry_note": retry_note})
        logger.info("LLM raw response (truncated): %s", raw[:500] if raw else "")
        try:
            parsed = _parse_llm_json(raw)
            return _validate_interpretation(parsed)
        except Exception as e:
            last_error = e
            logger.warning("LLM JSON parse/validate failed (attempt %s): %s", attempt + 1, e)
            retry_note = (
                "\nYour previous reply was not valid JSON or failed schema validation. "
                "Reply with ONLY one JSON object using keys: "
                "summary, trend_explanation, risk_level, strategy, confidence. "
                "risk_level and confidence must each be exactly one of: low, medium, high "
                "(strings only, never numeric confidence)."
            )
    raise ValueError(f"LLM did not return valid JSON after retry: {last_error}")


def _timed_interpretation(label: str, chain, metrics_json: str) -> tuple[dict, float]:
    t0 = time.perf_counter()
    try:
        result = _run_chain_with_retry(chain, metrics_json)
    finally:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        logger.info("%s interpretation completed in %.2f ms", label, elapsed_ms)
    return result, elapsed_ms


def _missing_key_response(provider: str, detail: str) -> dict:
    return {
        "summary": f"{provider} analysis unavailable.",
        "trend_explanation": detail,
        "risk_level": "medium",
        "strategy": "N/A",
        "confidence": "low",
    }


def analyze_metrics(metrics: dict) -> dict:
    """
    Run LangChain interpretation on computed metrics only (no OHLCV refetch).

    Returns groq and openrouter structured dicts plus optional timing for logs/comparison.
    """
    try:
        payload = _metrics_for_prompt(metrics)
    except KeyError as e:
        err = {"error": str(e)}
        return {
            "groq_analysis": err,
            "openrouter_analysis": err,
        }

    metrics_json = json.dumps(payload, indent=2)

    load_dotenv()
    groq_key = (os.getenv("GROQ_API_KEY") or "").strip()
    or_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()

    timing: Dict[str, Any] = {"groq": None, "openrouter": None}
    out: Dict[str, Any] = {}

    if not groq_key:
        out["groq_analysis"] = _missing_key_response("Groq", "Set GROQ_API_KEY to enable.")
    else:
        groq_llm = ChatOpenAI(
            model="llama-3.1-8b-instant",
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=0.2,
        )
        try:
            groq_result, groq_ms = _timed_interpretation(
                "Groq", _interpretation_chain(groq_llm), metrics_json
            )
            out["groq_analysis"] = groq_result
            timing["groq"] = round(groq_ms, 2)
        except Exception as e:
            logger.exception("Groq interpretation failed")
            out["groq_analysis"] = _missing_key_response("Groq", str(e))

    if not or_key:
        out["openrouter_analysis"] = _missing_key_response(
            "OpenRouter", "Set OPENROUTER_API_KEY to enable."
        )
    else:
        or_llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            api_key=or_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.2,
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "mlops-llm-project",
            },
        )
        try:
            or_result, or_ms = _timed_interpretation(
                "OpenRouter", _interpretation_chain(or_llm), metrics_json
            )
            out["openrouter_analysis"] = or_result
            timing["openrouter"] = round(or_ms, 2)
        except Exception as e:
            logger.exception("OpenRouter interpretation failed")
            out["openrouter_analysis"] = _missing_key_response("OpenRouter", str(e))

    if timing["groq"] is not None and timing["openrouter"] is not None:
        faster = (
            "Groq"
            if timing["groq"] < timing["openrouter"]
            else "OpenRouter"
            if timing["openrouter"] < timing["groq"]
            else "tie"
        )
        logger.info(
            "LLM timing comparison: Groq=%sms OpenRouter=%sms (faster: %s)",
            timing["groq"],
            timing["openrouter"],
            faster,
        )

    return out
