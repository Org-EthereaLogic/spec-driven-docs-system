# ADR-0003: Defer the Q-Score stability module to Phase 4

**Status:** Accepted
**Date:** 2026-04-26
**Deciders:** SDLC Pro architecture lead

## Context

The PR Drift Sentinel was designed with three modules: spec-drift, path-policy, and stability-drift. The first two are deterministic checks against the original TaskSpec. Spec-drift verifies that changed files remain within the scope described in the TaskSpec. Path-policy enforces structural rules (directory layout, naming conventions, prohibited paths) that were declared when the task was opened. Both modules produce a pass or fail that can be verified against the TaskSpec by inspection; their behavior is auditable per PR.

Stability-drift is different in kind. It computes a Q-Score — a mathematical estimate of repository destabilization derived from the Entropy-Guided DevOps Gatekeeper prototype lineage (Gemini's "E-Git" / "Entropic-Gated DevOps Oracle"). The formula is:

```text
Q-Score = 1 − clip(ΔS / threshold, 0, 1)
```

where ΔS is the entropy delta measured over the file-set graph for the PR. A Q-Score below the configured floor blocks the merge.

The problem is calibration. The SDLC Pro environment has no post-merge outcome history against which to set the threshold. An arbitrary threshold produces false positives — blocking PRs that would have been safe — and false negatives — passing PRs that would have introduced instability. Neither failure mode is acceptable: false positives erode developer trust in Sentinel output; false negatives make the gate feel authoritative while providing no protection. Shipping a math-based merge gate without calibration data is a false-confidence trap.

The AdaptiveThresholdManager component was designed to tune the Q-Score threshold over time by correlating threshold overrides with post-merge outcomes. It cannot do that tuning reliably until it has observed at least 50 post-merge outcomes. In a new environment that data does not yet exist.

These constraints were identified during architecture review and are documented in ARCHITECTURE.md §3.5 (the modules table), §6.2 (the risk note on uncalibrated thresholds), and §7 (the phased build plan).

## Decision

The PR Drift Sentinel ships in Phase 3 of the build plan with only the spec-drift and path-policy modules active. Both modules are deterministic, verifiable, and require no calibration data.

Q-Score implementation begins in Phase 4 behind a feature flag. The initial deployment uses a permissive threshold (Q-Score floor 0.4) so that the gate fires only on severe entropy spikes while the AdaptiveThresholdManager begins accumulating override and outcome data. Q-Score does not become a merge gate until the AdaptiveThresholdManager has recorded at least 50 post-merge outcomes and the resulting threshold distribution is reviewed.

This is a sequencing decision, not a capability cut. The Q-Score module remains in-scope, documented, and planned. Phase 4 means it ships later with calibration; it does not mean it is cancelled or deprioritized in principle.

## Consequences

### Positive

- Phase 3 ships with high-confidence, deterministic merge checks rather than an uncalibrated mathematical gate. Every Sentinel verdict in Phase 3 is directly traceable to a TaskSpec clause or a structural rule, which makes the tool trustworthy from day one.
- The AdaptiveThresholdManager has Phase 3's full operating window to gather override and outcome data before Q-Score affects any merge decision. By the time Q-Score becomes a gate in Phase 4, the threshold will reflect real SDLC Pro usage rather than an arbitrary starting value.

### Negative

- During Phase 3, SDLC Pro cannot detect stability drift that does not manifest as a spec or path violation. A PR that changes the right files in the right directories but still degrades repository health will pass Sentinel without comment.
- The prototype lineage promised mathematical merge gating as a differentiating capability. Users who read the Entropy-Guided DevOps Gatekeeper design materials and expect that capability at launch must wait until Phase 4.

### Neutral

- The deferral is reversible. Once calibration data exists, enabling Q-Score as a merge gate requires only a feature flag change and a threshold configuration update. No architectural change is needed.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Ship Q-Score in Phase 3 with a hard-coded threshold | An untuned threshold will produce false positives that irritate developers and false negatives that erode trust. Neither failure is recoverable quickly once users have formed an impression of the gate's reliability. |
| Drop Q-Score from the design entirely | Mathematical stability gating is one of the differentiating capabilities derived from the prototype lineage. Removing it permanently discards a design investment and reduces the Sentinel to a linter. Deferral is not the same as cancellation. |
| Ship Q-Score in warn-only mode in Phase 3 | Warn-only output without merge consequences trains users to dismiss Sentinel warnings. By the time Q-Score becomes a gate in Phase 4, the warning will have been noise for an entire phase and users will have learned to ignore it. |
