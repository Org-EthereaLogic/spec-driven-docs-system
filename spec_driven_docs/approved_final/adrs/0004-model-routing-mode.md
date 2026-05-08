# ADR-0004: Single-Model-Mode Acceptable for MVP; Hybrid Routing Optional

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Technical lead, product sponsor

## Context

PRD FR-022 describes a routing layer that selects between a local model and an approved external model based on complexity, cost, privacy, and quality. The capability is genuinely useful at scale, but the canonical MVP demo scope is one target company plus one prospect (preferred: one company plus two prospects from the same company). At that scope the optimization story for hybrid routing - cost amortization, latency parity, privacy-tier separation - has no measurable payoff. The risks of building it early are real: two model paths mean two sets of credentials, two failure modes, parity testing across models, and fallback logic that has to be exercised before it can be trusted.

The Project Plan (§3 SDLC, §1.1 plan baseline approval) flags model mode as a Phase 0 decision specifically because committing to hybrid would expand Phase 1 build scope and could push out demo readiness. Stakeholders have not asked for hybrid routing as a precondition for the demo. They have asked for the workflow itself to be reliable and auditable.

The independent goal that does need to be settled now is logging. Whatever model runs, the workflow run log must capture model identity, routing reason, and any fallback so that reviewers and auditors can attribute every step's output to a specific model invocation.

## Decision

A single approved model is sufficient for MVP success. The runner records `single_model_mode: true`, the configured model name, and the reason hybrid routing was not used (for example, "MVP scope: hybrid not required") on every workflow run that uses single-model mode.

If hybrid routing is later configured, every LLM call logs the selected model and the routing reason - the same fields, populated differently. If the local model is unavailable, the runner falls back to the configured default approved model and logs the fallback reason. The shape of the log is the same in either mode; only the values differ.

Hybrid routing remains MVP-optional and does not gate Phase 2 demo readiness. A future decision can revisit this without changing the schema or the runner contract; it changes only the configuration.

## Consequences

### Positive

- Lower operational complexity during Phase 1 build: one credential set, one failure mode to harden.
- Faster path to Phase 2 demo readiness; model selection is not on the critical path.
- Logging contract is identical across modes, so a later switch to hybrid is a configuration change rather than a re-architecture.
- Reviewers and auditors see consistent provenance regardless of routing mode.

### Negative

- Cost and latency optimization opportunities are deferred. Steady-state operation may surface them.
- Teams that need hybrid for privacy-tier reasons - keeping certain prospect data on a local model - must request hybrid as an explicit override or wait until post-MVP.

### Neutral

- Shapes the `produced_by_model` provenance field defined in ADR-0002 and recorded on every step output.
- Ties directly into the workflow run log specified in ADR-0003; routing decisions live there.

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| Require hybrid routing for MVP | Adds operational surface area without delivering an MVP-scope benefit. Risks pushing out Phase 2 demo readiness. |
| Defer all model decisions until Phase 1 build starts | Logging requirements must be settled before the runner is implemented. Deferring leaves the runner contract incomplete. |
