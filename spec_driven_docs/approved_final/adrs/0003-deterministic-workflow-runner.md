# ADR-0003: Use a Code-Defined Deterministic Workflow Runner

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Technical lead

## Context

The AI-Powered Lead Generation MVP must produce repeatable, auditable runs. The workflow's shape is well known and stable: campaign setup, target account selection, prospect identification, prospect-company validation, Prospect dossier generation, research checklist, personalization hook selection, first-touch email generation, multi-channel cadence planning, Guardrail checks, Readiness score, and Human-in-the-loop review. The order is the same for every prospect.

Agent-orchestrated workflows that let an LLM choose the next step at runtime undermine this stability. Two runs of the same campaign can take different paths, skip steps, repeat steps, or invoke tools in an order that the reviewer cannot predict. That non-determinism breaks the Guardrail gates - a Guardrail can only run between steps if the runner guarantees those step boundaries exist - and erodes the audit trail the project depends on. Reviewers comparing prospect packages cannot tell whether a difference reflects the prospect or the orchestrator's choices.

The PRD encodes the same requirement directly: FR-021 specifies that the system shall use deterministic code to control step order, that LLM prompts receive only the structured context required for that step, and that LLM responses are validated before downstream use. NFR-004 reinforces this by requiring schema-valid JSON output from every step or a safe failure with an actionable error.

## Decision

The runner is implemented as code with the step sequence fixed at design time. Acceptable forms include a function-call sequence, an explicit state machine, or a hand-authored DAG; what they share is that the order of steps is determined by the application, not selected at runtime by an LLM.

LLMs are invoked only inside individual steps to produce content - dossier text, message body, hook suggestions, account-fit interpretations. Each LLM call receives a structured input (the typed output of the previous step plus any explicit context the step assembles) and is expected to return a structured response that conforms to the step's schema (per ADR-0002). The LLM does not see beyond the step it is participating in and does not influence which step runs next.

Conditional branches are encoded as explicit code paths. Examples include the choice between manual target-company entry and Semantic account discovery, the inclusion of MVP-optional channels (LinkedIn, phone, voicemail), and the no-response follow-up that depends on opt-in. Each branch is named, reachable from a known input, and visible in the workflow run log.

The runner persists a workflow run log capturing step order, timing, model identity, inputs, outputs, validation results, Guardrail results, and any errors. The log is the canonical record of what happened during a run.

## Consequences

### Positive

- Runs are reproducible. The same inputs produce the same step sequence every time.
- Guardrails have stable insertion points between steps and can gate progression deterministically.
- Debugging is simpler: failures localize to a single step, and the run log identifies what the runner saw before and after.
- The audit trail required by NFR-005 (explainability) and NFR-010 (observability) follows naturally from the structure.

### Negative

- The workflow shape is harder to evolve. Adding a step or reordering existing steps requires a code change and review.
- Patterns that benefit from runtime flexibility - exploratory tool selection, opportunistic enrichment - are out of reach in this design.

### Neutral

- Shapes the architecture diagram in [architecture.md](../design/architecture.md) and the data-flow contract between steps.
- MVP-optional channels are implemented as opt-in branches rather than LLM-suggested additions.

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| LLM-orchestrated agent that picks the next step | Non-determinism breaks reproducibility, Guardrail gating, and audit. Directly violates FR-021. |
| Hybrid (code-defined main path, LLM picks optional steps) | Adds runtime complexity without solving an MVP problem. Deferred for post-MVP review if a real need surfaces. |
