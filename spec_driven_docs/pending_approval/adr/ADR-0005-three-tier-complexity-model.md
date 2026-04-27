# ADR-0005: Use a three-tier complexity model (Simple, Standard, Enterprise)

**Status:** Accepted
**Date:** 2026-04-26
**Deciders:** SDLC Pro architecture lead

## Context

Complexity drives cascading choices across the platform: which documents get generated, which Trinity routing mode is selected, which drift-sentinel modules are active, what the cost ceiling is, and what approval posture is enforced. A change in inferred complexity required a consistent change in every downstream system simultaneously.

A continuous complexity score was considered and rejected because every dependent system would have needed continuous parameter mappings, multiplying the configuration surface area across doc slates, routing mode selectors, policy fields, and cost ceilings. A discrete tier structure collapses that parameter space to a small number of named configurations; each tier becomes a fully specified bundle — one name resolves one routing mode, one doc slate, one cost ceiling, one test policy, and one approval posture.

Two tiers (Simple and Enterprise) were not sufficient because most real teams operate in the middle ground and would be systematically miscategorized. Four or more tiers added cardinality without adding distinct downstream configurations.

Three tiers map directly onto three real user personas from the PRD: a Solo Builder with minimal integrations (Simple), a Platform Engineer coordinating a small team (Standard), and a Compliance-Bound Architect under regulatory and SLO requirements (Enterprise). These personas also map exactly onto the three Trinity routing modes, making the tier cardinality load-bearing across multiple subsystems.

Sources: PRD.md §3 (personas), §5 (tier table), ARCHITECTURE.md §3.1.2 (classifier outputs table).

## Decision

The platform uses exactly three complexity tiers. The classifier defined in RFC-0002 assigns one of these tiers to every incoming story; operators may override the inferred tier, and all overrides are logged for telemetry. The full scoring rubric lives in the RFC; this ADR records the tier identities and their canonical bundles.

**Simple** targets a single developer with at most one integration and no auth or compliance signals, where the story is under 200 words. Trinity mode is `single` (Architect-only). The doc slate contains two documents (`manual` + `api`). The cost ceiling is $10. Auto-merge on PASS is configurable. Test policy is `best-effort`.

**Standard** targets a small team with two to four integrations and basic auth, where the story is under 500 words. Trinity mode is `trinity-hybrid`. The doc slate contains four documents (`design` + `api` + `manual` + `manual`). The cost ceiling is $30. Human approval is required for `direct_branch` output. Test policy is `required`.

**Enterprise** applies when regulated data terms appear (HIPAA, PCI, GDPR), SLO targets are present, multi-tenant concerns are stated, or the story is 500 words or longer. Trinity mode is `trinity` (full consensus). The doc slate contains eight documents. The cost ceiling is $100. Human approval is always required. Test policy is `required`.

Each tier carries a default cost ceiling, maximum runtime, and drift-sentinel module set as specified in PRD §5. Operators may override the inferred tier for any submission; overrides are recorded in the telemetry log without blocking the pipeline.

## Consequences

### Positive

- A small number of named configurations is easier for operators to reason about and document. Each tier name resolves all downstream parameters at once; no interpolation is required.
- Each tier maps to a real persona (Solo Builder, Platform Engineer, Compliance-Bound Architect), so tier assignments carry intuitive meaning for the teams receiving them.
- Tier cardinality matches the three natural Trinity routing modes (`single`, `trinity-hybrid`, `trinity`), eliminating mapping indirection between the classifier output and the routing layer.

### Negative

- Stories that fall between tier boundaries are forced into the adjacent tier. Boundaries encode current best guesses, not permanent truth; they will need to be recalibrated as production data accumulates.

### Neutral

- The operator override path provides an escape hatch for stories the classifier misclassifies. Because overrides are logged, the frequency and direction of corrections feeds back into future calibration.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Two tiers (Simple and Enterprise) | Most real teams sit in the middle ground and would be miscategorized in either direction; the Standard tier exists precisely to cover that population. |
| Five tiers | Additional cardinality does not map to distinct downstream configurations. The number of meaningfully different doc slates, routing modes, and policy bundles does not grow beyond three. |
| Continuous complexity score with continuous parameter interpolation | Configuration surface area on dependent systems (doc slate, Trinity mode, policy fields, cost ceiling) would be unmanageable; operators would require a parameter interpolation table for every downstream field on every story. |
| No automatic classification; require operator to choose tier | The platform's promise of low-friction submission requires a sensible inferred default. Mandatory operator selection shifts burden back to the user and creates inconsistency across teams. |
