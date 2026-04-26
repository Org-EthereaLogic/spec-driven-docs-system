---
model: haiku
description: Example plugin command demonstrating the standard structure
argument-hint: <required-arg> [--optional-flag <value>]
allowed-tools: Read, Glob
---

# Example Plugin Command

<!-- KEEP: every command needs a top-level heading and a one-sentence role description -->

You are an example command using Claude Haiku 4.5. Replace this paragraph with a description of what your command does and which tier of model is appropriate.

## Variables

<!-- KEEP: bind positional args and the full ARGUMENTS string for flag parsing -->

ARG: $1
ARGUMENTS: $ARGUMENTS

## Core Principles

<!-- EXTENSION POINT: add 3-5 named principle blocks that govern your command's behavior. -->
<!-- Each block is an XML-tag wrapper around an instruction + a "Why this matters:" rationale. -->

<example_principle>
Replace this with a real principle. State the rule, then explain why following it produces better outcomes than ignoring it.

**Why this matters:** Principles guide judgment when instructions are incomplete. The "Why" line is what lets the model handle edge cases the instructions did not anticipate.
</example_principle>

<use_parallel_tool_calls>
When reading multiple files or running multiple Glob/Grep operations, do them in parallel via concurrent tool calls.

**Why this matters:** Sequential reads add unnecessary latency. Parallel reads are correct and faster.
</use_parallel_tool_calls>

## Instructions

<!-- EXTENSION POINT: replace these phases with your actual command logic. -->
<!-- Use numbered phases. Each phase has 2-5 sub-steps. -->

### Phase 1: Parse Arguments

1. Read `ARG` and any flags from `ARGUMENTS`.
2. Validate the arguments are present and well-formed.
3. If invalid, abort with a usage message.

### Phase 2: Do The Thing

1. Use the allowed tools to perform the command's actual operation.
2. Build the result.

### Phase 3: Output

1. Format the result according to the Output Format section below.

## Error Handling

<!-- EXTENSION POINT: list specific errors your command can produce. -->

| Error | Response | Rationale |
|-------|----------|-----------|
| Missing required argument | Show usage and exit | Don't proceed with undefined behavior |
| Tool returned unexpected result | Report the exact error to the user | Surface failures, don't swallow them |

## Output Format

<!-- KEEP: every command should end with a structured output block. -->

End every successful invocation with a result summary:

```text
[Command Name] Complete
========================

[Key]:    [Value]
[Key]:    [Value]

Next steps:
  [Suggested follow-up command 1]
  [Suggested follow-up command 2]
```

## Examples

```text
/doc-custom example-arg
/doc-custom example-arg --optional-flag value
```
