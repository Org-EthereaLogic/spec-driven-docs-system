# ADR-0004: Default to human-in-the-loop for ship across all tiers in v1

**Status:** Accepted
**Date:** 2026-04-26
**Deciders:** SDLC Pro architecture lead

## Context

The Drift Sentinel was designed to produce a PASS verdict when a pull request's observable behavior remains within the tolerance envelope defined in its TaskSpec. The tier table in PRD §5 originally specified that a Simple-tier configuration could act on that verdict autonomously, with "Auto-merge on PASS: yes" as the documented default. That language assumed a level of production-validated confidence that v1 had not yet established.

The governing constitution for SDLC Pro resolves competing concerns in the following order: Safety, Evidence Traceability, Security, Simplicity, Reproducibility, Performance. Autonomous shipping without a human reviewer touches Safety and Evidence Traceability simultaneously. A platform without validated production runs carries an unknown false-negative rate on its primary quality gate. The PRD §8 trust threshold — a Drift Sentinel false-negative rate at or below 5% — provides the right criterion for relaxing autonomy, but that threshold cannot be cited as met until measured data exists.

PRD §9 captured this as risk R4: premature autonomy before trust is earned. ARCHITECTURE.md §6.8 framed the same tension as an open governance question: when is autonomous ship safe to enable, and who decides? Both converged on the same answer — the safe default must be conservative, and autonomy must be unlocked through earned trust rather than assumed at install time.

## Decision

The TaskSpec field `risk.requires_human_approval_before_ship` defaults to `true` for every tier in v1, including Simple. No tier ships to main autonomously by default.

Operators may override this default on a per-tier basis through explicit operator configuration. The override is not hidden or discouraged, but it is not the default; operators must affirmatively opt out of human-in-the-loop. Every opt-out is recorded in the run manifest so the audit trail captures which runs shipped without a human approver and under whose configuration authority.

The default may be relaxed in v2 after the trust criteria in PRD §8 are met: specifically, a Drift Sentinel false-negative rate at or below 5% and an override frequency below the threshold defined in that section. Relaxation is a v2 decision with its own ADR, not a silent change to configuration defaults.

## Consequences

### Positive

- The decision aligns with the governing constitution's resolution order. Safety and Evidence Traceability both rank above Performance and Speed, and this default honors that ordering without requiring per-project configuration.
- Every merged pull request in v1 carries a recorded human approver in the run manifest. The evidence trail is complete and auditable from day one, not retrofitted after an incident.
- The path to autonomy is explicit: PRD §8 defines measurable criteria, this ADR names them, and a future ADR will confirm when they are met. There is no ambiguity about what needs to change.

### Negative

- Simple-tier users chose that tier in part because the PRD tier table advertised autonomous merging on PASS. Those users pay an extra human-approval step on every pull request, and the throughput advantage they expected is deferred until v2.
- This decision directly contradicts the tier table language in PRD §5. That is a deliberate v1 override, not an oversight. The tier table must be updated, and Simple-tier users must be informed that auto-merge is unavailable until the false-negative rate threshold is met. The contradiction is honest: trust must precede autonomy, and the tier table was written before production data existed.

### Neutral

- Operators who understand the trade-off retain the ability to enable autonomous shipping through explicit opt-out configuration. The platform does not prevent autonomy; it requires a deliberate choice to enable it. Teams running SDLC Pro in controlled environments may opt out and accept responsibility for the unmeasured false-negative risk.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Default Simple tier to autonomous ship on Drift Sentinel PASS | Rejected because the platform has no validated false-negative rate in production. A PASS verdict on an unvalidated gate is not the same as a safe-to-ship signal. The tier name does not substitute for measured trust. |
| Require human approval only for Enterprise tier | Rejected because the autonomy ladder should be earned per-tier through measured trust, not assigned by tier name at product launch. Naming a tier "Enterprise" does not make its quality gate safer; naming a tier "Simple" does not make autonomous shipping riskier. Trust is a function of validated false-negative rates, not tier labels. |
| Make the default an operator decision at install time | Rejected because a configurable-at-install default is functionally equivalent to no default. The safe default must be conservative and hold until the platform earns the right to relax it. Operators who want autonomy can opt out; they should not be required to opt in to safety. |
