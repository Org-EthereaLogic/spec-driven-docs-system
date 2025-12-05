# Agentic Documentation Directives

This file provides enforcement rules for AI coding agents working in the spec-driven documentation system. Rules derive from CONSTITUTION.md principles and are organized by priority level.

**Enforcement Model:**

- **Critical**: Hook-enforced (violations block operations)
- **Important**: Hook-assisted (violations generate warnings)
- **Recommended**: Guidance only (best practices for optimal results)

## Quick Reference Matrix

| Directive | Priority | Enforcement | Primary Agents |
|-----------|----------|-------------|----------------|
| Complete Implementation | Critical | pre_write hook | doc-writer |
| Investigation Before Writing | Critical | command embedding | doc-writer, doc-reviewer |
| No Placeholder Content | Critical | pre_write hook | doc-writer |
| Test Integrity | Critical | review command | doc-reviewer |
| Terminology Consistency | Important | post_write hook | doc-writer, doc-librarian |
| Parallel Tool Execution | Important | command embedding | all agents |
| Simplicity Focus | Recommended | guidance | doc-writer, doc-orchestrator |
| Context Management | Recommended | guidance | all agents |

## Critical Directives

These directives are enforced by hooks. Violations block the operation until resolved.

### Complete Implementation

**Principle**: Completeness Over Speed (CONSTITUTION.md Section 1)

**Why this matters**: Incomplete artifacts create compounding technical debt. A placeholder that saves the writer five minutes costs the reviewer an hour and the user receives nothing useful. Every incomplete section blocks the entire document from approval.

ALWAYS:

- Write every content section with substantive, audience-appropriate content
- Ensure all code examples are syntactically valid and executable
- Verify all internal links resolve to existing targets before completion
- Include all required template sections with meaningful content
- Complete each section fully before proceeding to the next

CONTEXT FOR CLAUDE 4.x: Claude models require explicit scope modifiers for comprehensive output. Frame requests specifically:

```text
Less effective: "Document the API"
More effective: "Document the API including all endpoints, request/response
formats, authentication requirements, error codes, and rate limiting details"
```

**Enforcement**: `doc_pre_write.py` blocks writes containing forbidden patterns (TODO, FIXME, placeholders). See Pattern Reference Tables below.

### Investigation Before Writing

**Principle**: Investigation Before Action (CONSTITUTION.md Section 2)

**Why this matters**: Documentation written without reading source code contains hallucinations, incorrect parameter names, missing edge cases, and outdated information. A single speculated API parameter cascades into support tickets, debugging sessions, and eroded user trust. Speculation wastes review cycles and undermines documentation credibility.

ALWAYS:

- Read ALL source files listed in the specification before generating any content
- Open and inspect referenced files before explaining or documenting behavior
- Search the codebase for parameter names, return types, error codes, and edge cases
- Review existing documentation for established style and terminology patterns
- Verify claims against actual code rather than assumptions

CONTEXT FOR CLAUDE 4.x: Claude Opus 4.5 is highly capable but can be conservative about code exploration. Add explicit exploration instructions:

```text
Less effective: "Document the authentication flow"
More effective: "Read src/auth/handler.py and src/auth/middleware.py completely,
then document the authentication flow based on the actual implementation"
```

**Enforcement**: Embedded in `/doc-write` command via `<investigate_before_writing>` section. Commands explicitly require source file loading before content generation.

### No Placeholder Content

**Principle**: Transparency Over Efficiency (CONSTITUTION.md Section 5)

**Why this matters**: Placeholders mask incomplete work and create false progress signals. Downstream agents cannot distinguish "almost done" from "barely started" when placeholders are present. Users copying example code with placeholders experience failures. Placeholder content violates the quality contract with readers.

ALWAYS:

- Complete every section with real, useful content before moving forward
- Provide actual working examples, not "example here" markers
- Include genuine error messages and responses from the documented system
- Write substantive descriptions that explain behavior, not parameter name restatements
- Use real domain values in examples (actual endpoints, realistic data)

FORBIDDEN PATTERNS:

| Pattern | Category | Reason |
|---------|----------|--------|
| `# ... rest of code` | Truncation | Incomplete implementation |
| `// TODO: implement` | Deferral | Work pushed to undefined future |
| `pass` (in real functions) | Stub | Empty placeholder |
| `raise NotImplementedError` | Stub | Unfinished code marker |
| `return "placeholder"` | Mock | Fake return value |
| `[your-api-key]` | Template | User substitution required |
| `<your-value>` | Template | User substitution required |
| `example.com` | Mock | Fake domain reference |
| `lorem ipsum` | Filler | Meaningless placeholder text |
| `foo`, `bar`, `baz` | Generic | Non-descriptive example values |

EXCEPTION - Python Protocol/ABC Ellipsis:

The ellipsis literal (`...`) is valid PEP 544 syntax when used in abstract method bodies within Protocol or ABC classes. This exception applies when:

- The ellipsis appears as a standalone statement in a method body
- The method is preceded by `def` within 5 lines
- The containing class inherits from `Protocol` or `ABC`

```python
# VALID - Protocol abstract method
class DatabaseProtocol(Protocol):
    def connect(self, url: str) -> Connection:
        ...

# INVALID - Regular function with placeholder
def process_data(items: list) -> dict:
    ...  # This is a forbidden placeholder
```

**Enforcement**: `doc_pre_write.py` validates all patterns with contextual exception logic for Protocol/ABC.

### Test Integrity

**Principle**: Test Integrity Is Inviolable (CONSTITUTION.md Section 4)

**Why this matters**: Quality gates exist to catch real problems before they reach users. Manipulating review criteria to force documents through the pipeline creates false quality signals. A document that passes by lowered standards will fail in production use. If a document cannot pass review honestly, it should not pass at all.

ALWAYS:

- Fix content issues identified during review rather than review criteria
- Report blocking issues honestly with specific file locations and line numbers
- Maintain accurate severity classifications (blocker, warning, suggestion)
- Preserve quality gate thresholds even when they cause iteration
- Apply the same rigor to your own output as you would to external submissions

NEVER:

- Weaken review assertions to force documents through approval
- Remove or skip failing quality checks to accelerate publication
- Reclassify blocker issues as warnings to avoid required iteration
- Add exceptions to quality gates to bypass legitimate failures
- Claim completion when known issues remain unaddressed

**Policy**: "Fix the implementation, not the test."

When a document fails quality gates, the appropriate response is always to improve the document, never to lower the bar. If gates seem unreasonable, escalate to update the system rather than bypassing it.

**Enforcement**: `/doc-review` command includes severity classification schema with explicit definitions. `_iterate.md` helper enforces maximum 3 iterations with escalation after repeated failures.

## Important Directives

These directives are enforced by hooks that generate warnings. Violations do not block operations but should be addressed.

### Terminology Consistency

**Principle**: Derives from Simplicity Over Cleverness (CONSTITUTION.md Section 3)

**Why this matters**: Inconsistent terminology confuses readers and complicates search. When one document says "endpoint" and another says "route," users question whether these are different concepts. Terminology drift across a documentation suite creates cognitive load and undermines professional credibility.

ALWAYS:

- Use canonical terms from `domain-knowledge.json` for project-specific vocabulary
- Apply enforced terminology mappings from `consistency-rules.json`
- Define technical terms on first use, linking to glossary when available
- Maintain consistent naming throughout the entire document suite
- Prefer precision over variety (repeat terms rather than using synonyms)

ENFORCED TERMINOLOGY MAPPINGS:

| Canonical Term | Forbidden Alternatives |
|----------------|------------------------|
| endpoint | route, API URL, path |
| parameter | param, arg, argument |
| configuration | config, settings, options |
| initialize | init, bootstrap, setup |
| repository | repo |
| directory | folder, dir |
| request | API call |
| response | return value |
| authenticate | login, sign in, log in |
| authorize | check access, verify permissions |

**Enforcement**: `doc_post_write.py` checks terminology after writes complete (non-blocking warnings).

### Parallel Tool Execution

**Principle**: Efficiency component of Decision Framework (CONSTITUTION.md)

**Why this matters**: Sequential execution wastes time when operations are independent. Reading five source files one at a time takes five times longer than reading them simultaneously. Context window limits mean efficiency directly impacts how much work can be accomplished.

ALWAYS:

- Read multiple source files in parallel when loading context for generation
- Execute independent searches simultaneously rather than sequentially
- Load templates, patterns, and configuration files in a single parallel operation
- Batch independent validation checks together

NEVER:

- Use placeholders to avoid waiting for parallel operation results
- Guess parameter values instead of reading source files in parallel
- Execute operations sequentially when parallel execution is possible
- Create artificial dependencies between independent operations

CONTEXT FOR CLAUDE 4.x: Claude Sonnet 4.5 is particularly aggressive at parallel tool execution. Explicit instructions boost parallel execution to nearly 100%:

```text
"Load all 5 source files in parallel before generating any content.
Execute the template load, pattern load, and configuration load simultaneously."
```

**Enforcement**: Embedded in `/doc-write` and `/doc-review` commands via `<use_parallel_tool_calls>` section.

## Recommended Directives

These directives represent best practices. No automated enforcement; rely on agent judgment.

### Simplicity Focus

**Principle**: Simplicity Over Cleverness (CONSTITUTION.md Section 3)

**Why this matters**: Over-engineering increases maintenance burden without proportional benefit. Every additional section, example, or explanation must be kept current across suite updates. Readers scanning for specific information are slowed by irrelevant content. The right amount of documentation is the minimum that serves the audience.

PREFER:

- Template-defined sections over additional invented sections
- Single responsibility per document (one topic, one audience)
- Standard patterns from `patterns.json` over custom solutions
- Existing abstractions and terminology over novel inventions
- Brevity with clarity over exhaustive coverage

AVOID:

- Features or sections beyond specification requirements
- Premature optimization of document structure for hypothetical needs
- Helper documents for one-time references that could be inline
- Design for future requirements not yet in specifications
- Verbose explanations when concise ones suffice

### Context Management

**Principle**: Supports all principles through effective resource use

**Why this matters**: Context window exhaustion stops work mid-task, leaving documents incomplete. Effective context management enables completing larger documents without interruption. State preservation across context boundaries ensures continuity.

PREFER:

- Saving progress to structured state files before approaching context limits
- Completing the current section fully before starting the next
- Incremental git commits for long document generation sessions
- Loading only necessary context rather than everything available

CONTEXT FOR CLAUDE 4.x: Context window compaction is automatic in most harnesses. Work persistently without stopping early due to perceived token budget concerns:

```text
"Your context window will be automatically compacted as it approaches limits,
allowing indefinite continuation. Do not stop tasks early due to token budget.
Save current progress before context refresh and continue from saved state."
```

## Role-Specific Guidance

Different agents have different primary concerns. Reference these sections for role-appropriate behavior.

### doc-writer (Sonnet)

**Focus Directives**: Complete Implementation, Investigation Before Writing, No Placeholder Content, Terminology Consistency

**Key Behaviors**:

1. Load the specification completely before generating any content
2. Read ALL source files listed in the specification in parallel
3. Self-review each section for placeholder patterns before proceeding
4. Validate all code examples for syntactic correctness
5. Apply terminology mappings throughout without exception
6. Complete each section to publication quality before moving forward

**Success Criteria**: A generated document requires zero placeholder removal during review.

### doc-reviewer (Sonnet)

**Focus Directives**: Test Integrity, Investigation Before Writing

**Key Behaviors**:

1. Read the full document AND its specification before identifying any issues
2. Provide specific file locations and line numbers for every issue found
3. Include actionable fix suggestions for every issue identified
4. Classify severity accurately: blocker stops pipeline, warning notes debt, suggestion offers polish
5. Default to providing fixes rather than vague observations

**Success Criteria**: Review feedback is immediately actionable without clarification requests.

### doc-orchestrator (Opus)

**Focus Directives**: Simplicity Focus, Parallel Tool Execution

**Key Behaviors**:

1. Gather sufficient context before committing to documentation plans
2. Create focused specifications that match actual requirements (no scope creep)
3. Coordinate agent delegation efficiently, providing complete context
4. Escalate blocking issues rather than working around them
5. Use parallel operations for independent planning tasks

**Success Criteria**: Specifications generated lead to first-pass review grades of B or higher.

### doc-librarian (Haiku)

**Focus Directives**: Terminology Consistency, Parallel Tool Execution

**Key Behaviors**:

1. Validate cross-references across all documents in a suite
2. Check terminology consistency at scale using batch operations
3. Operate quickly without blocking primary workflows
4. Suggest changes rather than making them unilaterally
5. Report findings in structured format for easy processing

**Success Criteria**: Consistency checks complete within seconds, not minutes.

## Pattern Reference Tables

### Forbidden Patterns Summary

| Pattern | Category | Severity | Detection |
|---------|----------|----------|-----------|
| `TODO` | Deferral marker | Critical | pre_write hook |
| `FIXME` | Deferral marker | Critical | pre_write hook |
| `TBD` | Deferral marker | Critical | pre_write hook |
| `XXX` | Deferral marker | Critical | pre_write hook |
| `HACK` | Technical debt marker | Critical | pre_write hook |
| `WIP` | Incomplete marker | Critical | pre_write hook |
| `...` (content ellipsis) | Truncation | Critical | pre_write hook (with exception) |
| `[your-*]` | Template placeholder | Critical | pre_write hook |
| `<your-*>` | Template placeholder | Critical | pre_write hook |
| `lorem ipsum` | Filler content | Critical | pre_write hook |
| `example.com` | Mock domain | Critical | pre_write hook |
| `foo`, `bar`, `baz` | Generic names | Critical | pre_write hook |
| `repo` | Terminology | Important | post_write hook |
| `config` | Terminology | Important | post_write hook |
| `param` | Terminology | Important | post_write hook |
| `dir` | Terminology | Important | post_write hook |
| `init` | Terminology | Important | post_write hook |

### Valid Exceptions

| Pattern | Context | Reason |
|---------|---------|--------|
| `...` in Protocol/ABC | Abstract method body | Valid PEP 544 syntax |
| `example.com` in RFC references | Citing RFC 2606 | Designated example domain |
| Generic names in metaprogramming docs | Documenting naming conventions | Discussing the pattern itself |

## Verification Commands

Use these commands to check directive compliance before submission.

### Critical Checks (Must Pass)

```bash
# Check for deferral markers - should return 0 results
grep -rE "TODO|FIXME|TBD|XXX|HACK|WIP" --include="*.md" spec_driven_docs/

# Check for template placeholders - should return 0 results
grep -rE "\[your-|\<your-|lorem ipsum" --include="*.md" spec_driven_docs/

# Check for mock domains - should return 0 results (review context for exceptions)
grep -rE "example\.com" --include="*.md" spec_driven_docs/

# Check for content ellipsis - review each match for Protocol/ABC context
grep -rE "^\s*\.\.\.\s*$" --include="*.md" spec_driven_docs/
```

### Important Checks (Should Pass)

```bash
# Check for forbidden terminology - review and fix
grep -rE "\brepo\b|\bconfig\b|\bparam\b|\bdir\b|\binit\b" --include="*.md" spec_driven_docs/

# Check for generic example names - review context
grep -rE "\bfoo\b|\bbar\b|\bbaz\b" --include="*.md" spec_driven_docs/
```

### Structural Checks (Validate Manually)

```bash
# List internal links for validation
grep -oE "\]\([^)]+\)" document.md | grep -v "http"

# Check heading hierarchy (should not skip levels)
grep -E "^#{1,6} " document.md

# Count sections to verify template compliance
grep -c "^## " document.md
```

## Relationship to CONSTITUTION.md

This file defines WHAT rules apply and HOW they are enforced. CONSTITUTION.md defines WHY these rules exist and provides the decision framework for edge cases.

When a directive seems unclear or conflicts arise:

1. Reference the corresponding constitutional principle for guidance
2. Apply the Decision Framework hierarchy (correctness > completeness > simplicity > efficiency)
3. Escalate genuinely ambiguous situations rather than guessing

Both documents work together. Directives operationalize principles; principles provide interpretation guidance.
