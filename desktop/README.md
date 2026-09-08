# Quadruple Leverage Toolbox — Desktop (Tauri 2 · pnpm-managed)

Local desktop companion for the bilingual web tools in `tools/`. Runs the exact same
HTML pages inside a native window — **no data ever leaves the machine**.

## Stack
- **Tauri 2**: Rust core (`src-tauri/`) + system WebView
- **Commands** are managed with **pnpm** (`@tauri-apps/cli` as devDependency) —
  run everything through pnpm, no direct cargo/tauri-global calls
- **UI**: reuses the repo `tools/` directory directly (`frontendDist: "../../tools"`), zero rewrite
- **Bridge**: tools pages call `window.__TAURI__.core.invoke("export_result", …)` (global Tauri enabled);
  the Export button only appears inside the desktop app, never in plain browsers/gh-pages.

## Run (dev)
```bash
pnpm install     # in desktop/ — installs @tauri-apps/cli (Rust toolchain still required underneath)
pnpm tauri dev   # opens the app window (compiles Rust core on first run)
pnpm tauri build # production .app/.dmg
```

## Features
- v0.1 — native window loading the 10 bilingual tools + index (rust skeleton, PR #43–45)
- v0.2 — `export_result` Rust command: native save dialog + write file; Export button bridged on 10 pages
- v0.3 (planned) — remember-last-input per tool (localStorage persists in WebView), CSV-friendly export

Source chapters of every tool are listed inside each page; all content is hypothetical
teaching material, not investment advice. See `TOOLBOX-ROADMAP.md` at repo root.
