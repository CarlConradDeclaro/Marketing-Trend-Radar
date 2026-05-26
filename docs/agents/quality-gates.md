# Trend Intelligence Quality Gates

## AI Output Quality Gates

- Generated insights must be grounded in current source evidence.
- Unsupported or unclear claims must go into `open_questions`.
- Acceptance criteria must be concrete and testable.
- Duplicate or near-duplicate topics must be detected before approval.
- Empty queries or empty source sets must be rejected with a clear error.
- Source freshness, relevance, and credibility must be validated.
- Final outputs must include traceable source references where applicable.
- Draft insights must be editable before approval.
- No output may be published unless its status is `approved`.

## Code Quality Gates

- Lint passes for changed frontend and backend files where tooling exists.
- Typecheck passes where the stack supports it.
- Unit tests pass for affected behavior.
- Build passes for production-facing changes.
- Pydantic schema validation passes for backend source and insight models.
- Validation confirms required fields before export or publish.
- Integration code never logs or exposes API keys or source credentials.

## Done Definition

Work is done when:

- The requested behavior is implemented or documented.
- Files changed are limited to the scoped ownership plan.
- AI output and publication guardrails are preserved.
- Quality checks have been run or clearly documented as unavailable.
- Remaining risks are documented.
- Human approval is required before any final publish step.
- Documentation is updated when behavior, architecture, or workflow changes.
