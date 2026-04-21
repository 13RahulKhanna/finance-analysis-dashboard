import Card from "./atoms/Card.jsx";

export default function SummarySection({ summary }) {
  const text =
    typeof summary === "string"
      ? summary.trim()
      : summary != null && summary !== ""
        ? String(summary)
        : "";
  const hasContent = Boolean(text);

  return (
    <Card title="Summary">
      {hasContent ? (
        <p className="summary-lead">{text}</p>
      ) : (
        <p className="text-muted">No summary returned. Run analysis or check API keys.</p>
      )}
    </Card>
  );
}
