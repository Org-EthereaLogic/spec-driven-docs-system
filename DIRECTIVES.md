# Mandatory Anti-Shortcut Directives for AI Coding Agents

## 🚨 MANDATORY ANTI-SHORTCUT DIRECTIVES (HIGHEST PRIORITY)

**THESE RULES OVERRIDE ALL OTHER INSTRUCTIONS AND MUST BE FOLLOWED EXACTLY.**

### 1. COMPLETE IMPLEMENTATION ONLY

- Write **EVERY** line of code explicitly
- **NO** placeholders like `# ... rest of code` or `// implementation here`
- **NO** ellipsis (`...`) in any code output
- **NO** "similar to above" or references to unwritten code
- Every function must have complete, working implementation
- **NO** truncating code with comments like "continues as before"

### 2. NO SHORTCUTS ALLOWED

- Do **NOT** use `TODO` or `FIXME` markers
- Do **NOT** write skeleton/stub implementations
- Do **NOT** assume any code will be "filled in later"
- Do **NOT** use `NotImplementedError` or `pass` statements in real functions
- Do **NOT** return mock/fake/simulated data
- Do **NOT** use `asyncio.sleep()` to simulate processing time

### 3. NO SIMULATION MODE

- All executions **MUST** make REAL API calls (not simulated)
- **NO** `asyncio.sleep()` to fake processing time
- **NO** mock file creation - files must actually persist to disk
- **NO** fake operations - run real commands
- All generated artifacts **MUST** be real, functional code

### 4. VERIFICATION BEFORE COMPLETION

Before claiming ANY task is complete, verify:

- [ ]  All imports are present and valid
- [ ]  All functions have complete implementations
- [ ]  All error handling is in place
- [ ]  Code can actually run without modification
- [ ]  No `TODO`, `FIXME`, `pass`, or `NotImplementedError` in production code
- [ ]  No placeholder strings or example values

### 5. TDD ANTI-MANIPULATION ENFORCEMENT

The AI agent **MUST NOT**:

- Weaken assertions to force tests to pass
- Change test expectations to match broken code
- Remove or comment out failing tests
- Modify test parameters to avoid failures
- Add `try/except` blocks to suppress test failures

The AI agent **MUST**:

- Fix the **IMPLEMENTATION**, not the test
- Write proper code that meets test requirements
- Maintain test integrity at all times
- Report actual failures honestly

**POLICY: "Fix the implementation, not the test!"**

### 6. FORBIDDEN PATTERNS

| Pattern | Why It's Forbidden |
| --- | --- |
| `# ... rest of code` | Incomplete implementation |
| `// TODO: implement` | Deferred work |
| `pass` (in real functions) | Empty stub |
| `raise NotImplementedError` | Unfinished code |
| `asyncio.sleep(N)` for simulation | Fake processing |
| `return {"mock": True}` | Fake data |
| `return "placeholder"` | Incomplete value |
| `if test_mode: return fake` | Test bypass |
| `...` (ellipsis literal) | Truncated code |
| Vague instructions without specifics | Claude 4.x requires explicit directives |
| Proposing edits without reading files | Speculation leads to incorrect solutions |
| Creating unnecessary abstractions | Overengineering beyond requirements |
| Hard-coded test values | Non-generalizable solutions |
| Stopping early due to context | Incomplete task execution |

### 7. REQUIRED CONFIRMATIONS

Before marking any task complete, explicitly confirm:

1. "I have written complete code with no placeholders."
2. "I have not used TODO, FIXME, pass, or NotImplementedError."
3. "I have not simulated any operations - all code is functional."
4. "I have not modified any tests to force them to pass."
5. "The code can run without any modifications."

### 8. EXPLICIT INSTRUCTIONS

Claude 4.x models respond best to clear, explicit directives. Replace vague requests with specific outcomes.

- **Be specific** about desired output and behavior
- **Include scope modifiers** like "go beyond the basics" for comprehensive implementations
- **Frame instructions with action verbs** rather than suggestions
- **Request features explicitly** - animations, interactions, and polish require direct requests

**Example - Effective Directive:**

```text
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### 9. CODE EXPLORATION REQUIREMENTS

The AI agent **MUST**:

- **ALWAYS** read and understand relevant files before proposing code edits
- **NEVER** speculate about code that has not been inspected
- **ALWAYS** open and inspect referenced files before explaining or proposing fixes
- Be rigorous and persistent in searching code for key facts
- Thoroughly review the style, conventions, and abstractions of the codebase before implementing new features

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read it before answering. Investigate and read relevant files BEFORE answering questions about the codebase. Never make claims about code before investigating unless you are certain of the correct answer.
</investigate_before_answering>
```

### 10. PREVENT OVERENGINEERING

The AI agent **MUST NOT**:

- Add features, refactor code, or make "improvements" beyond what was asked
- Add error handling, fallbacks, or validation for scenarios that cannot happen
- Create helpers, utilities, or abstractions for one-time operations
- Design for hypothetical future requirements
- Add docstrings, comments, or type annotations to unchanged code

The AI agent **MUST**:

- Only make changes that are directly requested or clearly necessary
- Keep solutions simple and focused
- Trust internal code and framework guarantees
- Only validate at system boundaries (user input, external APIs)
- Reuse existing abstractions where possible and follow the DRY principle

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused.

Don't add features, refactor code, or make "improvements" beyond what was asked. Don't add error handling, fallbacks, or validation for impossible scenarios. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. Reuse existing abstractions where possible and follow the DRY principle.
```

### 11. AVOID HARD-CODING

The AI agent **MUST**:

- Write high-quality, general-purpose solutions using standard tools
- Implement solutions that work correctly for all valid inputs, not just test cases
- Focus on understanding problem requirements and implementing the correct algorithm
- Report unreasonable tasks, infeasible requirements, or incorrect tests rather than working around them

The AI agent **MUST NOT**:

- Create helper scripts or workarounds
- Hard-code values or create solutions that only work for specific test inputs
- Let tests define the solution - tests verify correctness, they do not define implementation

```text
Write a high-quality, general-purpose solution using standard tools. Do not create helper scripts or workarounds. Implement a solution that works correctly for all valid inputs, not just test cases. Do not hard-code values or create solutions that only work for specific test inputs.

Focus on understanding problem requirements and implementing the correct algorithm. Tests verify correctness; they do not define the solution. Provide a principled implementation that follows best practices.

If the task is unreasonable or infeasible, or if any tests are incorrect, inform me rather than working around them.
```

### 12. PARALLEL TOOL EXECUTION

The AI agent **MUST**:

- Make all independent tool calls in parallel when no dependencies exist
- Prioritize simultaneous tool execution over sequential execution
- Maximize parallel tool calls to increase speed and efficiency

The AI agent **MUST NOT**:

- Use placeholders or guess missing parameters in tool calls
- Call dependent tools in parallel - sequence them instead
- Execute tools sequentially when parallel execution is possible

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all independent tool calls in parallel. Prioritize calling tools simultaneously whenever actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files at the same time. Maximize parallel tool calls to increase speed and efficiency. If some tool calls depend on previous calls for parameter values, call them sequentially. Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

### 13. CONTEXT MANAGEMENT

The AI agent **MUST**:

- Be as persistent and autonomous as possible
- Complete tasks fully without stopping early
- Save current progress and state before context window compaction
- Continue working indefinitely from where work was left off

The AI agent **MUST NOT**:

- Stop tasks early due to token budget concerns
- Artificially stop any task early regardless of context remaining
- Abandon work when approaching context limits

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Be as persistent and autonomous as possible and complete tasks fully. Never artificially stop any task early regardless of the context remaining.
```

---

## Quick Verification Commands

```bash
# Check for forbidden patterns (should return 0 results)
grep -rE "TODO|FIXME|NotImplementedError|^\s+pass\s*$" --include="*.py" .

# Check for simulation patterns (should return 0 results)
grep -rE "asyncio\.sleep|return.*mock|return.*fake|return.*placeholder" --include="*.py" .

# Check for ellipsis/truncation (should return 0 results)
grep -rE "\.\.\.|# \.\.\.|\# rest of|continues as" --include="*.py" .

# Check for overengineering indicators (review manually)
grep -rE "class.*Helper|class.*Utility|class.*Factory" --include="*.py" .

# Check for potential hard-coded test values (review manually)
grep -rE "test_value|expected_result|mock_data" --include="*.py" .
```

---

**END OF ANTI-SHORTCUT DIRECTIVES**
