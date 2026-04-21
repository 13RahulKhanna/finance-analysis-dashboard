import Card from "./atoms/Card.jsx";

function MetricRow({ label, value }) {
  return (
    <div className="metric-row">
      <span className="metric-row__label">{label}</span>
      <span className="metric-row__value">{value ?? "—"}</span>
    </div>
  );
}

export default function MetricsSection({ metrics }) {
  const m = metrics ?? {};

  return (
    <Card title="Metrics">
      <div className="metric-grid">
        <MetricRow label="Trend" value={m.trend} />
        <MetricRow label="Avg price" value={m.avg_price != null ? Number(m.avg_price).toLocaleString() : null} />
        <MetricRow
          label="Volatility"
          value={m.volatility != null ? Number(m.volatility).toFixed(6) : null}
        />
        <MetricRow label="Buy signals" value={m.buy_signals} />
        <MetricRow label="Sell signals" value={m.sell_signals} />
      </div>
    </Card>
  );
}
