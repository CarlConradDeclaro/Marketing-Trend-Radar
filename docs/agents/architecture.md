# Trend Intelligence Multi-Agent Architecture

## Text Diagram

```text
User Request
  |
  v
AI Agents Team
  |
  v
Marcus: Triage, risk scoring, guardrails
  |
  v
Elena: Scope files, source coverage, exclusive ownership
  |
  v
Specialist Agents
  |-- Rafa: Backend, source connectors, schemas, services, integrations
  |-- Mia: Frontend, query flow, result cards, approval panel
  |-- Nico: Tests, validation, quality gates
  |
  v
Quality Chain
  |-- lint
  |-- typecheck
  |-- tests
  |-- build
  |-- schema validation
  |-- duplicate detection
  |-- source freshness validation
  |-- human approval gate validation
  |
  v
Human Review and Approval
  |
  v
Ship Agent: approved implementation or approved publication
  |
  v
Lena: AI overview, documentation summary, architecture notes
```

## Role Explanation

Marcus is the intake and guardrail agent. Marcus classifies the request, checks missing requirements, scores risk, and protects the rule that generated output cannot be published without human approval.

Elena maps the work before edits begin. Elena identifies the minimum files to change, assigns exclusive ownership, and keeps implementation order clear.

Specialist agents perform focused implementation work. Rafa owns backend and integrations, Mia owns frontend and review UX, and Nico owns test coverage and validation.

Operational visibility matters as much as ownership. During progress reporting, the active role should be named explicitly so the user can tell whether the work is in triage, scoping, frontend, backend, QA, or documentation.

The quality chain runs before work is considered complete. It checks code quality, schema compatibility, duplicate handling, empty input behavior, source freshness, and human approval enforcement.

The Ship Agent prepares final delivery. For publication, it should only send outputs that have been explicitly approved and should preserve source references and summary metadata.

Lena closes the loop with documentation. Lena summarizes the feature, affected files, agent roles, quality checks, known limitations, and next recommended step.
