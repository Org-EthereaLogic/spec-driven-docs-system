---
allowed-tools: Bash, Read, Write, Glob, Grep
description: Automated workspace maintenance with temporary file removal, orphaned file management, and archival
argument-hint: [--execute flag for actual changes (default: dry-run)]
model: claude-haiku-4-5-20251001
---

# cleanup_workspace

Perform automated workspace maintenance to keep the SynthAI codebase clean and organized. This command delegates to the specialized workspace cleanup agent for comprehensive maintenance operations.

## Agent Delegation

This command invokes the workspace cleanup agent located at:
`/workspaces/SynthAI/.claude/agents/workspace-cleanup.md`

## Usage

```bash
/cleanup_workspace [--execute]
```

## Arguments

- `--execute`: Execute actual cleanup operations (default: dry-run mode)
- No arguments: Run in dry-run mode to preview changes

## Agent Capabilities

The workspace cleanup agent provides:

- **Temporary File Removal**: Python cache, build artifacts, stale logs
- **Orphaned File Management**: Move misplaced files to organized structure
- **Logical Reorganization**: Relocate files to proper directories
- **Archival Operations**: Compress and archive old inactive files
- **Safety Verification**: Protect git-tracked files and critical directories
- **Comprehensive Reporting**: Detailed logs and statistics

## Execution Flow

1. Parse command arguments to determine execution mode
2. Invoke workspace cleanup agent with appropriate parameters
3. Agent performs all maintenance operations following SynthAI safety patterns
4. Return comprehensive report to user

## Safety Features

- Dry-run by default (no changes without explicit --execute flag)
- All git-tracked files automatically protected
- Protected directories excluded (.git, .venv, node_modules, trees)
- Complete audit trail in logs
- Orphaned files moved, not deleted
- Full verification before and after operations

## Example Output

### Dry-Run Mode
```
=== SynthAI Workspace Cleanup Report ===
Mode: DRY-RUN (no changes made)
[Agent generates detailed preview of proposed changes]

To execute these changes, run:
  /cleanup_workspace --execute
```

### Execute Mode
```
=== SynthAI Workspace Cleanup Results ===
Mode: EXECUTE (changes applied)
[Agent reports completed operations and verification results]

Workspace cleanup completed successfully.
```

## Notes

- Agent enforces complete operations (no shortcuts or placeholders)
- All operations logged to `logs/cleanup_<timestamp>.log`
- Follows SynthAI anti-shortcut philosophy
- Comprehensive error handling and recovery

For agent implementation details, see:
`/workspaces/SynthAI/.claude/agents/workspace-cleanup.md`
