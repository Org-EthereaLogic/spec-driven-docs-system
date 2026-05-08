# ADR-0005: Iterative-Incremental SDLC with Phase Gates

**Related:** [System Architecture](../design/architecture.md), [ADR-0003 Workflow Runner](./0003-deterministic-workflow-runner.md)

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Product sponsor, technical lead

## Context

The AI-Powered Lead Generation MVP carries significant early uncertainty. Several Phase 0 decisions remain open at planning time: which data provider or source strategy to use, which deliverable format to produce (script, notebook, or UI), which model mode is acceptable (single-model or hybrid routing), and what evidence standard governs the prospect dossier. AI output quality cannot be fully predicted upfront; it must be tested against real demo prospects before the team can confidently scope the remaining work.

A strict waterfall model would require these decisions to be locked before implementation begins, which is not feasible. Conversely, a pure sprint-based agile approach without formal phase gates would not produce the explicit go/no-go approvals that the product sponsor and reviewer / approver group require before each major delivery increment.

The team is small, so the process model must remain lightweight. Ceremonies and overhead must be proportional to what a small team can actually sustain. The canonical demo has a clear definition of done — a complete prospect package covering at least one target company and one prospect — and that milestone boundary maps naturally to a mid-project stopping point before scale-readiness work begins.

## Decision

We will deliver the MVP using an iterative-incremental lifecycle with explicit phase gates between each of the following four phases:

- **Phase 0 — Decisions:** close all blocking open questions, select demo inputs, confirm delivery format, evidence standard, model mode, data-source strategy, and risk posture.
- **Phase 1 — Foundation:** implement the deterministic workflow runner, data schemas, core generation steps, basic run logging, and a minimum demo package capable of processing one target company and one prospect end-to-end.
- **Phase 2 — End-to-end demo:** strengthen guardrails, readiness scoring, the human-in-the-loop review flow, test execution, and observability to produce the preferred demo package (one target company, two prospects, coordinated messaging).
- **Phase 3 — Scale-readiness:** scope and estimate follow-on integrations for data enrichment, CRM / ATS, outbound tooling, analytics, and optional browser workflow concepts.

Each phase ends with an explicit gate covering five categories drawn from Project Plan §1.1:

1. **Scope** — canonical MVP scope and optional-feature boundaries confirmed.
2. **Technical feasibility** — delivery format, architecture direction, and build approach confirmed.
3. **Risk-profile** — high-impact risks accepted, mitigated, or deferred.
4. **Schedule / budget** — rough-order-of-magnitude estimate confirmed or re-baselined.
5. **Demo readiness** — demo package quality and known gaps confirmed before stakeholder walkthrough.

The schedule and cost estimate will be re-baselined after Phase 0 exit, once the data-source strategy, deliverable format, and model mode decisions are resolved. No downstream phase dates are committed before those decisions land.

Within phases, work proceeds in short build iterations (two to three business days each) with continuous QA per the Project Plan WBS quality-control workstream, ensuring that schema validation, guardrail checks, and reviewer quality ratings are tracked from the first iteration, not only at final dry-run.

## Consequences

### Positive

- Delivery milestones align with decision points, so the team does not build on unresolved assumptions.
- Phase gates allow scope to expand or contract in a controlled way at each boundary rather than mid-stream.
- The end-to-end demo (Phase 2) is a distinct, approvable milestone before scale-readiness work begins.
- Short iterations surface AI quality issues early, when remediation cost is lowest.

### Negative

- Phase gates require coordinated availability from the product sponsor and reviewer / approver group; delays in approver availability can stall progression.
- Continuous QA from day one adds overhead during Phase 1, when the workflow is still being assembled.
- The model requires active backlog management and regular status reporting throughout, which adds a small but non-zero process burden on the technical lead.

### Neutral

- This lifecycle decision shapes the Project Plan workstream sequencing, milestone definitions, and the architecture's phased implementation plan; changes to the phase structure would require a corresponding update to those documents.

## Alternatives considered

| Alternative | Why not chosen |
|---|---|
| Strict waterfall | Too many Phase 0 decisions remain open for a full upfront design commitment. Locking architecture and schedule before data-source and delivery-format decisions are resolved would produce an unreliable baseline. |
| Pure agile, no phase gates | The product sponsor and reviewer / approver group require explicit go/no-go approval before each major increment. Sprint-only cadence without gates does not produce those approvals. |
| Spike-then-build (PoC followed by full waterfall) | The PoC and the demo are essentially the same artifact for this MVP. Separating them into a throwaway spike and a subsequent waterfall build would duplicate effort and delay the first working demo. |
