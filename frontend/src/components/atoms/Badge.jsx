const LEVELS = new Set(["low", "medium", "high"]);

function normalizeLevel(value) {
  if (typeof value !== "string") return null;
  const v = value.trim().toLowerCase();
  return LEVELS.has(v) ? v : null;
}

export default function Badge({ label, value }) {
  const level = normalizeLevel(value);
  const cls = level ? `badge badge--${level}` : "badge badge--neutral";
  const text = level ?? (value != null ? String(value) : "—");

  return (
    <span className={cls} title={label}>
      {label ? <span className="badge__label">{label}</span> : null}
      <span className="badge__value">{text}</span>
    </span>
  );
}
