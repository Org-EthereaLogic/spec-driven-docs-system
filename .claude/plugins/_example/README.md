# Example Plugin

This is a working skeleton for a command plugin. Copy this directory, rename it, and customize the contents to build your own plugin.

## Files in this Plugin

- `plugin.json` - manifest (required)
- `doc-custom.md` - the command entry point
- `README.md` - this file (recommended)

## How to Use This as a Template

1. Copy this directory to a new name:

   ```bash
   cp -r .claude/plugins/_example .claude/plugins/my-new-plugin
   ```

2. Edit `plugin.json`:
   - Change `name` to your plugin's name (kebab-case, matching the directory)
   - Update `description` to one sentence describing what the command does
   - Update `entry_point` and `installs` if you renamed the command file
   - Update `author` and `version`

3. Edit `doc-custom.md`:
   - Rename it to `doc-<your-verb>.md` (e.g., `doc-changelog.md`)
   - Update the frontmatter `description` and `argument-hint`
   - Replace the example phases with your actual command logic
   - Adjust `allowed-tools` to only include tools the command actually needs

4. Update this README to describe your specific plugin.

5. Install the command by symlinking it:

   ```bash
   ln -s ../../plugins/my-new-plugin/doc-<your-verb>.md \
         .claude/commands/doc/doc-<your-verb>.md
   ```

   Or copy:

   ```bash
   cp .claude/plugins/my-new-plugin/doc-<your-verb>.md \
      .claude/commands/doc/
   ```

6. Test:

   ```bash
   npm test
   ```

## Reading the Example Command

Open `doc-custom.md`. The comments mark each section that you must customize:

- `<!-- EXTENSION POINT -->` markers indicate where to add your own logic
- `<!-- KEEP -->` markers indicate sections you should preserve as-is

## Removing the Example

If you don't need the example skeleton, simply delete this directory:

```bash
rm -rf .claude/plugins/_example
```

The example is not installed (no symlink in `.claude/commands/`) so removing it has no effect on the system.
