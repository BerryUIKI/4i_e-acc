# Quadruple Leverage Toolbox — Desktop (Tauri 2 + Rust)

Local desktop companion for the bilingual web tools in `tools/`. Runs the exact same
HTML pages inside a native window — no data ever leaves the machine.

## Stack
- **Rust** (`desktop/src-tauri`) — Tauri 2 shell + commands
- **Frontend**: reuses the repo `tools/` directory directly (`frontendDist: "../../tools"`), zero rewrite
- **Icon**: generated brand icon (navy / pink flower / bronze coin), see `icons/icon.png`

## Run (dev)
```bash
cargo run --manifest-path desktop/src-tauri/Cargo.toml
```
Requires Rust toolchain + Xcode CLT on macOS.

## Roadmap
- v0.1: shell + reuse of 10 bilingual tools (current)
- v0.2: per-tool parameter persistence (localStorage already persists in WebView) + CSV export via Rust command + save dialog
- v0.3: optional BlueWhale / AlphaForge data bridging (Rust side)

Source chapters of every tool are listed inside each page; all content is hypothetical
teaching material, not investment advice. See `TOOLBOX-ROADMAP.md` at repo root.
