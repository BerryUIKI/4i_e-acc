# Handoff Reception & Validation — Workflow

Mandatory procedure for every agent when receiving a handoff document from `agents/handoffs/`.

---

## Step 1 — Roster validation

Read the handoff file's metadata header. Extract the `Issuer Main Agent ShortID` and `Executor Sub Agent ShortID`.

Cross-reference both against `agents/handoffs/agent-roster.md`:

| Check | If FAIL |
|-------|---------|
| ShortAgentID exists in roster | **Abort immediately.** Do not read further. Do not execute any task. Tell the user: `"Handoff file references unregistered agent: {ShortAgentID}. This agent is not in the roster. The handoff cannot be processed. Should I accept this handoff anyway?"` Wait for explicit user confirmation before proceeding. |
| Agent lifecycle status is ACTIVE | **Abort.** If SUSPENDED/RETIRED/DRAFT: `"The agent {ShortAgentID} has status {STATUS}. Handoff cannot be executed. Please check the roster entry."` |

---

## Step 2 — Role scope check

Compare the handoff's `Agent Full Role Name` against the receiving agent's own role in the roster.

| Check | If FAIL |
|-------|---------|
| Task domain matches receiver's domain | `"This handoff is scoped to role {role}. My registered role is {my_role}. This task falls outside my authorized domain. Do you want me to proceed anyway?"` |
| Forbidden operations list is compatible with receiver's permissions | If the handoff requires git push and receiver is a Sub agent: **reject unconditionally.** Sub agents cannot push. Tell user: `"This handoff requires git push but I am a Sub agent — push is forbidden by root AGENTS.md."` |

---

## Step 3 — Push status check

Verify all work from the issuer is pushed to the remote branch:

1. Read the handoff's `Related Workspace Path`.
2. If local git history exists, run `git log --oneline -10` and check that the latest commit SHA matches what the handoff claims.
3. If local git is unavailable (sandbox), query the GitHub API for the branch's latest commit and compare.
4. **If work is not pushed**: `"The issuer's work has not been pushed to remote. I cannot verify completeness. Should I continue with the handoff, or wait for the push?"`

---

## Step 4 — File integrity check

Verify all files listed in the handoff's "Completed work" or "Modified files" section actually exist at their stated paths:

| Check | Action |
|-------|--------|
| File exists at stated path | Continue |
| File missing | Log warning. `"Referenced file {path} not found. Handoff may be incomplete."` |
| Handoff references files the receiver cannot access | Tell user: `"Handoff references {path} which I cannot access."` |

---

## Step 5 — Cleanup

After all checks pass and the user confirms acceptance:

1. **Delete the received handoff file** from `agents/handoffs/`.
2. **Scan for stale handoffs**: check `agents/handoffs/` for any handoff files older than 48 hours that do not reference an active roster agent. List them to the user: `"Found {N} stale handoff files. Should I delete them?"`
3. **If user confirms**: delete stale files.
4. **If the issuer's handoff was a task dispatch**: archive a brief summary in the session's daily memory log before deletion (so the trace is not lost).

---

## Step 6 — Resume normal workflow

After cleanup, proceed with the task described in the handoff (if accepted). All subsequent commits must reference the issuer's ShortAgentID in a "dispatched-by" note if the work originated from a handoff dispatch.

---

## Quick reference

| Step | Check | Fail action |
|------|-------|-------------|
| 1 | Agent in roster + ACTIVE | Abort, ask user |
| 2 | Role scope match | Warn, ask user (Sub push = hard reject) |
| 3 | Work pushed to remote | Warn, ask user |
| 4 | Referenced files exist | Log warning |
| 5 | Delete handoff + clean stale files | Ask user before deleting stale |
| 6 | Proceed or archive | Resume normal workflow |
