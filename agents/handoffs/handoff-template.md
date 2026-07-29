# Handoff Template

Copy this template for every handoff document. Generated files use naming convention:
`handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md`

---

```markdown
# Handoff — {ShortAgentID}

## Metadata Header
- **Issuer Main Agent ShortID:**
- **Executor Sub Agent ShortID:**
- **Global Full SHA256 Agent UID:**
- **Agent Full Role Name:**
- **Desensitized Device Fingerprint:**
- **UTC Register Timestamp (ms):**
- **UTC Document Created Time:**
- **Lifecycle Type:** Task Dispatch / Task Result Delivery
- **Related Workspace Path:**
- **Reference Docs Path (agents/*):**
- **Agent Lifecycle Status At Creation:**

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
<!-- Links to agents/references/ or agents/workflows/ files. -->

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

Example: `handoff-305cde212a-20260729-1130.md`
