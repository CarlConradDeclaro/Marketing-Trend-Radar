import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { TrendInsight } from "@/types/trend";

type AttentionChartProps = {
  trends: TrendInsight[];
};

export function AttentionChart({ trends }: AttentionChartProps) {
  if (!trends.length) {
    return (
      <div className="flex h-72 items-center justify-center rounded-3xl border border-white/10 bg-white/5 text-sm text-slate-400">
        No trend data to chart yet.
      </div>
    );
  }

  const data = trends.map((trend) => ({
    topic: trend.topic,
    score: trend.attention_score,
  }));

  return (
    <div className="h-72 rounded-3xl border border-white/10 bg-white/5 p-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 12, left: 0, bottom: 24 }}>
          <CartesianGrid stroke="rgba(148, 163, 184, 0.16)" vertical={false} />
          <XAxis dataKey="topic" tick={{ fill: "#cbd5e1", fontSize: 12 }} angle={-15} textAnchor="end" interval={0} />
          <YAxis tick={{ fill: "#cbd5e1", fontSize: 12 }} domain={[0, 100]} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0b1629",
              border: "1px solid rgba(255,255,255,0.12)",
              borderRadius: 16,
              color: "#f8fafc",
            }}
          />
          <Bar dataKey="score" fill="#22d3ee" radius={[12, 12, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

