# MVP Demo Quickstart

**Status:** Draft
**Author:** Anthony G. Johnson II
**Audience:** Demo runner (operator running the workflow live, or presenter walking through a pre-recorded run)
**Created:** 2026-05-08
**Last Updated:** 2026-05-08
**Suite:** ai-powered-lead-gen-mvp
**Related:** [Operator User Manual](./operator-manual.md), [Reviewer and Approver Guide](./reviewer-guide.md)

## Before the Demo

Confirm before the walkthrough begins:

- [ ] **ICP** is locked.
- [ ] **Offer** is chosen and the operator can speak to its core value proposition.
- [ ] **Target company** input is ready - either a pre-selected company for manual entry, or a natural-language description for Semantic account discovery.
- [ ] **Approval owner** is available during the demo to take the explicit approval action live.
- [ ] **Source data** access is confirmed (data provider configured, or manual prospect data ready).
- [ ] **Demo scope** is set: 1 target company + 1 prospect (minimum) or 1 + 2 from the same company (preferred). Decide before starting; do not switch mid-run.

Success looks like: an end-to-end Prospect package with reviewer approval recorded, in under 30 minutes from campaign creation to approved export.

## The Demo Walkthrough

### 1. Create the campaign

Set name, description, ICP, buyer role, offer, conversion goal, and approval owner.

> **Point out:** Every artifact downstream is bound to this campaign. ICP and offer drive personalization and Guardrail behavior throughout.

### 2. Select the target company

Manual path: enter the company directly. Semantic account discovery path: describe the profile in natural language; the system extracts criteria and returns banded candidates.

> **Point out:** Confidence is banded `<60` low, `60-79` needs review, `>=80` high. We approve high-confidence candidates and refine criteria when nothing reaches `60`.

### 3. Identify prospects

Ask the system to identify prospects at the approved company. For minimum demo, 1 prospect is enough; for preferred demo, 2 prospects from the same company.

> **Point out:** Prospects are people; buyer roles are the roles those people play in the buying process.

### 4. Show prospect-company validation

The system validates each prospect against the target company using a cited source.

> **Point out:** Validation has its own `source_ref`. We do not approve prospects whose validation source is stale or missing.

### 5. Walk through the Prospect dossier

Show the confirmed facts list, the assumptions list, and the source refs.

> **Point out:** Confirmed facts have source refs per ADR-0006. Assumptions are flagged distinctly - they are not facts. The research checklist meets the threshold (6 of 9 with categories 1-2 mandatory).

### 6. Show personalization hook selection

Show the hook classifications: professional, company-relevant, role-relevant, or excluded.

> **Point out:** Excluded hooks are blocked automatically. Sensitive personalization is not a judgment call we leave to the operator.

### 7. Show the first-touch email

Walk through subject, opening, body, and call to action.

> **Point out:** No broken variables. Every claim in the body traces to a `source_ref` in either the dossier or the Approved claim library.

### 8. Show the multi-channel cadence

Walk through the steps and their channels.

> **Point out:** MVP-required channels (email, manual follow-up task) are present. MVP-optional channels (LinkedIn, phone, voicemail) are marked optional or hidden per the demo's approved scope.

### 9. Show the Guardrail panel

Show at least one blocking and one non-blocking finding to demonstrate verbosity. Resolve the blocking one with a fix-and-rerun; demonstrate the override flow on the non-blocking one.

> **Point out:** Overrides are recorded with reviewer identity, the offending Guardrail result ID, and the reason. The audit trail is the system's accountability story.

### 10. Show the Readiness score

Show the breakdown across dimensions.

> **Point out:** The MVP-ready threshold is `>=80`, but score is necessary, not sufficient. Per ADR-0001, no package is approved without explicit reviewer action regardless of score.

### 11. Reviewer approves the Prospect package

The approval owner takes explicit action: approve, reject, or request revision. For the demo, run the approve flow.

> **Point out:** The Review record captures reviewer identity and timestamp. Without this action, the package's `package_status` does not change to `approved`.

### 12. Show the exported package

Per FR-027, the export contains: campaign summary, target company profile, prospect profile, validation status, Prospect dossier, personalization hooks, first-touch email, MVP-required cadence, Guardrail results, approval status, Readiness score.

> **Point out:** Stakeholders can see how the workflow moved from target selection to outreach recommendation. The audit trail follows the package.

## Coordinated Multi-Buyer Demo (Preferred 1+2 Scope)

When running the preferred scope, after step 12 above also show:

- The two messages side by side. They share campaign theme but differ in role-specific framing per FR-013.
- Company-level facts are consistent across both messages.
- Each message has its own Guardrail results and personalization hooks.
- The Readiness score is per Prospect package; each prospect has their own.

> **Point out:** This is what coordinated buying-committee outreach looks like - tailored per role, consistent on company facts, both gated by the same approval rule.

## Common Demo Issues

| Issue | Quick recovery |
|-------|----------------|
| Provider unavailable mid-demo | Fall back to manual target-company entry. Note that data-provider selection (OQ-001) is an open Phase 0 decision; the workflow handles provider absence by design. |
| Guardrail false positive on a fine-looking claim | Use the override flow with a recorded reason. State that this is exactly what reviewers do in production - the override audit trail is part of the design. |
| Readiness score under 80 because the checklist threshold isn't met | Show which categories are missing in the breakdown. If appropriate, supply `user_provided` facts in real time and re-run the dossier step. The system records the `user_provided` marker explicitly. |
| Wrong-person Guardrail flagged the message | Show how fix-and-rerun corrects the message. Do not edit the Prospect record to silence the Guardrail; that is the wrong direction. |
| Demo time runs short before the reviewer approves | Skip the cadence walkthrough (step 8) and head straight from messages (step 7) to Guardrails (step 9). The cadence is most easily understood from the exported package in step 12. |

## After the Demo

Capture before stakeholders leave:

- **Stakeholder feedback** per FR-027 (the PRD's end-to-end demo package requirement) - what surprised them, what raised confidence, what raised concerns.
- **Reviewer FR-028 ratings** (the PRD's human-quality comparison rubric) - 1-5 on research quality, personalization quality, message usefulness. Target average is 4.0 or higher.
- **Open decisions** mentioned during the demo (Phase 0 OQs, especially OQ-001 data provider, OQ-002 deliverable format, OQ-003 Chrome extension scope).
- **Notes for the change-management process** - any FR / NFR adjustments stakeholders requested.

For deeper detail on any step, see the [Operator User Manual](./operator-manual.md). For reviewer rationale on the approval flow, see the [Reviewer and Approver Guide](./reviewer-guide.md).
