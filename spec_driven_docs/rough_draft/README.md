# Rough Draft Documentation

This directory contains **initial output** from the `/doc-write` command.

## Purpose

Documents in rough_draft are:

- Freshly generated from specifications
- **Not yet reviewed** for quality
- May contain errors, placeholders, or inconsistencies
- **Not suitable** for public consumption

## Quality Level

**Unreviewed** - Do not share externally

Documents here have not passed quality gates and may require iteration.

## Next Steps

1. **Review the document:**

   ```bash
   /doc-review spec_driven_docs/rough_draft/[category]/[document].md --fix
   ```

2. **If grade is C, D, or F:** Iterate on the specification or document
3. **If grade is A or B:** Move to pending_approval stage

## Iteration Strategy

| Grade | Action |
|-------|--------|
| A/B | Document is high quality, move to pending_approval |
| C | Iterate once, focus on specific issues |
| D | Significant issues, review spec completeness |
| F | Major problems, restart from specification |

## File Organization

```text
rough_draft/
├── api/                    # API documentation
├── design/                 # Design documents (RFCs, architecture)
└── guides/                 # User manuals and how-to guides
```

Maintain consistent categorization across all workflow stages.
