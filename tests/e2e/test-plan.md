# E2E Test Plan: Spec-Driven Documentation System

## Overview

This test plan validates the complete documentation workflow from specification creation through review and iteration.

## Test Phases

### Phase 1: Document Planning (COMPLETED)
- [x] Test `/doc-plan` command with --type api
- [x] Test `/doc-plan` command with --type design
- [x] Test `/doc-plan` command with --type manual
- [x] Verify spec files created in correct location

### Phase 2: Document Generation (COMPLETED)
- [x] Test `/doc-write` on API spec
- [x] Test `/doc-write` on User Manual spec
- [x] Verify output to draft location
- [x] Fix output directory issues

### Phase 3: Review Workflow - Architecture Doc (IN PROGRESS)
- [ ] Run `/doc-write` on architecture spec
- [ ] Verify output saved to `drafts/`
- [ ] Run `/doc-review` on generated architecture doc
- [ ] Test iteration loop if issues found
- [ ] Verify quality gate scoring

### Phase 4: Batch Operations
- [ ] Test `/doc-batch generate` with suite
- [ ] Test `/doc-batch review` with suite
- [ ] Test `--parallel` flag
- [ ] Test `--continue-on-error` flag

### Phase 5: Sync Operations
- [ ] Test `/doc-sync` for terminology consistency
- [ ] Test `/doc-sync --fix` auto-correction
- [ ] Verify cross-reference validation

### Phase 6: Suite Management
- [ ] Test `/doc-status` dashboard
- [ ] Test suite manifest operations
- [ ] Test `/doc-improve` pattern learning

## Test Documents

| Doc ID | Type | Spec Path | Output Path | Status |
|--------|------|-----------|-------------|--------|
| Doc 1 | api | specs/docs/e2e-test/api-reference-spec.md | drafts/api-reference.md | Pending |
| Doc 2 | manual | specs/docs/e2e-test/user-guide-spec.md | drafts/user-guide.md | Pending |
| Doc 3 | design | specs/docs/e2e-test/architecture-spec.md | drafts/architecture.md | **In Progress** |

## Backport Notes

Issues identified for upstream fixes:
1. Default manifest template should use `drafts/` instead of `final/`
2. `/doc-write` output should always go to draft location initially
3. Only `/doc-approve` (or similar command) should move documents to `final/`

## Progress Tracking

See `test_progress.json` for detailed event log.
