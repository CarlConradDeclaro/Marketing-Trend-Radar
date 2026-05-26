import type { Article } from "@/types/trend";

type SourceListProps = {
  sources: Article[];
};

export function SourceList({ sources }: SourceListProps) {
  if (!sources.length) {
    return (
      <div className="rounded-3xl border border-dashed border-white/10 bg-white/5 p-5 text-sm text-slate-400">
        No source articles returned for this query.
      </div>
    );
  }

  return (
    <div className="grid gap-3">
      {sources.map((source) => (
        <a
          key={`${source.url}-${source.title}`}
          href={source.url}
          target="_blank"
          rel="noreferrer"
          className="rounded-3xl border border-white/10 bg-slate-900/80 p-4 transition hover:border-cyan-400/40 hover:bg-slate-900"
        >
          <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <div>
              <h4 className="text-base font-semibold text-white">{source.title || "Untitled article"}</h4>
              <p className="text-sm text-slate-400">
                {source.domain || "Unknown source"} {source.published_at ? `- ${source.published_at}` : ""}
              </p>
            </div>
            <span className="text-xs uppercase tracking-[0.25em] text-cyan-300">Open source</span>
          </div>
          {source.snippet ? <p className="mt-3 text-sm leading-6 text-slate-300">{source.snippet}</p> : null}
        </a>
      ))}
    </div>
  );
}

