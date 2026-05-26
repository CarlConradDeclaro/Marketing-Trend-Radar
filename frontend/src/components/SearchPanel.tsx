"use client";

type SearchPanelProps = {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
};

export function SearchPanel({ value, onChange, onSubmit, isLoading }: SearchPanelProps) {
  return (
    <form
      className="flex flex-col gap-3 rounded-3xl border border-white/10 bg-white/5 p-4 shadow-glow backdrop-blur"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <label className="text-sm font-medium text-slate-200" htmlFor="query">
        Marketing topic
      </label>
      <div className="flex flex-col gap-3 md:flex-row">
        <input
          id="query"
          className="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-slate-100 outline-none ring-0 placeholder:text-slate-500 focus:border-cyan-400"
          placeholder="AI marketing, creator economy, B2B demand gen..."
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-2xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? "Analyzing..." : "Search trends"}
        </button>
      </div>
      <p className="text-sm text-slate-400">
        Enter a topic to pull recent coverage and generate marketing recommendations.
      </p>
    </form>
  );
}
