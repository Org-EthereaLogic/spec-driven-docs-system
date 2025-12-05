# Approved Final Documentation

This directory contains **production-ready** documentation that has been **approved for publication**.

## Purpose

Documents in approved_final:

- Have passed quality review (Grade A or B)
- Have received stakeholder approval
- Are ready for public/internal distribution
- Represent the **canonical, authoritative** version

## Quality Level

**Production Ready** - Approved and publishable

These documents are suitable for:

- Public documentation websites
- Developer portals
- Internal knowledge bases
- Customer-facing materials

## Maintenance

### When to Update

Update documents when:

- APIs or features change
- Errors or inaccuracies are discovered
- User feedback identifies gaps
- Business requirements evolve

### Update Process

1. **Update the specification** in `specs/docs/`
2. **Regenerate** the document:

   ```bash
   /doc-write specs/docs/[spec].md
   ```

3. **Review** the updated document:

   ```bash
   /doc-review spec_driven_docs/rough_draft/[category]/[document].md
   ```

4. **Move through workflow** again (pending_approval → approved_final)
5. **Archive old version** if needed (git history preserves it)

### Version Control

- Track all changes via git commits
- Use semantic versioning for major documentation releases
- Tag releases corresponding to product versions
- Maintain changelog for significant updates

## Publishing

Documents from this directory can be:

- Deployed to documentation websites
- Included in product releases
- Distributed to customers
- Linked from public resources

## File Organization

```text
approved_final/
├── api/                    # API documentation
├── design/                 # Design documents
└── guides/                 # User manuals
```

Maintain consistent structure with other workflow stages.

## Archive Strategy

For old/deprecated documentation:

- Keep in git history (don't delete)
- Add deprecation notices if still accessible
- Consider moving to `approved_final/archive/[year]/` for long-term storage
- Update cross-references to point to current versions
