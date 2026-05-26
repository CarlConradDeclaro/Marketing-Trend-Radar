# Workflow

## Human Approval Gate

Generated insight packs are drafts until a human approves them. Draft, rejected, unreviewed, or AI-only output must not be published or exported as final guidance.

## Source Strategy

Current recommendations should be grounded in recent, traceable sources. Prefer a mix of high-signal sources, recency checks, and duplicate suppression so the final output reflects what is getting attention now rather than stale or repeated material.

## Recommendation Pass

When the team wants improvement ideas instead of immediate implementation, run a recommendation pass using [recommendations.md](recommendations.md). The recommendation pass should read the repo guidance files first, then return prioritized suggestions for v0.1 gaps, quick wins, source coverage, ranking logic, UX clarity, and later-phase roadmap ideas.

For ready-to-use prompts and role examples, see [prompt-template.md](prompt-template.md).

## Named Agent Updates

During implementation, progress updates should show which role is currently active. This is for visibility, not literal process isolation.

Use role-prefixed updates such as:

- `Marcus: this request is a trend-ranking feature with source validation risk.`
- `Elena: minimum files are the ranking service and the discovery screen.`
- `Mia: the result cards now surface source count, recency, and confidence.`
- `Nico: lint is running to verify the ranking and validation changes.`
- `Lena: the summary and affected-files notes are updated.`

If work moves from one area to another, switch the prefix to match the current owner instead of continuing with anonymous updates.
