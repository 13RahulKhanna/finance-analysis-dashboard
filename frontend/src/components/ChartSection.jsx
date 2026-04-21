import { useLayoutEffect, useRef, useState } from "react";
import { Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";
import Card from "./atoms/Card.jsx";

const CHART_HEIGHT = 260;

const tooltipStyle = {
  backgroundColor: "#0f172a",
  border: "1px solid #334155",
  borderRadius: "8px",
  color: "#e2e8f0",
  fontSize: "12px",
};

function SignalDot(props) {
  const { cx, cy, payload } = props;
  if (cx == null || cy == null || !payload) return null;
  const fill =
    payload.signal === 1 ? "rgba(74, 222, 128, 0.75)" : "rgba(100, 116, 139, 0.55)";
  return <circle cx={cx} cy={cy} r={2} fill={fill} />;
}

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const row = payload[0]?.payload;
  const sigLabel = row?.signal === 1 ? "Above mean (buy bias)" : "At/below mean (sell bias)";
  return (
    <div style={tooltipStyle}>
      <div style={{ marginBottom: 4 }}>Bar #{label}</div>
      <div style={{ color: "#94a3b8" }}>Price: {Number(row?.price).toLocaleString()}</div>
      <div style={{ color: "#64748b", marginTop: 4, fontSize: "11px" }}>{sigLabel}</div>
    </div>
  );
}

function useChartWidth() {
  const ref = useRef(null);
  const [width, setWidth] = useState(() => {
    if (typeof window === "undefined") return 640;
    return Math.min(720, Math.max(280, Math.floor(window.innerWidth - 48)));
  });

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return undefined;

    const measure = () => {
      const w = el.getBoundingClientRect().width;
      const next = Math.floor(w > 0 ? w : Math.min(720, window.innerWidth - 48));
      setWidth(Math.max(280, next));
    };

    measure();
    const ro = new ResizeObserver(() => measure());
    ro.observe(el);
    window.addEventListener("resize", measure);
    return () => {
      ro.disconnect();
      window.removeEventListener("resize", measure);
    };
  }, []);

  return { ref, width };
}

export default function ChartSection({ chartData }) {
  const raw = Array.isArray(chartData) ? chartData : [];
  const rows = raw.filter(
    (d) =>
      d &&
      typeof d === "object" &&
      typeof d.price === "number" &&
      !Number.isNaN(d.price) &&
      Number.isFinite(d.price)
  );

  const { ref: wrapRef, width } = useChartWidth();

  if (rows.length === 0) {
    return (
      <Card title="Price Trend">
        <p className="text-muted">No chart data available. Restart the API if this persists.</p>
      </Card>
    );
  }

  return (
    <Card title="Price Trend">
      <div
        ref={wrapRef}
        className="chart-wrap"
        style={{ width: "100%", height: CHART_HEIGHT, minHeight: CHART_HEIGHT }}
      >
        <LineChart width={width} height={CHART_HEIGHT} data={rows} margin={{ top: 8, right: 12, left: 4, bottom: 4 }}>
          <XAxis
            dataKey="index"
            tick={{ fill: "#64748b", fontSize: 11 }}
            axisLine={{ stroke: "#334155" }}
            tickLine={{ stroke: "#334155" }}
            minTickGap={28}
          />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fill: "#64748b", fontSize: 11 }}
            axisLine={{ stroke: "#334155" }}
            tickLine={{ stroke: "#334155" }}
            tickFormatter={(v) =>
              v >= 1e6 ? `${(v / 1e6).toFixed(1)}M` : v >= 1e3 ? `${(v / 1e3).toFixed(0)}k` : String(v)
            }
            width={52}
          />
          <Tooltip content={<ChartTooltip />} cursor={{ stroke: "#94a3b8", strokeOpacity: 0.35 }} />
          <Line
            type="monotone"
            dataKey="price"
            name="Close"
            stroke="#94a3b8"
            strokeWidth={2}
            dot={(dotProps) => <SignalDot {...dotProps} />}
            activeDot={{ r: 4, fill: "#cbd5e1", stroke: "#475569" }}
            isAnimationActive={false}
          />
        </LineChart>
      </div>
      <p className="chart-legend text-muted">
        Dots: <span style={{ color: "rgba(74, 222, 128, 0.85)" }}>●</span> buy-bias signal{" "}
        <span style={{ color: "rgba(100, 116, 139, 0.85)" }}>●</span> sell-bias signal
      </p>
    </Card>
  );
}
