# ADR-0001: Require Human-in-the-Loop Approval for All Outreach

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Product sponsor, technical lead, reviewer / approver group

## Context

Outbound lead generation routinely fails when AI-generated content reaches prospects unreviewed. Source materials catalog the failure modes: messages addressed to the wrong person, references to companies the prospect no longer works at, unresolved placeholder variables in send-ready copy, claims about the prospect or product that are not supported by evidence, and generic personalization that signals automation. Each failure damages sender credibility and is difficult to retract once a message is delivered.

The AI-Powered Lead Generation MVP exists to prove a quality-first workflow before scale. Auto-sending plausible-but-occasionally-wrong AI output would invert that priority. The source planning context emphasizes governance, validation, and human judgment as the differentiators for this product, and stakeholders expect a demonstrable approval gate they can audit.

A Readiness score is part of the workflow, but a numeric heuristic cannot detect every failure mode. Subtly wrong company facts, tonally inappropriate framing, or context the model lacked all pass automated scoring while still requiring correction. The score is therefore necessary but not sufficient evidence that a Prospect package is ready for use.

## Decision

Every outreach artifact requires explicit Human-in-the-loop approval before it can be marked ready for use, exported, or copied to an outbound platform. This applies to first-touch emails, multi-channel cadence steps, LinkedIn copy, phone notes, voicemail scripts, and follow-ups - every channel, every send.

The Review step is the single approval gate. Bypassing it is prohibited for the MVP: programmatic export of unapproved content, auto-promotion based on score thresholds, and automated forwarding to outbound platforms are all blocked at the workflow boundary. A Readiness score of 80 or higher is necessary but does not by itself release a Prospect package; explicit reviewer action is required.

Approval is recorded against the Prospect package with reviewer identity, timestamp, and a link to the prospect, campaign, and message or cadence item being reviewed. Overrides - reviewers accepting content despite a Guardrail flag - are recorded the same way and remain auditable. Unapproved content stays in draft state regardless of any other workflow signal.

## Consequences

### Positive

- Prevents AI errors from reaching prospects, preserving sender reputation and stakeholder trust in the demo.
- Gives reviewers veto power over every outbound artifact, including those that pass numeric guardrails.
- Produces an auditable approval record for each Prospect package, supporting governance and explainability goals.
- Aligns the MVP with the project's quality-over-volume principle, reinforcing the product narrative.

### Negative

- Throughput is bounded by reviewer attention; the workflow cannot exceed human review capacity without later automation work.
- Noisy Guardrails increase reviewer load and risk reviewer fatigue, which can dull approval discipline over time.
- The reviewer becomes the visible bottleneck during demos and at scale, a cost that must be planned around in steady-state operation.

### Neutral

- Shapes the data model: the Review object is a first-class workflow artifact, not an annotation.
- Shapes the demo deliverable: every walkthrough must show the Review step, not just the generated content.
- Defers any automation of approval to a post-MVP decision; that decision is explicitly out of scope here.

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| Auto-send when Readiness score is 90 or higher | The score is a heuristic. It cannot detect subtly wrong facts, missing context, or tonally inappropriate framing - exactly the failure modes the MVP exists to prevent. |
| Auto-approve content from trusted reviewers | Trust calibration requires a working Review history first. The MVP must demonstrate the gate works before any bypass can be justified. |
