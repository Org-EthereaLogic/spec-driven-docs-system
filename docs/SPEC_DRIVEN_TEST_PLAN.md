# Spec-Driven Docs System Test Plan

## Test Plan for Enhanced ADWS v1.0 Design Documents

**Purpose:** Fully exercise all features of the spec-driven docs system while generating 6 design documents for Enhanced ADWS v1.0.

**Test Duration:** Single session with checkpoints for context management

---

## Document Generation Matrix

| Doc # | Document | Template Type | Primary Features Tested |
|-------|----------|---------------|------------------------|
| 2 | Software Requirements Specification (SRS) | `design` | `/doc-plan`, `/doc-write`, basic workflow |
| 3 | Architecture Blueprint | `design` | `/doc-review`, quality gates, iteration |
| 4 | Software Design Document (SDD) | `design` | Suite operations, dependencies |
| 5 | Test Plan | `design` | `/doc-batch` generate, parallel execution |
| 6 | Build Instructions | `manual` | `/doc-sync`, cross-reference validation |
| 7 | CONTRIBUTING.md | `manual` | `/doc-improve`, `/doc-status`, full cycle |

---

## Feature Coverage Matrix

### Commands to Test

| Command | Test Phase | Document(s) | Validation |
|---------|------------|-------------|------------|
| `/doc-plan` | Phase 1-2 | Doc 2, 3 | Spec created with correct structure |
| `/doc-write` | Phase 2-3 | Doc 2, 3, 4 | Document generated from spec |
| `/doc-review` | Phase 3-4 | Doc 3, 4 | Quality score returned, issues identified |
| `/doc-review --fix` | Phase 4 | Doc 3 | Auto-fixable issues resolved |
| `/doc-sync` | Phase 5 | Suite | Cross-references validated |
| `/doc-batch generate` | Phase 4 | Doc 5, 6 | Parallel document generation |
| `/doc-batch review` | Phase 5 | Suite | Batch review execution |
| `/doc-status` | All Phases | Suite | Dashboard displays correctly |
| `/doc-improve` | Phase 6 | N/A | Patterns extracted from successful docs |

### Agents to Test

| Agent | Model | Test Phase | Validation |
|-------|-------|------------|------------|
| doc-orchestrator | Opus | Phase 1, 4, 6 | Specs created, batch coordinated |
| doc-writer | Sonnet | Phase 2-4 | Documents generated |
| doc-reviewer | Sonnet | Phase 3-5 | Quality validated |
| doc-librarian | Haiku | Phase 5 | Consistency checked |

### Quality System to Test

| Feature | Test Phase | Validation |
|---------|------------|------------|
| Spec completeness gate | Phase 1-2 | Spec passes validation |
| Content quality gate | Phase 2-3 | No placeholders, valid code blocks |
| Consistency gate | Phase 3-5 | Terminology enforced |
| Final approval gate | Phase 5-6 | Documents approved |
| Quality scoring (A-F) | Phase 3-5 | Scores calculated correctly |
| Auto-fix capability | Phase 4 | Fixable issues resolved |

### Suite Operations to Test

| Feature | Test Phase | Validation |
|---------|------------|------------|
| Suite creation | Phase 1 | manifest.json created |
| Document dependencies | Phase 4 | Dependency order respected |
| Parallel execution | Phase 4 | Multiple docs generated concurrently |
| Cross-reference sync | Phase 5 | Links validated across suite |
| Health scoring | Phase 5-6 | Suite health calculated |
| Checkpoint/resume | If needed | State preserved across context |

---

## Test Phases

### Phase 1: Suite Setup and First Specification (Doc 2: SRS)

**Objective:** Test suite creation and `/doc-plan` command

**Steps:**
1. Create documentation suite `enhanced-adws-docs`
2. Run `/doc-plan` for Software Requirements Specification
3. Validate spec structure and completeness
4. Record spec path for Phase 2

**Expected Outputs:**
- `.claude/docs/suites/enhanced-adws-docs/manifest.json`
- `specs/docs/enhanced-adws-docs/02-srs-spec.md`

**Validation Criteria:**
- [ ] Suite manifest created with correct structure
- [ ] Spec contains all required sections
- [ ] Document type is `design`
- [ ] Source references include Doc 1 (User Stories)

---

### Phase 2: Document Generation (Doc 2: SRS)

**Objective:** Test `/doc-write` command and writer agent

**Steps:**
1. Run `/doc-write` on the SRS spec
2. Validate output document structure
3. Check for forbidden patterns (TODO, TBD, etc.)
4. Record quality observations

**Expected Outputs:**
- `design_documents/final/02_software_requirements_specification.md`

**Validation Criteria:**
- [ ] Document follows design template structure
- [ ] No placeholder content
- [ ] All sections populated
- [ ] Cross-references to User Stories (Doc 1)

---

### Phase 3: Review Workflow (Doc 3: Architecture Blueprint)

**Objective:** Test `/doc-plan`, `/doc-write`, and `/doc-review` in sequence

**Steps:**
1. Run `/doc-plan` for Architecture Blueprint
2. Run `/doc-write` to generate document
3. Run `/doc-review` to validate quality
4. Document quality score and issues

**Expected Outputs:**
- `specs/docs/enhanced-adws-docs/03-architecture-spec.md`
- `design_documents/final/03_architecture_blueprint.md`
- Review report with quality score

**Validation Criteria:**
- [ ] Complete sequential workflow executes
- [ ] Quality score calculated (0-100)
- [ ] Issues classified by severity (blocker/warning/suggestion)
- [ ] Architecture diagrams included (Mermaid)

---

### Phase 4: Batch Operations and Dependencies (Doc 4, 5, 6)

**Objective:** Test `/doc-batch generate`, dependencies, and parallel execution

**Steps:**
1. Run `/doc-plan` for remaining design docs (4, 5, 6)
2. Configure dependencies in manifest:
   - Doc 4 (SDD) depends on Doc 3 (Architecture)
   - Doc 5 (Test Plan) depends on Doc 2 (SRS)
   - Doc 6 (Build Instructions) depends on Doc 4 (SDD)
3. Run `/doc-batch enhanced-adws-docs generate --parallel`
4. Verify dependency order respected
5. Run `/doc-review --fix` on any failing documents

**Expected Outputs:**
- 3 new spec files
- 3 new document files
- Batch execution report

**Validation Criteria:**
- [ ] Dependencies resolved correctly
- [ ] Parallel execution where allowed
- [ ] Manifest updated after each completion
- [ ] Auto-fix resolves terminology issues

---

### Phase 5: Synchronization and Consistency (Full Suite)

**Objective:** Test `/doc-sync`, `/doc-batch review`, and cross-references

**Steps:**
1. Run `/doc-batch enhanced-adws-docs review`
2. Run `/doc-sync enhanced-adws-docs --fix`
3. Run `/doc-status enhanced-adws-docs`
4. Document suite health score

**Expected Outputs:**
- Batch review report
- Sync report with violations found/fixed
- Status dashboard output

**Validation Criteria:**
- [ ] All documents reviewed
- [ ] Terminology synchronized across suite
- [ ] Cross-references validated
- [ ] Suite health score calculated
- [ ] Dashboard shows completion status

---

### Phase 6: Final Document and Learning (Doc 7: CONTRIBUTING.md)

**Objective:** Test full cycle with `/doc-improve` pattern learning

**Steps:**
1. Run `/doc-plan` for CONTRIBUTING.md with `--type manual`
2. Run `/doc-write` to generate
3. Run `/doc-review` to validate
4. Run `/doc-improve` to extract patterns
5. Run final `/doc-status` for complete dashboard

**Expected Outputs:**
- `specs/docs/enhanced-adws-docs/07-contributing-spec.md`
- `design_documents/final/07_CONTRIBUTING.md`
- Updated patterns.json (if patterns extracted)
- Final suite status report

**Validation Criteria:**
- [ ] Manual template used correctly
- [ ] Document passes quality gates
- [ ] `/doc-improve` identifies patterns from successful docs
- [ ] Suite shows 100% completion (6/6 docs)

---

## State Tracking for Context Management

### Progress File Location
`/Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/test_progress.json`

### Progress Structure
```json
{
  "test_plan_version": "1.0",
  "current_phase": 1,
  "last_checkpoint": "2025-12-02T00:00:00Z",
  "documents": {
    "02_srs": {"spec": "pending", "doc": "pending", "review": "pending"},
    "03_architecture": {"spec": "pending", "doc": "pending", "review": "pending"},
    "04_sdd": {"spec": "pending", "doc": "pending", "review": "pending"},
    "05_test_plan": {"spec": "pending", "doc": "pending", "review": "pending"},
    "06_build_instructions": {"spec": "pending", "doc": "pending", "review": "pending"},
    "07_contributing": {"spec": "pending", "doc": "pending", "review": "pending"}
  },
  "suite_created": false,
  "batch_tests_completed": [],
  "sync_completed": false,
  "improve_completed": false,
  "notes": []
}
```

### Resume Instructions (If Context Exhausted)

If starting a new context window:

1. **Read state:**
   ```
   Read /Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/test_progress.json
   Read /Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/SPEC_DRIVEN_TEST_PLAN.md
   ```

2. **Check git status:**
   ```
   cd /Users/etherealogic/Dev/enhanced-adws-v1.0 && git status && git log --oneline -5
   ```

3. **Verify suite state:**
   ```
   /doc-status enhanced-adws-docs
   ```

4. **Resume from current_phase in progress file**

---

## Success Criteria

### Minimum Success (Test Plan Valid)
- [ ] All 7 commands executed at least once
- [ ] All 4 agents invoked
- [ ] 6 documents generated
- [ ] Suite operations functional

### Full Success (System Production-Ready)
- [ ] All documents pass quality gates (Grade B or higher)
- [ ] Batch operations complete without manual intervention
- [ ] Cross-references validated across suite
- [ ] Pattern learning extracts at least 2 new patterns
- [ ] Suite health score >= 80%

### Test Failures to Document
- Commands that fail or timeout
- Quality gate false positives/negatives
- Agent errors or unexpected behavior
- Suite sync issues

---

## Execution Order Summary

```
Phase 1: Setup
├── Create suite manifest
└── /doc-plan Doc 2 (SRS)

Phase 2: Basic Generation
└── /doc-write Doc 2 (SRS)

Phase 3: Review Workflow
├── /doc-plan Doc 3 (Architecture)
├── /doc-write Doc 3
└── /doc-review Doc 3

Phase 4: Batch Operations
├── /doc-plan Doc 4, 5, 6
├── Configure dependencies
├── /doc-batch generate --parallel
└── /doc-review --fix (as needed)

Phase 5: Synchronization
├── /doc-batch review
├── /doc-sync --fix
└── /doc-status

Phase 6: Final + Learning
├── /doc-plan Doc 7 (CONTRIBUTING)
├── /doc-write Doc 7
├── /doc-review Doc 7
├── /doc-improve
└── Final /doc-status
```

---

## Reference Paths

| Resource | Path |
|----------|------|
| Spec-Driven System | `/Users/etherealogic/Dev/spec-driven-docs-system/` |
| Enhanced ADWS Project | `/Users/etherealogic/Dev/enhanced-adws-v1.0/` |
| Design Documents | `/Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/` |
| Manual Prompts | `/Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/prompts/` |
| Test Progress | `/Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/test_progress.json` |
| Suite Manifest | `.claude/docs/suites/enhanced-adws-docs/manifest.json` |

---

## Dependencies on Document 1

All generated documents will reference the manually-created Document 1 (User Stories & Acceptance Criteria). The test plan assumes this document exists at:

`/Users/etherealogic/Dev/enhanced-adws-v1.0/design_documents/final/01_user_stories_acceptance_criteria.md`

If Document 1 is not yet complete, Phase 1 should wait until it is available, OR specifications should note the dependency as "pending external document."

---

*Test Plan Version: 1.0*
*Created: 2025-12-02*
*System Under Test: Spec-Driven Technical Document Creation System*
