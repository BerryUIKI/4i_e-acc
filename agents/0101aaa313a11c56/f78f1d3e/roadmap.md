# Roadmap — Long-Term Planning

## Q3 2026

### Book: 《四倍做多认知，长期做多人生》
- [ ] CI PDF auto-compilation passing (pandoc → xelatex)
- [ ] PR #7 merged to main → Release published
- [ ] 18 illustrations generated and placed in `assets/illustrations/`
- [ ] Full proofreading pass

### Agents infrastructure
- [x] Agent identity system deployed (SHA256 UID → ShortAgentID = last 8 hex)
- [x] Handoff template + naming convention adopted (v2: 4-field metadata)
- [x] Roster simplified (removed device FP, salt rotation, multi-device binding)
- [ ] Sub-agent workflow validated end-to-end
- [ ] CI validation scripts implemented

#### CI validation script schedule
| Script | File | Purpose | Target |
|--------|------|---------|--------|
| Roster validator | `.github/scripts/check_agent_roster.py` | Extract `[ShortAgentID]` from commit messages, cross-check against `agent-roster.md` for ACTIVE status | Q3 2026 |
| Identity binding validator | `.github/scripts/check_agent_binding.py` | Match git committer identity with commit message `[ShortAgentID]` bound Main agent; handle API-push exception | Q3 2026 |
| CI workflow trigger | `.github/workflows/agent-audit.yml` | Run both validators on every PR to `main`; block merge on failure | Q3 2026 |

#### Full sub-agent test workflow
Target: Q3 2026. Exercise the complete lifecycle once:

1. **Register a DRAFT sub-agent**: Main agent creates a test sub-agent entry in `agent-roster.md` with role `ci-test-runner`, status `DRAFT`.
2. **Generate dispatch handoff**: Main agent writes `agents/handoffs/handoff-{sub_id}-{ts}.md` with a simple task (e.g., "count total lines in all `agents/` markdown files").
3. **Sub-agent execution**: Sub-agent reads dispatch handoff, performs task, writes result delivery handoff `agents/handoffs/handoff-{sub_id}-{ts}.md` (Lifecycle Type = Task Result Delivery).
4. **Main agent aggregate**: Main agent reads result handoff, verifies output, adds result to session log.
5. **Promote to ACTIVE**: Main agent updates sub-agent status from `DRAFT` to `ACTIVE`.
6. **Validation**: Verify that the sub-agent `[ShortAgentID]` appears in the result handoff metadata and matches the roster entry.
7. **Cleanup**: Archive test handoff files (or delete if temporary), confirm no git push was attempted by the sub-agent.

## Q4 2026

### Pipeline hardening
- [ ] `docs-checks.yml` (check_links.py, check_style.py) passing
- [ ] CI automatically deploys PDF to Release on every main push

### Content expansion
- [ ] Supplementary appendices (tax, estate planning)
- [ ] English translation of key chapters (optional)

## 2027

### Platform
- [ ] Multi-format output (epub, web)
- [ ] Interactive charts embedded in web version
- [ ] Agent lifecycle automation (auto-validate roster on PR)
