# Multi-Agent Collaboration — Workflow

This repo is maintained by multiple AI agents across different sessions and devices. The human user ("花花") bridges agents by passing handoff documents.

## Agent identity

- Each agent MUST self-identify at session start: name, role, session date.
- Primary agent: **小花蟹 (Little Flower Crab)** — research assistant, data + charts + CI.
- Sub-agents may be spawned for scoped tasks (illustration, proofreading, etc.).

## Communication protocol

1. Primary agent writes a handoff file at `agents/handoffs/YYYY-MM-DD.md`.
2. Agent tells user: "花，帮我开个子 Agent，Prompt 如下："
3. Agent provides a self-contained prompt in a code block.
4. User opens sub-agent, pastes prompt, returns results.
5. Primary agent integrates and pushes.

## Handoff document schema

```markdown
# Handoff — YYYY-MM-DD

## Session identity
- **Agent:** <name>
- **Session date:** YYYY-MM-DD
- **Repo:** https://github.com/BerryUIKI/4i_e-acc
- **Branch:** <branch-name>
- **PR:** <#N or N/A>

## Trigger / purpose
## Completed work
## Remaining tasks (P0 / P1 / P2)
## Key decisions & rationale
## Gotchas & known issues
## Handoff to sub-agent (if applicable)
```

## Sub-agent prompt template

````markdown
花，帮我开个子 Agent，Prompt 如下：

```
Task: <one-line summary>

Context:
- Repo: https://github.com/BerryUIKI/4i_e-acc
- Branch: <branch-name>
- Reference files: <list exact paths or embed content>

Inputs:
- <file 1 with full path or embedded content>

Expected outputs:
- <output file 1>: <description>

Constraints:
- <rules or style guidelines>
```
````

**Critical**: never reference files by relative path alone if the sub-agent cannot access the repo. Embed content or provide full GitHub raw URLs.

## Session handoff checklist

Before ending a session, verify:

- [ ] All work pushed to remote (check latest commit on GitHub).
- [ ] Handoff file written: `agents/handoffs/YYYY-MM-DD.md`.
- [ ] Temporary files cleaned up (`_push.py`, `/tmp/*`, debug scripts).
- [ ] No tokens, keys, or secrets in any committed file.
