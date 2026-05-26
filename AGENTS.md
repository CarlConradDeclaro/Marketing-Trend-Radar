# Agent Workflow

## Project Overview

This project focuses on finding, ranking, and packaging topics or strategies that are getting strong attention online right now.

The system should help users:

- discover emerging themes from current sources
- compare topics by momentum, engagement, and relevance
- summarize why something is gaining attention
- surface practical strategies with source-backed evidence
- keep results current, traceable, and easy to review

## Agent Roles

- Marcus: product triage, request classification, query framing, guardrails, scoring, and risk identification.
- Elena: repository inspection, source scoping, architecture mapping, and exclusive file ownership planning.
- Rafa: backend, source connectors, data ingestion, schemas, services, persistence, AI orchestration, and integration work.
- Mia: frontend, search and filter UI, topic cards, strategy panels, review workflows, and status views.
- Nico: tests, QA gates, source validation, duplicate detection, freshness checks, and edge cases.
- Lena: documentation, README updates, methodology notes, and final insight summaries.

## File Ownership Rules

- Assign one owner per file before editing.
- Avoid overlapping edits between specialist agents.
- Shared contracts, such as source schemas and insight payloads, require one implementation owner and explicit reviewers.
- Do not delete existing project files unless the user explicitly requests removal.
- Do not overwrite app logic when adding workflow or documentation infrastructure.
- Prefer small, reversible changes that match the existing backend and frontend structure.

## Progress Update Format

When reporting progress during work, always name the active role at the start of the update. Do not switch to generic status-only updates once implementation has started.

Required rule:

For every progress update you write, always prefix the active role name:
Marcus, Elena, Rafa, Mia, Nico, or Lena.

Before each tool action, state the active role and what that role is doing.
After each important tool result, restate the active role and summarize the result.
Do not use anonymous commentary updates.

Use this format:

- `Marcus:` for triage, risk framing, and task classification
- `Elena:` for scope, file ownership, and implementation order
- `Rafa:` for backend, API, schema, and integration work
- `Mia:` for frontend, UI, component, and workflow interaction work
- `Nico:` for lint, typecheck, tests, validation, and QA findings
- `Lena:` for documentation, summaries, and final overview work

Preferred examples:

- `Marcus: this request is a trend-discovery feature, not a backend-only patch.`
- `Elena: minimum files are the topic ranking service and the discovery screen.`
- `Mia: the result cards now emphasize recency, source count, and momentum.`
- `Nico: validation passed, but one freshness edge case still needs coverage.`

Avoid anonymous updates such as `Working`, `Checking`, or `The state sync is now...` without an owning role prefix.

## Quality Chain

Before an implementation is considered complete, run or define the closest available checks:

- lint
- typecheck
- unit tests
- build
- schema validation
- duplicate topic detection
- empty query handling
- source freshness validation
- human approval gate validation

For frontend work, use available `npm` scripts such as `npm run lint`, `npm run typecheck`, `npm run test`, and `npm run build`.

For Python backend work, use available checks such as `pytest`, `ruff`, `flake8`, and Pydantic schema validation.

## Implementation Workflow

1. User request enters the AI Agents Team.
2. Marcus performs triage and identifies risks.
3. Elena scopes files, source coverage, and implementation order.
4. Specialist agents work on exclusive files.
5. Nico runs the quality chain.
6. Human reviews and approves generated insights or implementation output.
7. Ship work prepares approved content or code for delivery.
8. Lena writes the final overview and documentation summary.

## Recommendation Workflow

When the user asks what the project should improve, fix, or build next, use [recommendations.md](docs/agents/recommendations.md) together with the repository guidance files as the source of truth:

- `README.md`
- `AGENTS.md`
- `docs/agents/architecture.md`
- `docs/agents/workflow.md`
- `docs/agents/quality-gates.md`

That review should return prioritized recommendations for:

- missing v0.1 product capabilities
- topic discovery and ranking improvements
- backend or source-ingestion gaps
- quality, validation, and freshness gaps
- future integration or export improvements
- documentation and onboarding gaps

It should also:

- read the current project docs first
- identify must-have v0.1 gaps
- distinguish quick wins from later-phase roadmap work
- preserve the human approval gate and source-traceability strategy

## Approval Rule

No generated insight pack, export, or downstream integration should be published without explicit human approval.
