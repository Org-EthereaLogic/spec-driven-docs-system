#!/bin/bash
# setup-isolated-test.sh
# Creates an isolated test environment simulating real-world installation
#
# Usage: ./tests/setup-isolated-test.sh [test-root]
# Default test root: /tmp/spec-docs-test

set -e

# Configuration
TEST_ROOT="${1:-/tmp/spec-docs-test}"
FRAMEWORK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "========================================"
echo "Isolated Test Environment Setup"
echo "========================================"
echo "Framework: $FRAMEWORK_ROOT"
echo "Test Root: $TEST_ROOT"
echo ""

# Clean previous test environment
if [ -d "$TEST_ROOT" ]; then
    echo "Removing existing test environment..."
    rm -rf "$TEST_ROOT"
fi

# Create test directory structure
echo "Creating test directory structure..."
mkdir -p "$TEST_ROOT"
mkdir -p "$TEST_ROOT/source"
mkdir -p "$TEST_ROOT/docs"

# Copy framework files (simulating real installation)
echo "Installing framework files..."
cp -r "$FRAMEWORK_ROOT/.claude" "$TEST_ROOT/"
cp -r "$FRAMEWORK_ROOT/specs" "$TEST_ROOT/"

# Remove any test artifacts from copied files
rm -rf "$TEST_ROOT/.claude/docs/suites/"*
rm -rf "$TEST_ROOT/specs/docs/"*

# Restore only the _example templates
mkdir -p "$TEST_ROOT/.claude/docs/suites"
cp -r "$FRAMEWORK_ROOT/.claude/docs/suites/_example" "$TEST_ROOT/.claude/docs/suites/"
cp "$FRAMEWORK_ROOT/.claude/docs/suites/README.md" "$TEST_ROOT/.claude/docs/suites/" 2>/dev/null || true

mkdir -p "$TEST_ROOT/specs/docs"
cp -r "$FRAMEWORK_ROOT/specs/docs/_example" "$TEST_ROOT/specs/docs/" 2>/dev/null || true
cp "$FRAMEWORK_ROOT/specs/docs/README.md" "$TEST_ROOT/specs/docs/" 2>/dev/null || true

# Create self-contained test source materials
echo "Creating test source materials..."

cat > "$TEST_ROOT/source/task-manager-overview.md" << 'EOF'
# Task Manager System Overview

## Purpose

Task Manager is a simple CLI-based task tracking system designed for developers. It allows users to create, update, list, and delete tasks from the command line.

## Core Concepts

### Task
A task is the fundamental unit of work. Each task has:
- **ID**: Unique 8-character hexadecimal identifier
- **Title**: Brief description (max 100 chars)
- **Status**: pending | in_progress | completed
- **Priority**: low | medium | high | critical
- **Created**: ISO 8601 timestamp
- **Updated**: ISO 8601 timestamp

### Project
Tasks are organized into projects. A project groups related tasks and provides:
- **Name**: Project identifier
- **Description**: What the project is about
- **Tasks**: Collection of task references

## Architecture

### Components
1. **CLI Interface** - Parses commands and arguments
2. **Task Service** - Business logic for task operations
3. **Storage Layer** - JSON file-based persistence
4. **Formatter** - Output formatting (table, JSON, minimal)

### Data Flow
```
User Input → CLI Parser → Task Service → Storage → Response → Formatter → Output
```

## API Endpoints (Internal)

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Create | POST | /tasks | Create new task |
| Read | GET | /tasks/:id | Get task by ID |
| Update | PUT | /tasks/:id | Update task |
| Delete | DELETE | /tasks/:id | Remove task |
| List | GET | /tasks | List all tasks |

## Error Handling

| Error Code | Description |
|------------|-------------|
| TASK_NOT_FOUND | Task with specified ID does not exist |
| INVALID_STATUS | Status value not in allowed set |
| INVALID_PRIORITY | Priority value not in allowed set |
| STORAGE_ERROR | Failed to read/write storage file |

## Usage Examples

```bash
# Create a task
task-manager create "Fix login bug" --priority high

# List all tasks
task-manager list

# Update task status
task-manager update abc12345 --status completed

# Delete a task
task-manager delete abc12345
```

## Configuration

Configuration file: `~/.task-manager/config.json`

```json
{
  "storage_path": "~/.task-manager/tasks.json",
  "default_priority": "medium",
  "output_format": "table"
}
```

## Technology Stack

- **Runtime**: Bun 1.0+
- **Language**: TypeScript
- **Storage**: JSON files
- **CLI Framework**: Commander.js
EOF

# Create test progress log template
cat > "$TEST_ROOT/test_progress.json" << EOF
{
  "test_plan_version": "1.0",
  "test_type": "isolated_installation",
  "execution_started": "$TIMESTAMP",
  "current_phase": 1,
  "phase_name": "Installation Validation",
  "last_checkpoint": "$TIMESTAMP",
  "documents": {},
  "commands_executed": [],
  "agents_invoked": {},
  "review_iterations": [],
  "issues_encountered": [],
  "corrections_applied": [],
  "patterns_learned": [],
  "batch_operations": [],
  "notes": [
    "$TIMESTAMP: Test environment created via setup-isolated-test.sh"
  ]
}
EOF

# Verify installation
echo ""
echo "Verifying installation..."
echo ""

echo "Framework directories:"
ls -la "$TEST_ROOT/.claude/" 2>/dev/null || echo "  ERROR: .claude/ missing"

echo ""
echo "Specs directories:"
ls -la "$TEST_ROOT/specs/docs/" 2>/dev/null || echo "  ERROR: specs/docs/ missing"

echo ""
echo "Source materials:"
ls -la "$TEST_ROOT/source/" 2>/dev/null || echo "  ERROR: source/ missing"

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. cd $TEST_ROOT"
echo "  2. Start Claude Code: claude"
echo "  3. Run: /doc-status"
echo "  4. Follow test plan phases"
echo ""
echo "Test plan: $FRAMEWORK_ROOT/tests/isolated-test-plan.md"
echo ""
EOF
