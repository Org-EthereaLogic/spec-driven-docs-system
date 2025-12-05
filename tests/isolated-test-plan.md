# Isolated Installation Test Plan

**Version:** 1.0
**Created:** 2025-12-04
**Purpose:** Validate spec-driven-docs-system in a clean environment simulating real-world installation

---

## 1. Overview

### 1.1 Goals

This test plan validates the spec-driven-docs-system by:

1. **Simulating real installation** - Copy framework files to isolated test project
2. **Using relative paths only** - No hardcoded absolute paths
3. **Self-contained testing** - All source materials within test project
4. **Validating portability** - Test would work on any machine

### 1.2 Key Differences from Previous Approach

| Aspect | Previous (Integration) | New (Isolated) |
|--------|----------------------|----------------|
| Environment | Run from repo, point to external project | Run from isolated test project |
| Paths | Hardcoded absolute paths | Relative paths only |
| Source files | External repository | Copied into test project |
| Portability | Only works on one machine | Works on any machine |
| Scope | Integration testing | Installation + Unit testing |

---

## 2. Test Environment Setup

### 2.1 Directory Structure

```
/tmp/spec-docs-test/                 # Isolated test root
├── .claude/                         # Copied from framework
│   ├── agents/
│   ├── commands/
│   ├── docs/
│   │   ├── config/
│   │   ├── expertise/
│   │   ├── suites/
│   │   │   └── _example/
│   │   └── templates/
│   └── hooks/
├── specs/                           # Copied from framework
│   └── docs/
│       └── _example/
├── docs/                            # Generated output (created during test)
├── source/                          # Test source materials (self-contained)
│   ├── api-spec.md                  # Sample API specification
│   ├── design-spec.md               # Sample design specification
│   └── user-guide-spec.md           # Sample user guide specification
└── test_progress.json               # Test execution log
```

### 2.2 Setup Script

```bash
#!/bin/bash
# setup-isolated-test.sh

TEST_ROOT="/tmp/spec-docs-test"
FRAMEWORK_ROOT="$(pwd)"  # Run from spec-driven-docs-system repo

# Clean previous test
rm -rf "$TEST_ROOT"
mkdir -p "$TEST_ROOT"

# Copy framework files (simulating real installation)
cp -r "$FRAMEWORK_ROOT/.claude" "$TEST_ROOT/"
cp -r "$FRAMEWORK_ROOT/specs" "$TEST_ROOT/"

# Create source materials directory
mkdir -p "$TEST_ROOT/source"
mkdir -p "$TEST_ROOT/docs"

# Copy test source materials (see Section 3)
# These are self-contained and use relative paths

echo "Test environment ready at: $TEST_ROOT"
echo "Run tests with: cd $TEST_ROOT && claude"
```

---

## 3. Test Source Materials

### 3.1 Sample API Specification (`source/api-spec.md`)

A self-contained API specification for a fictional "Task Manager API":

- 5 endpoints (CRUD + list)
- Authentication section
- Error handling documentation
- Request/response examples

**Purpose:** Tests API documentation template and patterns.

### 3.2 Sample Design Specification (`source/design-spec.md`)

A self-contained system design for "Task Manager Backend":

- Problem statement
- Proposed solution
- Architecture overview (with Mermaid diagrams)
- Alternatives considered
- Implementation plan

**Purpose:** Tests design documentation template, ADR format, diagrams.

### 3.3 Sample User Guide Specification (`source/user-guide-spec.md`)

A self-contained user manual for "Task Manager CLI":

- Getting started
- Core concepts
- How-to guides
- Troubleshooting

**Purpose:** Tests user manual template, progressive disclosure pattern.

---

## 4. Test Phases

### Phase 1: Installation Validation

**Objective:** Verify framework files are properly installed and accessible.

| Step | Command/Action | Expected Result |
|------|---------------|-----------------|
| 1.1 | `ls -la .claude/` | All directories present |
| 1.2 | `ls -la specs/docs/` | _example template present |
| 1.3 | `/doc-status` | Shows empty suite status (no active suites) |

**Pass Criteria:**
- [ ] All framework directories present
- [ ] Config files readable
- [ ] Templates accessible
- [ ] /doc-status runs without error

### Phase 2: Suite Creation

**Objective:** Create a test suite with relative paths only.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 2.1 | `/doc-plan "Task Manager API Reference" --type api --suite task-manager --output specs/docs/task-manager/api-spec.md` | Spec created with relative paths |
| 2.2 | Verify manifest | All paths relative, no absolute paths |
| 2.3 | `/doc-status task-manager` | Shows 1 document pending |

**Manifest Validation Checklist:**
- [ ] `spec_path` uses relative path (no `/Users/...`)
- [ ] `output_path` uses relative path (e.g., `docs/api/reference.md`)
- [ ] No hardcoded machine-specific paths
- [ ] External dependencies (if any) are within project

### Phase 3: Document Generation

**Objective:** Generate documents using self-contained source materials.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 3.1 | `/doc-write specs/docs/task-manager/api-spec.md` | API doc generated to `docs/` |
| 3.2 | Verify output | Document exists, no placeholders |
| 3.3 | `/doc-plan "Task Manager Backend Design" --type design --suite task-manager` | Design spec created |
| 3.4 | `/doc-write specs/docs/task-manager/design-spec.md` | Design doc generated |

**Quality Validation:**
- [ ] All documents generated without errors
- [ ] No TODO/FIXME/TBD markers
- [ ] Code examples syntactically valid
- [ ] Mermaid diagrams render correctly

### Phase 4: Document Review

**Objective:** Validate quality gates and review process.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 4.1 | `/doc-review docs/api/reference.md --spec specs/docs/task-manager/api-spec.md` | Review completes with score |
| 4.2 | If issues, `/doc-review ... --fix` | Auto-fix applied |
| 4.3 | Repeat for design doc | All docs pass review |

**Review Validation:**
- [ ] Quality gates execute correctly
- [ ] Scores calculated accurately
- [ ] Issues identified with locations
- [ ] Auto-fix works for fixable issues

### Phase 5: Batch Operations

**Objective:** Test batch processing capabilities.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 5.1 | Add user manual to suite | Third document added |
| 5.2 | `/doc-batch task-manager generate --parallel` | All docs generated |
| 5.3 | `/doc-batch task-manager review` | All docs reviewed |

**Batch Validation:**
- [ ] Parallel generation works
- [ ] Dependency ordering respected
- [ ] Continue-on-error functions correctly
- [ ] Summary statistics accurate

### Phase 6: Synchronization

**Objective:** Test cross-document consistency.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 6.1 | `/doc-sync task-manager` | Consistency report generated |
| 6.2 | `/doc-sync task-manager --fix` | Auto-fixes applied |

**Sync Validation:**
- [ ] Terminology consistency checked
- [ ] Cross-references validated
- [ ] Style consistency enforced
- [ ] Health score calculated

### Phase 7: Pattern Learning

**Objective:** Test expertise extraction.

| Step | Command | Expected Result |
|------|---------|-----------------|
| 7.1 | `/doc-improve` | Patterns extracted from successful docs |
| 7.2 | Verify expertise files | New patterns added |

**Learning Validation:**
- [ ] Good patterns identified
- [ ] Anti-patterns detected (if any)
- [ ] Usage counts updated
- [ ] Expertise version incremented

---

## 5. Portability Test

### 5.1 Relocation Test

After completing all phases:

```bash
# Move entire test directory to new location
mv /tmp/spec-docs-test /tmp/relocated-test

# Re-run status command
cd /tmp/relocated-test
# /doc-status task-manager
```

**Pass Criteria:**
- [ ] All commands work from new location
- [ ] No broken path references
- [ ] Documents still accessible
- [ ] Suite status correct

### 5.2 Clean Machine Simulation

```bash
# Export test project (excluding .DS_Store, etc.)
tar -czf test-project.tar.gz -C /tmp spec-docs-test

# Extract to different path
mkdir /tmp/fresh-install
tar -xzf test-project.tar.gz -C /tmp/fresh-install

# Verify functionality
cd /tmp/fresh-install/spec-docs-test
# /doc-status
```

**Pass Criteria:**
- [ ] Project functions after archive/extract
- [ ] No missing dependencies
- [ ] All relative paths resolve

---

## 6. Test Data Requirements

### 6.1 Self-Contained Source Materials

Create these files in `source/` directory:

**api-spec.md** (~200 lines):
- REST API specification
- 5 endpoints with full details
- Auth requirements
- Error codes

**design-spec.md** (~300 lines):
- System architecture
- Component descriptions
- Data flow diagrams
- Technology decisions

**user-guide-spec.md** (~150 lines):
- Installation steps
- Basic usage
- Common tasks
- FAQ/Troubleshooting

### 6.2 Expected Outputs

| Document | Type | Est. Lines | Location |
|----------|------|------------|----------|
| API Reference | api | 400-600 | docs/api/reference.md |
| Backend Design | design | 800-1200 | docs/design/backend.md |
| CLI User Guide | manual | 300-500 | docs/guides/cli.md |

---

## 7. Success Criteria

### 7.1 Functional Requirements

- [ ] All 7 slash commands execute without error
- [ ] All 4 agent types spawn correctly
- [ ] All 4 quality gates function
- [ ] All 3 document templates work

### 7.2 Path Portability

- [ ] Zero absolute paths in manifest files
- [ ] Zero hardcoded machine-specific references
- [ ] Project works after relocation
- [ ] Project works after archive/extract

### 7.3 Quality Metrics

- [ ] All generated documents score >= 80 (B grade)
- [ ] Zero blocker issues in final reviews
- [ ] All auto-fix operations succeed
- [ ] Sync health score >= 90

### 7.4 Documentation

- [ ] Test progress log complete
- [ ] All issues documented with root cause
- [ ] Corrections tracked with before/after
- [ ] Patterns learned recorded

---

## 8. Execution Instructions

### 8.1 Prerequisites

- Claude Code CLI installed
- Access to spec-driven-docs-system repository
- Write access to /tmp or alternative test location

### 8.2 Running the Test

```bash
# 1. Navigate to framework repo
cd /path/to/spec-driven-docs-system

# 2. Run setup script
./tests/setup-isolated-test.sh

# 3. Change to test directory
cd /tmp/spec-docs-test

# 4. Start Claude Code
claude

# 5. Execute test phases sequentially
# Follow Phase 1-7 steps above
```

### 8.3 Recording Results

Update `test_progress.json` after each phase with:
- Commands executed
- Issues encountered
- Corrections applied
- Scores achieved

---

## 9. Comparison with Integration Testing

| Metric | Integration Test | Isolated Test |
|--------|-----------------|---------------|
| Environment | Existing repo | Clean install |
| Source data | External project | Self-contained |
| Path validation | Not tested | Primary focus |
| Portability | Fails | Must pass |
| Reproducibility | Low | High |
| Real-world simulation | Low | High |

---

## 10. Post-Test Actions

### 10.1 On Success

1. Archive test results to `tests/archives/`
2. Update framework documentation if gaps found
3. Add any new patterns to expertise files
4. Create issue for any improvements identified

### 10.2 On Failure

1. Document failure with full context
2. Identify root cause (framework vs. test setup)
3. Create fix and re-run specific phase
4. Do not proceed until phase passes

---

## Appendix A: Quick Reference

### Slash Commands Tested

| Command | Phase | Purpose |
|---------|-------|---------|
| `/doc-status` | 1, 2, 7 | Suite status |
| `/doc-plan` | 2, 3 | Create specifications |
| `/doc-write` | 3, 5 | Generate documents |
| `/doc-review` | 4 | Quality validation |
| `/doc-batch` | 5 | Batch operations |
| `/doc-sync` | 6 | Consistency checks |
| `/doc-improve` | 7 | Pattern learning |

### Agent Types Tested

| Agent | Model | Phase |
|-------|-------|-------|
| doc-orchestrator | opus | 2 |
| doc-writer | sonnet | 3, 5 |
| doc-reviewer | sonnet | 4, 5 |
| doc-librarian | haiku | 6 |

---

*Test Plan Version 1.0 - Created 2025-12-04*
