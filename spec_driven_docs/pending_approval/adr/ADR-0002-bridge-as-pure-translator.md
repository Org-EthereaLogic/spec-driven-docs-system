# ADR-0002: Spec-to-TaskSpec bridge is a translator, not an orchestrator

**Status:** Accepted
**Date:** 2026-04-26
**Deciders:** SDLC Pro architecture lead

## Context

The original SDLC Pro design proposed a bridge module that served two purposes: it orchestrated the documentation-authoring pipeline (running `/doc-plan`, `/doc-write`, `/doc-review`, and `/doc-promote` in sequence) and it translated the resulting approved docs into a TaskSpec for ADWS_PRO. Both responsibilities were bundled into one component because, at the time of initial design, no canonical headless orchestrator existed in spec-driven-docs-system.

A re-audit of spec-driven-docs-system v1.0.0 surfaced `/doc-flow` as exactly that missing piece. Defined in `.claude/commands/doc/doc-flow.md` and documented in ARCHITECTURE.md §3.2, it already chains plan → write → review → promote as a single invocation, applies smart per-doc model selection (design/rfc/openapi → Opus, adr → Haiku, api ≥5 sections → Sonnet), enforces all four quality gates with per-doc `quality_profile` thresholds, and caches spec analysis daily. Its `--auto-promote` flag drives docs all the way to `approved_final/` without human intervention — exactly the mode the SDLC Pro intake lane required.

The orchestration the bridge would have owned overlapped entirely with `/doc-flow`. Two systems driving the same pipeline would have produced competing invocations of `/doc-write` and `/doc-review`, inconsistent workflow-state transitions across `rough_draft/`, `pending_approval/`, and `approved_final/`, and diverging quality-gate enforcement paths. The bridge's proposed orchestration logic was a strict functional subset of what `/doc-flow` already shipped.

That duplication was the trigger. With `/doc-flow` validated as part of v1.0.0, the correct response was to hand orchestration back upstream and constrain the bridge to its single unique responsibility: translating an approved-doc payload into a TaskSpec.

## Decision

The Spec-to-TaskSpec bridge is a pure translator. It accepts an approved-doc payload posted by the `sdlc-promote` plugin — a JSON object containing `suite_id`, `approved_docs[]` with `doc_path`, `doc_type`, and `quality_score` per entry — and produces a TaskSpec validated via AJV against `ADWS_PRO/specs/schema/taskspec.schema.json`. It then POSTs that TaskSpec to ADWS_PRO's `/api/tasks` endpoint.

The bridge does not invoke `/doc-plan`, `/doc-write`, `/doc-review`, or `/doc-promote` directly. It does not track workflow-stage transitions in `spec_driven_docs/`. It does not retry failed doc generations. All doc-pipeline orchestration is delegated to `/doc-flow`, which is invoked by the `sdlc-intake` plugin via `/doc-flow {suite_id} --auto-promote`. The `sdlc-promote` plugin fires only after `/doc-flow` has completed and a stakeholder (or the auto-approve rule for Simple tier) has moved docs to `approved_final/`.

The bridge's translation logic is the sole non-trivial concern: extracting `acceptance_criteria` from design doc "Goals" sections, mapping `policy.test_policy` from complexity tier, inferring `risk.task_size` from doc count, and constructing `task.file_hints` from API doc endpoint paths and design doc implementation-plan references. That mapping belongs in the bridge and nowhere else.

## Consequences

### Positive

- Separation of concerns is clean: one orchestrator (`/doc-flow` via `sdlc-intake`), one translator (the bridge). Neither component needs to know about the other's internals.
- The bridge becomes small enough to ship in days as Phase 1 of the phased build plan, rather than requiring the weeks a full orchestrator would take. The scope is bounded: read an approved-doc payload, map fields, validate against a schema, POST.
- Smart per-doc model selection is inherited automatically from `/doc-flow` without any bridge-side configuration. When spec-driven-docs-system updates its model-selection rules, the bridge benefits immediately.
- The `sdlc-promote` plugin and the bridge are coupled by an explicit JSON contract (ARCHITECTURE.md §4.3) — the only integration surface the bridge must maintain.

### Negative

- Any orchestration feature SDLC Pro needs that `/doc-flow` does not support — for example, a doc-retry policy tuned specifically to SDLC Pro's quality thresholds — requires an upstream contribution to spec-driven-docs-system rather than a local implementation in the bridge, carrying coordination and review cost.

### Neutral

- The bridge is intentionally coupled to the `sdlc-promote` plugin for its inputs. The plugin enforces that only docs that have completed the `/doc-flow` pipeline and reached `approved_final/` are handed to the bridge; loosening that coupling would reintroduce the risk of partially-reviewed docs reaching ADWS_PRO.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Keep bridge as orchestrator-plus-translator | Duplicates `/doc-flow` entirely. Two systems would drive the same workflow-state transitions, producing race conditions and inconsistent quality-gate enforcement. The duplication was the specific finding that triggered this ADR. |
| Replace `/doc-flow` with a custom orchestrator inside SDLC Pro | Discards a tested v1.0.0 capability built for exactly this use case. Creates an ongoing maintenance burden: every future improvement to the doc pipeline (new quality profiles, new template types, updated model-selection rules) would require parallel updates in the custom orchestrator. |
| Skip the bridge and have `sdlc-promote` POST directly to ADWS `/api/tasks` | TaskSpec construction involves non-trivial field mapping from multiple doc types (design, api, manual, adr). Embedding that logic in a doc-system plugin would violate the plugin's single responsibility (wrapping `/doc-promote`) and couple a doc-system component to ADWS_PRO's schema. The bridge exists precisely to own this mapping in the right layer. |
