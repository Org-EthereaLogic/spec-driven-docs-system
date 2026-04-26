# Plugin System

The spec-driven-docs-system supports four kinds of extensions: commands, agents, templates, and hooks. Plugins live under `.claude/plugins/<plugin-name>/` with a `plugin.json` manifest describing what they install.

## Plugin Types

| Type | What it adds | Where it gets installed |
|------|--------------|-------------------------|
| `command` | A new `/doc-*` slash command | `.claude/commands/doc/` |
| `agent` | A specialized sub-agent | `.claude/agents/` |
| `template` | A new document template | `.claude/docs/templates/` (and registered in `_template-registry.md`) |
| `hook` | A pre/post write validation hook | `.claude/hooks/` (and registered in `.claude/settings.json`) |

A single plugin directory can ship multiple files (e.g., a command + a template). The `type` field in `plugin.json` indicates the primary type for discovery.

## `plugin.json` Manifest Schema

Every plugin MUST contain a `plugin.json` at its root. Fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Plugin name in kebab-case |
| `version` | string | yes | Semver (e.g., `1.0.0`) |
| `type` | string | yes | One of: `command`, `agent`, `template`, `hook` |
| `entry_point` | string | yes | Path relative to plugin directory (e.g., `doc-custom.md`) |
| `description` | string | yes | One-sentence description |
| `author` | string | no | Author name or org |
| `compatibility` | object | no | `{ "min_system_version": "1.0" }` |
| `installs` | array | no | Additional files this plugin places (relative paths from plugin dir) |
| `requires` | array | no | Other plugin names this plugin depends on |

### Example

```json
{
  "name": "doc-changelog",
  "version": "1.0.0",
  "type": "command",
  "entry_point": "doc-changelog.md",
  "description": "Generate a CHANGELOG entry from recent doc activity",
  "author": "EthereaLogic",
  "compatibility": { "min_system_version": "1.0" }
}
```

## Installation

Plugins are file-based. There is no build step or `npm install`.

1. Copy the plugin directory into `.claude/plugins/`.
2. Copy or symlink the entry point file into the appropriate target directory:

   | Plugin type | Target directory |
   |-------------|------------------|
   | command | `.claude/commands/doc/` |
   | agent | `.claude/agents/` |
   | template | `.claude/docs/templates/` (also add an entry to `_template-registry.md`) |
   | hook | `.claude/hooks/` (also register the matcher in `.claude/settings.json`) |

3. For hook plugins, add the matcher to `.claude/settings.json`:

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "<your matcher pattern>",
           "hooks": [{ "type": "command", "command": "python3 .claude/hooks/<your-hook>.py" }]
         }
       ]
     }
   }
   ```

4. Run `npm test` to verify the system still passes smoke tests.

## Per-Type Constraints

### Command plugins

- Must follow the standard command file structure: YAML frontmatter (`model`, `description`, `argument-hint`, `allowed-tools`), `## Variables`, `## Core Principles`, numbered phases, `## Output Format`.
- Must declare `allowed-tools` accurately. Tools not listed will be unavailable.
- The slash command name is derived from the filename (e.g., `doc-changelog.md` → `/doc-changelog` or `doc:doc-changelog`).

### Agent plugins

- Must follow the agent frontmatter pattern: `name`, `model` (haiku/sonnet/opus), `description`, `tools`.
- Must include a `## Accumulated Patterns` section if you want `/doc-improve` to learn from outputs.
- Should reference `CONSTITUTION.md` and `DIRECTIVES.md` when relevant.

### Template plugins

- Must include the standard template sections: Purpose, Target Audience, Required Sections, Style Guidelines, Anti-Bloat Warning, Template Body.
- Must add a corresponding `quality_profiles` entry in `quality-gates.json` if the template needs custom quality enforcement.
- Must register in `_template-registry.md` under both Available Templates and Template Selection Guide.

### Hook plugins

- Must be Python 3.10+ scripts with the `# /// script` PEP 723 metadata block.
- Should `from hook_utils import ...` to share utilities (sys.path setup at top is required).
- Must produce JSON output matching the existing hook contract (`continue`, `feedback` for PreToolUse; `feedback` only for PostToolUse).
- Must run quickly (target < 100ms) since they fire on every matching tool call.

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Plugin directory | `kebab-case` | `doc-changelog/` |
| Plugin name in manifest | matches directory | `doc-changelog` |
| Command file | `doc-<verb>.md` | `doc-changelog.md` |
| Agent file | `<noun>-<role>.md` | `release-notes-writer.md` |
| Template file | `<type>.md` | `runbook.md` |
| Hook file | `doc_<phase>_<purpose>.py` | `doc_pre_write_security.py` |

## Example Plugin

See `_example/` in this directory for a working command plugin skeleton with all required files:

- `plugin.json` - the manifest
- `doc-custom.md` - the command entry point with extension-point comments
- `README.md` - documentation specific to that plugin

Copy `_example/`, rename it, and customize.

## Compatibility and Versioning

The `compatibility.min_system_version` field declares the minimum spec-driven-docs-system version the plugin was tested against. The current system version is read from `package.json` `version` field. If a plugin requires a newer version than installed, the operator should either upgrade the system or flag it as incompatible.

Breaking changes to the plugin interface will be noted in the system's CHANGELOG. Plugins should pin their `compatibility.min_system_version` to the version they were tested against.

## Discovery

Currently plugins are discovered by directory presence. There is no automatic registration. The expected workflow is:

1. Maintainer reviews plugin source (read `plugin.json`, read entry point file).
2. If acceptable, the maintainer manually copies/symlinks files to the target directories listed in "Installation" above.
3. Tests are run to confirm the system still works.

A future enhancement may add an `install` script that automates step 2 - this is intentionally not present today to keep the surface area small and reviewable.

## Reporting Issues with Plugins

If a plugin breaks the system, the easiest recovery is to:

1. Remove the symlink/copy from the target directory (e.g., `.claude/commands/doc/<plugin-cmd>.md`).
2. Run `npm test` to confirm the system is back to baseline.
3. Report the issue to the plugin author.

The plugin's own directory under `.claude/plugins/` does not affect system operation - only the installed copies in target directories do.
