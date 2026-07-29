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

## Bulk file push (single commit)

For pushing many files at once, use the Git Data API (blob → tree → commit → ref) instead of the Contents API (which creates one commit per file). Example in the project's commit history: `68a0c60`.
