# Design Document Template

## Purpose
This template defines the structure and requirements for design documents. Use this template when documenting system architecture, technical designs, feature specifications, or architectural decisions.

## Target Audience
- Engineering teams implementing the design
- Technical leads reviewing the approach
- Architects ensuring system coherence
- Future maintainers understanding decisions

---

## Required Sections

### 1. Problem Statement
**Purpose:** Clearly define the problem being solved.

**Must Include:**
- Current state description
- Pain points or limitations
- Impact of not solving the problem
- Success criteria

**Example Structure:**
```markdown
# [Design Title]

**Status:** [Draft | In Review | Approved | Implemented | Deprecated]
**Author:** [Name]
**Created:** [Date]
**Last Updated:** [Date]

## Problem Statement

### Current State
[Describe how things work today]

### Pain Points
- [Pain point 1 with quantified impact if possible]
- [Pain point 2]
- [Pain point 3]

### Impact
If not addressed, [describe consequences].

### Success Criteria
This design is successful if:
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
```

---

### 2. Goals and Non-Goals
**Purpose:** Define explicit scope boundaries.

**Must Include:**
- What the design will accomplish
- What the design explicitly will NOT address
- Why non-goals are out of scope

**Example Structure:**
```markdown
## Goals and Non-Goals

### Goals
1. **[Goal 1]:** [Explanation of what and why]
2. **[Goal 2]:** [Explanation]
3. **[Goal 3]:** [Explanation]

### Non-Goals
1. **[Non-Goal 1]:** [Why this is out of scope for this design]
2. **[Non-Goal 2]:** [Reason]

> **Note:** Non-goals may be addressed in future iterations.
```

---

### 3. Proposed Solution
**Purpose:** Detail the recommended approach.

**Must Include:**
- High-level overview
- Architecture diagram(s)
- Component descriptions
- Data flow
- Key interfaces/APIs
- Security considerations

**Example Structure:**
```markdown
## Proposed Solution

### Overview
[2-3 paragraph summary of the approach]

### Architecture

\`\`\`mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Component C]
    B --> D[Database]
\`\`\`

### Components

#### [Component Name]
- **Purpose:** [What it does]
- **Responsibilities:**
  - [Responsibility 1]
  - [Responsibility 2]
- **Dependencies:** [What it depends on]
- **Interface:**
  \`\`\`typescript
  interface ComponentAPI {
    method(param: Type): ReturnType;
  }
  \`\`\`

### Data Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Security Considerations
- [Security aspect 1]
- [Security aspect 2]
```

---

### 4. Alternatives Considered
**Purpose:** Document other approaches and why they were rejected.

**Must Include:**
- At least 2 alternative approaches
- Pros and cons of each
- Clear reasoning for rejection

**Example Structure:**
```markdown
## Alternatives Considered

### Alternative 1: [Name]

**Description:** [Brief description of the approach]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Rejection Reason:** [Why this wasn't chosen]

---

### Alternative 2: [Name]

**Description:** [Brief description]

**Pros:**
- [Advantage 1]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Rejection Reason:** [Why this wasn't chosen]

---

### Comparison Matrix

| Criterion | Proposed | Alt 1 | Alt 2 |
|-----------|----------|-------|-------|
| Complexity | Low | Medium | High |
| Performance | High | Medium | High |
| Maintainability | High | Low | Medium |
```

---

### 5. Implementation Plan
**Purpose:** Define how the design will be implemented.

**Must Include:**
- Phases or milestones
- Dependencies between work items
- Rough effort estimates
- Rollout strategy

**Example Structure:**
```markdown
## Implementation Plan

### Phase 1: Foundation
**Goal:** [Phase objective]
**Dependencies:** None

| Task | Description | Effort |
|------|-------------|--------|
| [Task 1] | [Description] | [S/M/L] |
| [Task 2] | [Description] | [S/M/L] |

### Phase 2: Core Implementation
**Goal:** [Phase objective]
**Dependencies:** Phase 1 complete

| Task | Description | Effort |
|------|-------------|--------|
| [Task 1] | [Description] | [S/M/L] |

### Phase 3: Integration & Polish
**Goal:** [Phase objective]
**Dependencies:** Phase 2 complete

| Task | Description | Effort |
|------|-------------|--------|
| [Task 1] | [Description] | [S/M/L] |

### Rollout Strategy
- **Stage 1:** [Internal testing]
- **Stage 2:** [Beta users]
- **Stage 3:** [General availability]

### Feature Flags
| Flag | Description | Default |
|------|-------------|---------|
| [flag_name] | [What it controls] | [on/off] |
```

---

### 6. Risks and Mitigations
**Purpose:** Identify potential problems and how to address them.

**Must Include:**
- Technical risks
- Operational risks
- Business risks
- Mitigation strategies

**Example Structure:**
```markdown
## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation strategy] |
| [Risk 2] | Low | Critical | [Mitigation strategy] |
| [Risk 3] | High | Low | [Mitigation strategy] |

### Detailed Risk Analysis

#### [Risk 1 Name]
- **Description:** [Full description]
- **Trigger:** [What would cause this]
- **Impact:** [Consequences if it occurs]
- **Mitigation:** [How to prevent or handle]
- **Monitoring:** [How to detect early]
```

---

### 7. Open Questions
**Purpose:** Document unresolved decisions requiring input.

**Must Include:**
- Question statement
- Options being considered
- Who needs to decide
- Decision deadline

**Example Structure:**
```markdown
## Open Questions

### Q1: [Question title]
**Question:** [Full question]
**Options:**
1. [Option A] - [Brief pros/cons]
2. [Option B] - [Brief pros/cons]

**Decision Maker:** [Name/Team]
**Needed By:** [Date]
**Status:** [Open | Resolved]
**Decision:** [If resolved, the decision made]

---

### Q2: [Question title]
[Same format]
```

---

## Optional Sections

### Testing Strategy
How the implementation will be tested.

### Monitoring and Observability
Metrics, logs, and alerts to add.

### Performance Requirements
Expected performance characteristics and benchmarks.

### Backwards Compatibility
How existing functionality is preserved.

### Migration Plan
How to move from current to new state.

### Cost Analysis
Infrastructure or operational cost implications.

---

## Style Guidelines

### Diagrams
- Include at least one architecture diagram
- Use Mermaid for version-controllable diagrams
- Label all components clearly
- Show data flow direction

### Decisions
- Be explicit about decisions and reasoning
- Document trade-offs honestly
- Acknowledge uncertainties

### Terminology
- Define technical terms on first use
- Be consistent with project terminology
- Avoid jargon where possible

### Length
- Problem Statement: 1-2 paragraphs
- Proposed Solution: As detailed as needed
- Each Alternative: 1-2 paragraphs
- Aim for completeness over brevity
