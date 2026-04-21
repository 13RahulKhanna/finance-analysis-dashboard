import argparse
import json
import logging
import math
import sys
import time

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm.llm_analysis import analyze_metrics
from pipeline.data_processing import load_config, load_data
from pipeline.signals import build_metrics, compute_signals

load_dotenv()


def _build_chart_data(df: pd.DataFrame, signal: pd.Series, max_points: int = 400) -> list:
    """Downsampled close price + binary signal for the UI chart (keeps payload small)."""
    n = len(df)
    if n == 0:
        return []
    step = max(1, (n + max_points - 1) // max_points)
    close = df["close"].astype(float)
    sig = signal.astype(int)
    rows = []
    for i in range(0, n, step):
        price = float(close.iloc[i])
        if math.isnan(price) or math.isinf(price):
            continue
        s = sig.iloc[i]
        try:
            sig_val = int(s) if pd.notna(s) else 0
        except (TypeError, ValueError):
            sig_val = 0
        rows.append(
            {
                "index": i + 1,
                "price": price,
                "signal": sig_val,
            }
        )
    return rows


def run_pipeline_job(
    input_path: str = "data.csv",
    config_path: str = "pipeline/config.yaml",
    output_path: str = "metrics.json",
    log_file: str = "run.log",
    *,
    persist_to_disk: bool = True,
) -> dict:
    """
    Execute the full batch pipeline and LLM interpretation.
    Returns the same dict written to metrics.json in CLI mode.
    """
    start_time = time.time()

    if not logging.getLogger().handlers:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )
    logging.getLogger("llm.llm_analysis").setLevel(logging.INFO)

    logging.info("Job started")

    try:
        config = load_config(config_path)
        logging.info("Config loaded: %s", config)

        np.random.seed(config["seed"])

        df = load_data(input_path)
        logging.info("Rows loaded: %s", len(df))

        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        _, signal = compute_signals(df, config["window"])
        latency_ms = int((time.time() - start_time) * 1000)
        metrics = build_metrics(df, signal, config, latency_ms)

        llm_results = analyze_metrics(metrics)
        chart_data = _build_chart_data(df, signal)
        final_output = {
            "metrics": metrics,
            "groq_analysis": llm_results["groq_analysis"],
            "openrouter_analysis": llm_results["openrouter_analysis"],
            "chart_data": chart_data,
        }

        if persist_to_disk:
            with open(output_path, "w") as f:
                json.dump(final_output, f, indent=2)

        logging.info("Metrics: %s", metrics)
        logging.info("LLM layers attached; job finished successfully")

        return final_output

    except Exception as e:
        logging.error(str(e))

        error_metrics = {
            "version": config["version"] if "config" in locals() else "unknown",
            "status": "error",
            "error_message": str(e),
        }
        final_output = {
            "metrics": error_metrics,
            "groq_analysis": {"error": "pipeline failed before LLM"},
            "openrouter_analysis": {"error": "pipeline failed before LLM"},
            "chart_data": [],
        }

        if persist_to_disk:
            with open(output_path, "w") as f:
                json.dump(final_output, f, indent=2)

        return final_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data.csv")
    parser.add_argument("--config", default="pipeline/config.yaml")
    parser.add_argument("--output", default="metrics.json")
    parser.add_argument("--log-file", default="run.log")
    args = parser.parse_args()

    final_output = run_pipeline_job(
        args.input,
        args.config,
        args.output,
        args.log_file,
        persist_to_disk=True,
    )
    print(json.dumps(final_output, indent=2))

    if final_output.get("metrics", {}).get("status") == "error":
        sys.exit(1)


app = FastAPI(title="Finance AI Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/run")
def run_pipeline_endpoint():
    """Runs the same pipeline as the CLI; returns JSON without requiring query params (defaults)."""
    return run_pipeline_job(persist_to_disk=False)


if __name__ == "__main__":
    main()
