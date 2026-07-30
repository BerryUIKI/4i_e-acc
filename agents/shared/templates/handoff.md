# Handoff Template

Copy this template for every handoff document. Generated files use naming convention:
`handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md`

---

```markdown
# Handoff — {ShortAgentID}

## Metadata
- **Agent**: {ShortAgentID}
- **Task**: {one-line summary}
- **Branch**: {branch-name}
- **Status**: DISPATCHED / IN_PROGRESS / DONE

---

## 1. Task Summary
<!-- One-paragraph description of what needs to be done. -->

## 2. Context & Background
<!-- Why this task exists. Relevant history, decisions, constraints. -->

## 3. Hard Constraints
<!-- Non-negotiable rules. Reference root AGENTS.md if needed. -->
- [ ] Constraint 1
- [ ] Constraint 2

## 4. Input Files
<!-- Full repository paths or embedded content. Use full URLs if sub-agent cannot access the repo. -->
| File | Path | Description |
|---|---|---|
| ... | ... | ... |

## 5. Expected Outputs
<!-- Concrete deliverables with file paths. -->
| Output | Path | Format |
|---|---|---|
| ... | ... | ... |

## 6. Forbidden Operations
<!-- Things the sub-agent MUST NOT do. -->
- Never push to remote origin
- Never modify files outside the allowed workspace
- ...

## 7. Reference Documents
<!-- Links to agents/shared/references/ or agents/shared/workflows/ files. -->

## 8. Risk & Validation Checklist
- [ ] All expected outputs produced
- [ ] No forbidden operations performed
- [ ] Commit message starts with `[{ShortAgentID}]`
- [ ] Handoff document follows naming convention
```

---

## Naming convention

```
handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md
```

Example: `handoff-f78f1d3e-20260729-2300.md`
