import Card from "./atoms/Card.jsx";
import Badge from "./atoms/Badge.jsx";

export default function AnalysisCard({ title, analysis }) {
  const a = analysis ?? {};

  if (a.error && !a.summary) {
    return (
      <Card title={title}>
        <p className="text-muted">{String(a.error)}</p>
      </Card>
    );
  }

  return (
    <Card title={title}>
      <div className="analysis-block">
        <h3 className="analysis-block__heading">Trend explanation</h3>
        <p className="analysis-block__text">{a.trend_explanation ?? "—"}</p>
      </div>
      <div className="analysis-block">
        <h3 className="analysis-block__heading">Strategy</h3>
        <p className="analysis-block__text">{a.strategy ?? "—"}</p>
      </div>
      <div className="analysis-badges">
        <Badge label="Risk" value={a.risk_level} />
        <Badge label="Confidence" value={a.confidence} />
      </div>
    </Card>
  );
}
