import { useState } from "react";
import { fetchRunAnalysis } from "./api.js";
import Button from "./components/atoms/Button.jsx";
import SummarySection from "./components/SummarySection.jsx";
import MetricsSection from "./components/MetricsSection.jsx";
import ChartSection from "./components/ChartSection.jsx";
import AnalysisCard from "./components/AnalysisCard.jsx";
import ComparisonSection from "./components/ComparisonSection.jsx";
import AnimatedBackground from "./components/background/AnimatedBackground.jsx";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);

  async function runAnalysis() {
    setLoading(true);
    setErr(null);
    setData(null);
    try {
      const payload = await fetchRunAnalysis();
      if (payload == null || typeof payload !== "object") {
        setErr("Unexpected response from server. Try again or check API logs.");
        return;
      }
      setData(payload);
    } catch (e) {
      const detail = e?.response?.data?.detail;
      const msg =
        (Array.isArray(detail) ? detail.map((d) => d.msg).join(" ") : detail) ??
        e?.message ??
        "Request failed. Is the API running (uvicorn main:app --reload)?";
      setErr(String(msg));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <AnimatedBackground />
      <div className="dashboard">
      <header className="dashboard__header">
        <h1>Finance AI Analyzer</h1>
        <Button onClick={runAnalysis} disabled={loading}>
          {loading ? "Running analysis…" : "Run Analysis"}
        </Button>
      </header>

      {loading && (
        <p className="state-banner state-banner--loading" aria-live="polite">
          Loading pipeline and LLM layers…
        </p>
      )}

      {err && (
        <p className="state-banner state-banner--error" role="alert">
          {err}
        </p>
      )}

      {data && !loading && (
        <div className="dashboard__sections">
          <SummarySection summary={data.groq_analysis?.summary} />
          <MetricsSection metrics={data.metrics} />
          <ChartSection chartData={data.chart_data ?? data.chartData} />
          <AnalysisCard title="Groq Analysis" analysis={data.groq_analysis} />
          <AnalysisCard title="OpenRouter Analysis" analysis={data.openrouter_analysis} />
          <ComparisonSection
            groqAnalysis={data.groq_analysis}
            openrouterAnalysis={data.openrouter_analysis}
          />
        </div>
      )}
      </div>
    </div>
  );
}
