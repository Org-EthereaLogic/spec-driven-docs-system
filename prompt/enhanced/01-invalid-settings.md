# Fix Invalid Claude Code Hook Configuration

Resolve the invalid hook configuration errors in this project's Claude Code settings file and verify the fix works correctly.

## Context

**Settings File:** `/Users/etherealogic/Dev/spec-driven-docs-system/.claude/settings.json`

**Current Errors:**
| Hook Type     | Path         | Issue                                |
|---------------|--------------|--------------------------------------|
| PostToolUse   | `[0].hooks`  | Expected object, but received string |
| PreToolUse    | `[0].hooks`  | Expected object, but received string |

**Root Cause:** The `hooks` array contains bare strings (script paths) instead of command objects. Claude Code hooks require each entry in the `hooks` array to be an object with `type` and `command` properties.

## Task

### Phase 1: Fix the Configuration

Update the settings.json to use the correct hook format. Transform:

```json
"hooks": [".claude/hooks/doc_pre_write.py"]
```

Into:

```json
"hooks": [
  {
    "type": "command",
    "command": ".claude/hooks/doc_pre_write.py"
  }
]
```

Apply this fix to both `PreToolUse` and `PostToolUse` configurations while preserving the existing `matcher` patterns.

### Phase 2: Verify the Fix

1. Read the updated settings.json to confirm correct structure
2. Validate JSON syntax is correct
3. Verify each hook entry has the required `type` and `command` properties

### Phase 3: Document Resolution

Create a brief summary containing:
- What was wrong (the specific schema violation)
- What was fixed (the structural changes made)
- How to prevent this in the future (reference to correct format)

## Reference

The correct hook structure per Claude Code documentation (`docs/claude-code-hooks.md`):

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

## Success Criteria

- [ ] settings.json contains valid JSON
- [ ] Both `PreToolUse` and `PostToolUse` hooks use object format with `type` and `command`
- [ ] Original matcher patterns (`Write.*docs/.*\\.md$`) are preserved
- [ ] Original script paths are preserved as command values
- [ ] Running Claude Code diagnostics shows no hook configuration errors
