# Documentation Suites

Suites organize related documents for batch operations. Each suite has a `manifest.json` that defines the documents, their dependencies, and batch configuration.

## Creating a New Suite

1. Copy the `_example` directory:
   ```bash
   cp -r .claude/docs/suites/_example .claude/docs/suites/my-suite
   ```

2. Edit `manifest.json`:
   - Update `suite_id` and `name`
   - Define your documents in the `documents` array
   - Set dependencies between documents
   - Adjust `configuration` as needed

3. Create spec files for each document using `/doc-plan`:
   ```
   /doc-plan "API Reference" --type api --suite my-suite
   ```

## Manifest Structure

| Field | Description |
|-------|-------------|
| `suite_id` | Unique identifier for the suite |
| `name` | Human-readable suite name |
| `configuration.parallel_limit` | Max concurrent document operations |
| `configuration.continue_on_error` | Whether to continue if one document fails |
| `documents[].doc_id` | Unique document identifier within suite |
| `documents[].type` | Document type: `api`, `design`, or `manual` |
| `documents[].dependencies` | Array of doc_ids that must complete first |
| `documents[].status` | `pending`, `writing`, `review`, or `completed` |

## Batch Operations

```
/doc-batch my-suite generate    # Generate all pending documents
/doc-batch my-suite review      # Review all documents
/doc-batch my-suite sync        # Synchronize cross-references
/doc-status my-suite            # View suite status
```
