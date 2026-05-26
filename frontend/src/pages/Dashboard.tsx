"use client";

import { useState } from "react";

import { analyzeTrends } from "@/api/trendApi";
import { AttentionChart } from "@/components/AttentionChart";
import { SearchPanel } from "@/components/SearchPanel";
import { SourceList } from "@/components/SourceList";
import { TrendCard } from "@/components/TrendCard";
import type { AnalyzeTrendsResponse } from "@/types/trend";

const DEFAULT_QUERY = "AI marketing";

export default function Dashboard() {
  const [query, setQuery] = useState(DEFAULT_QUERY);
  const [data, setData] = useState<AnalyzeTrendsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch() {
    const trimmed = query.trim();
    if (!trimmed) {
      setError("Enter a marketing topic to analyze.");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await analyzeTrends({ query: trimmed, max_articles: 20 });
      setData(response);
    } catch (requestError) {
      setData(null);
      setError(requestError instanceof Error ? requestError.message : "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.18),_transparent_32%),linear-gradient(180deg,#020817_0%,#07111f_40%,#020817_100%)] text-slate-100">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-10 md:px-8 lg:px-10">
        <section className="rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-glow backdrop-blur">
          <div className="max-w-3xl">
            <p className="text-sm uppercase tracking-[0.4em] text-cyan-300">Marketing Trend Radar</p>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight text-white md:text-6xl">
              Discover what marketing topics are getting attention right now.
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300 md:text-lg">
              Pull current coverage from recent news sources, analyze it with an AI agent, and turn it into practical
              trend insights, recommended actions, and source-backed campaign ideas.
            </p>
          </div>
        </section>

        <SearchPanel value={query} onChange={setQuery} onSubmit={handleSearch} isLoading={isLoading} />

        {error ? (
          <div className="rounded-3xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-100">
            {error}
          </div>
        ) : null}

        {!data && !isLoading ? (
          <section className="rounded-3xl border border-dashed border-white/10 bg-white/5 p-8 text-slate-300">
            Run a search to see a live marketing trend brief.
          </section>
        ) : null}

        {isLoading ? (
          <section className="grid gap-4 md:grid-cols-2">
            <div className="h-56 animate-pulse rounded-3xl bg-white/5" />
            <div className="h-56 animate-pulse rounded-3xl bg-white/5" />
          </section>
        ) : null}

        {data ? (
          <>
            <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
              <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-glow">
                <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">Summary</p>
                <h2 className="mt-3 text-2xl font-semibold text-white">Trend summary</h2>
                <p className="mt-3 text-base leading-7 text-slate-300">{data.summary}</p>
                <div className="mt-6 rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-cyan-200">Overall recommendation</p>
                  <p className="mt-2 text-sm leading-6 text-cyan-50">{data.overall_recommendation}</p>
                </div>
              </div>
              <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-glow">
                <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">Attention score</p>
                <h2 className="mt-3 text-2xl font-semibold text-white">Trends by score</h2>
                <div className="mt-4">
                  <AttentionChart trends={data.top_trends} />
                </div>
              </div>
            </section>

            <section>
              <div className="mb-4 flex items-end justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">Trend cards</p>
                  <h2 className="mt-2 text-2xl font-semibold text-white">Top marketing topics</h2>
                </div>
                <p className="text-sm text-slate-400">{data.top_trends.length} topics analyzed</p>
              </div>
              {data.top_trends.length ? (
                <div className="grid gap-5 xl:grid-cols-2">
                  {data.top_trends.map((trend) => (
                    <TrendCard key={trend.topic} trend={trend} />
                  ))}
                </div>
              ) : (
                <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-slate-300">
                  No trend insights were generated for this query.
                </div>
              )}
            </section>

            <section>
              <div className="mb-4">
                <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">Sources</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Source articles</h2>
              </div>
              <SourceList sources={data.sources} />
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
