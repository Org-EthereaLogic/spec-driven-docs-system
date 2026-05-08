# ADR-0002: Structured JSON Outputs Per Workflow Step

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Technical lead, product sponsor

## Context

The AI-Powered Lead Generation MVP must demonstrate repeatable, auditable behavior across runs. Free-text LLM output resists that goal: the same prompt can produce slightly different shapes on each call, downstream parsers fail unpredictably, and validation rules cannot reliably extract the fields they need to gate the next step. Reviewers comparing two runs of the same prospect cannot tell whether differences reflect genuine model variation or formatting drift.

Every Guardrail in the workflow consumes the previous step's output - the broken-variable detector reads the message body, the wrong-person check reads the prospect reference, the unsupported-claim detector reads research claims and source refs. If those inputs are unstructured prose, each Guardrail must re-implement extraction, and behavior diverges as the prompts change. The Readiness scorer faces the same problem at the end of the pipeline. Stable, machine-checkable outputs are the precondition for any of these downstream consumers to work correctly.

The PRD also requires (FR-020, NFR-004) that completed packages trace data across campaign, company, prospect, dossier, message, cadence, Guardrail, and approval records. That cross-record traceability assumes a typed, named-field shape that a free-text response cannot guarantee.

## Decision

Every workflow step emits a JSON object that conforms to a documented schema. The schema is defined alongside the data objects in the Data Model design doc and is enforced before the next step starts: invalid JSON stops the workflow and surfaces an actionable error rather than passing degraded data forward.

Field naming is `snake_case`. Identifiers use the `_id` suffix (`campaign_id`, `prospect_id`, `dossier_id`). Cross-record references use the `_ref` suffix (`company_ref`, `dossier_ref`). Every step output includes provenance fields: `step_id`, `produced_at`, `workflow_run_id`, and - when an LLM was involved in producing the content - `produced_by_model`. Steps that wrap an LLM call validate the model's response against the schema before forwarding; non-conforming responses are treated as step failures, not soft warnings.

Downstream API documentation (the deferred Workflow Step JSON API Reference and the OpenAPI Specification) will derive from these same schemas once the delivery format decision (OQ-002) closes. Until then, the schemas live in `data-model.md` and in the runner's validation code, which remains the single source of truth.

## Consequences

### Positive

- Enables every Guardrail and the Readiness scorer to consume stable, named fields without re-implementing extraction.
- Makes runs comparable across time, supporting the demo, regression tests, and reviewer audits.
- Provides a clean derivation point for future API documentation, OpenAPI artifacts, and integration tooling.
- Aligns with the deterministic runner (ADR-0003): predictable inputs and outputs at every step boundary.

### Negative

- Writing schemas is upfront work. Every new step adds a schema and validation cost.
- Schema churn during Phase 1 build will require coordinated updates across step implementations and any tests that use them.
- LLMs occasionally produce nearly-correct JSON; the strict-validation rule means those outputs fail a step rather than passing degraded.

### Neutral

- Establishes the project's `snake_case`, `_id`, and `_ref` conventions for the rest of the codebase and documentation.
- Forces explicit decisions about which fields are required versus optional, surfacing data-model questions earlier than they would otherwise appear.

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| Free-text outputs with downstream parsing | Parsing fails unpredictably on prose drift. Cannot serve as a reliable gate for Guardrails or Readiness scoring. |
| Loosely-typed dictionaries without schemas | Every consumer would re-implement validation. Drift across consumers is a known anti-pattern that erodes the auditability goal. |
