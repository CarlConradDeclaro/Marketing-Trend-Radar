import type { TrendInsight } from "@/types/trend";

type TrendCardProps = {
  trend: TrendInsight;
};

export function TrendCard({ trend }: TrendCardProps) {
  return (
    <article className="rounded-3xl border border-white/10 bg-slate-900/80 p-5 shadow-glow">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-cyan-300">Trend</p>
          <h3 className="mt-2 text-xl font-semibold text-white">{trend.topic}</h3>
        </div>
        <div className="rounded-2xl bg-cyan-400/10 px-3 py-2 text-right">
          <p className="text-xs text-cyan-200">Attention</p>
          <p className="text-2xl font-bold text-cyan-300">{trend.attention_score}</p>
        </div>
      </div>

      <p className="mt-4 text-sm leading-6 text-slate-300">{trend.why_it_is_trending}</p>

      <dl className="mt-5 grid gap-3 text-sm text-slate-300 sm:grid-cols-2">
        <div>
          <dt className="text-slate-500">Audience</dt>
          <dd className="mt-1 text-slate-100">{trend.target_audience}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Risk</dt>
          <dd className="mt-1 text-slate-100">{trend.risk_level}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Confidence</dt>
          <dd className="mt-1 text-slate-100">{trend.confidence}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Action</dt>
          <dd className="mt-1 text-slate-100">{trend.recommended_action}</dd>
        </div>
      </dl>

      <div className="mt-5 space-y-4">
        <section>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Content ideas</p>
          <ul className="mt-2 flex flex-wrap gap-2">
            {trend.content_ideas.map((item) => (
              <li key={item} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm text-slate-200">
                {item}
              </li>
            ))}
          </ul>
        </section>
        <section>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Campaign angles</p>
          <ul className="mt-2 flex flex-wrap gap-2">
            {trend.campaign_angles.map((item) => (
              <li key={item} className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-sm text-emerald-100">
                {item}
              </li>
            ))}
          </ul>
        </section>
        <section>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Channels</p>
          <ul className="mt-2 flex flex-wrap gap-2">
            {trend.best_channels.map((item) => (
              <li key={item} className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-100">
                {item}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </article>
  );
}
