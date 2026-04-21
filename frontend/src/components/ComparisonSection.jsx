import Card from "./atoms/Card.jsx";

export default function ComparisonSection({ groqAnalysis, openrouterAnalysis }) {
  const g = groqAnalysis?.risk_level;
  const o = openrouterAnalysis?.risk_level;
  const same = g && o && g === o;
  const bothPresent = Boolean(g && o);

  return (
    <Card title="Comparison">
      {!bothPresent ? (
        <p className="text-muted">Risk levels unavailable for one or both models.</p>
      ) : same ? (
        <p className="comparison-ok">Groq and OpenRouter agree on risk: <strong>{g}</strong></p>
      ) : (
        <div className="comparison-warn" role="status">
          <p className="comparison-warn__title">Different risk interpretation</p>
          <p>
            Groq: <strong>{g}</strong>
            <span className="comparison-warn__sep">·</span>
            OpenRouter: <strong>{o}</strong>
          </p>
        </div>
      )}
    </Card>
  );
}
