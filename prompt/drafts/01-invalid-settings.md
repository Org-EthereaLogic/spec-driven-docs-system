# Invalid settings in Claude Code

Investigate the following diagnostic issues to determine their root causes and provide solutions. Then, summarize your findings and recommendations in a comprehensive report.

## Diagnostics

- **Currently running:** npm-global (2.0.56)
- **Path:** `/Users/etherealogic/.nvm/versions/node/v24.9.0/bin/node`
- **Invoked:** `/Users/etherealogic/.nvm/versions/node/v24.9.0/bin/claude`
- **Config install method:** global
- **Auto-updates:** default (true)
- **Update permissions:** Yes
- **Search:** OK (vendor)

## Invalid Settings

**File:** `/Users/etherealogic/Dev/spec-driven-docs-system/.claude/settings.json`

### Errors

| Hook Type     | Path       | Issue                                      |
|---------------|------------|--------------------------------------------|
| PostToolUse   | `[0].hooks`| Expected object, but received string       |
| PreToolUse    | `[0].hooks`| Expected object, but received string       |

### Solution

Hooks require the new format with matchers. Update your configuration as follows:

```json
{
    "PostToolUse": [
        {
            "matcher": { "tools": ["BashTool"] },
            "hooks": [{ "type": "command", "command": "echo Done" }]
        }
    ]
}
```

For more details, see the [Claude Code Hooks documentation](https://docs.claude.com/en/docs/claude-code/hooks).