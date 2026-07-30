# Git Safety — Workflow

## Hard ban

- **NEVER force-push** (`git push --force`, `--force-with-lease`) on any shared branch.
  Force-push silently erases other agents' commits — analysis scripts and chapter content were lost on 2026-07-28 due to this.
- **NEVER push to `main`.** Use branch + PR only. See root `AGENTS.md` for branch naming.

## Sandbox workaround

Local git is frequently broken on this project (detached HEAD, missing history, sandbox restrictions).
When `git push` fails, use the GitHub REST API:

1. **GET** the file's SHA:
   ```
   GET /repos/BerryUIKI/4i_e-acc/contents/<path>?ref=<branch>
   ```
2. **Base64-encode** the local file content.
3. **PUT** the update:
   ```json
   { "message": "...", "content": "<base64>", "sha": "<sha>", "branch": "<branch>" }
   ```

Never write the PAT into any file inside the repo tree. The PAT lives at `~/.workbuddy/MEMORY.md` (outside the repo).

## REST API trace gap mitigation

When commits are created via the GitHub REST API (Contents API or Git Data API), the git committer is always the PAT owner (`BerryUIKI`), not the agent. This breaks the `[ShortAgentID]` committer identity traceability rule.

### Mitigation
1. **Tag in commit message is authoritative.** The `[ShortAgentID]` prefix in the commit message is the primary traceability anchor. Even when the API committer is the human user, the message tag identifies which agent authored the change.
2. **Record API-pushed commits in the handoff.** After any REST API push, the Main agent MUST log the commit SHA + timestamp + ShortAgentID in the session handoff file under a `## API Push Log` section.
3. **Document the gap.** Every handoff that involves an API push MUST include:
   ```markdown
   > ⚠️ API-pushed commits: committer = PAT owner, not agent.
   > Traceability: `[ShortAgentID]` in commit message + this handoff record.
   ```
4. **CI exception for API-pushed commits.** When the CI pre-merge check encounters a commit with the repo owner as committer AND a `[ShortAgentID]` in the message, it checks for a corresponding handoff log entry instead of rejecting the mismatch. This allows API pushes while maintaining audit integrity.

## Bulk file push (single commit)

For pushing many files at once, use the Git Data API (blob → tree → commit → ref) instead of the Contents API (which creates one commit per file). Example in the project's commit history: `68a0c60`.
