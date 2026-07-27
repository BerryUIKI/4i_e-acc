# DollarHua (花有财) — Shared IP Character Asset

> English (default) · [中文](./README-zh_CN.md)

A **reusable mascot IP** for this workspace. Use it wherever a friendly, on-brand
visual face is needed — section headers, callouts, social cards, article heroes,
status banners, etc. The character was designed by the repo owner; this folder is
the **single source of truth** for the asset. Always pull from here (not from a
re-downloaded copy) so identity and colors stay consistent.

- **Package:** `DollarHua_AI_Character_Pack_Lite_v1.4`
- **Edition:** Lite · **Version:** v1.4 · **Updated:** 2026-07-19
- **Intended use:** Flexible AI generation for low-complexity / lower-requirement scenarios.

## Identity

| Field | Value |
|-------|-------|
| Name (EN) | DollarHua |
| Name (中文) | 花有财 |
| Nickname | 花花 |
| Role | A cheerful designer who loves wealth and has a hidden feng shui talent. |
| Personality | ENFP — energetic, warm, playful, imaginative, quick to recover. |
| Catchphrase | 包能做的，但要加钱 ("I can do it, but it costs extra.") |
| Appearance | Chibi character with fluffy short white hair, large white cat ears, warm golden starry eyes, pink flower hair accessories, a soft-pink oversized hoodie, a bronze coin pendant, and a brown bead bracelet. |

**Creative freedom** (safe to vary per task): pose, expression, scene, props,
outfit details, lighting, rendering style.

## Color standard

Authoritative tokens — see [`color_standard.json`](./color_standard.json).
`signature_pink` is the **primary identity color** and must not be displaced.

| Token | Name | Hex | Usage | Restriction |
|-------|------|-----|-------|-------------|
| `signature_pink` | Signature Pink | `#FEC6CD` | Hoodie, primary soft-pink fields, friendly emphasis, major brand surfaces. | Do not shift toward saturated magenta or cool purple. |
| `blossom_pink` | Blossom Pink | `#F3A6AF` | Flower accessories, blush, hearts, sticker lettering. | Keep enough contrast from Signature Pink. |
| `amber_gold` | Amber Gold | `#E3A04B` | Iris base, stars, sparkles, prosperity cues. | Keep eye highlights white; no green/blue eyes. |
| `outline_navy` | Outline Navy | `#1D1E50` | Primary line art, dark display text, sticker keylines. | Prefer this navy over pure black. |
| `pendant_bronze` | Pendant Bronze | `#B86C40` | Round pendant, brown bead bracelet, metallic-earth accents. | Do not replace pendant with bright yellow gold. |
| `warm_skin` | Warm Skin | `#F9DECE` | Skin base, soft warm facial rendering. | Keep skin soft/warm; avoid harsh gray shadows. |
| `soft_white` | Soft White | `#FCFDFD` | Hair, ears, clean backgrounds, sticker cutlines. | Use subtle shading; don't flatten all white. |
| `contextual_lucky_red` | Contextual Lucky Red | `#E85D61` | Limited prosperity / warning / celebration / feng shui accents. | Never displace Signature Pink as primary. |

## File map

```
dollarhua/
├── character.json        # Identity, appearance, creative-freedom rules
├── color_standard.json   # 8 authoritative color tokens
├── manifest.json         # Package metadata + per-file SHA-256
├── prompt_seed.txt       # Base generation prompt (start here)
├── references/           # Canonical multi-angle references
│   ├── front.png                 (5.8 MB)
│   ├── front_three_quarter.png
│   ├── front_transparent.png     (transparent bg)
│   ├── left.png
│   ├── right.png
│   ├── back.png
│   └── rear_three_quarter.png
└── examples/             # Expression references
    ├── hello.png
    ├── happy.png
    ├── crying.png
    └── thinking.png
```

### Reference previews

| Front | Three-quarter | Transparent |
|-------|---------------|------------|
| ![front](./references/front.png) | ![three-quarter](./references/front_three_quarter.png) | ![transparent](./references/front_transparent.png) |

### Expression examples

| hello | happy | crying | thinking |
|-------|-------|--------|----------|
| ![hello](./examples/hello.png) | ![happy](./examples/happy.png) | ![crying](./examples/crying.png) | ![thinking](./examples/thinking.png) |

## How to use

1. **Start from the prompt seed:** copy [`prompt_seed.txt`](./prompt_seed.txt) as your
   base prompt, then adapt pose / expression / scene / props / outfit / lighting / style
   per the task (these are explicitly allowed).
2. **Keep the identity stable:** white hair + cat ears, golden starry eyes, pink flower
   accessories, soft-pink hoodie, bronze coin pendant, brown bead bracelet.
3. **Honor the palette:** use the 8 tokens above; never displace `signature_pink` as the
   primary color and never recolor the pendant to bright yellow gold.
4. **Reference images are authoritative** for rendered appearance — when in doubt, match
   them. `front_transparent.png` is the easiest base for compositing.
5. **One source of truth:** link or copy from this folder; do not re-introduce a divergent
   copy elsewhere in the repo.

## Related

- Parent folder: [../README.md](../README.md) · [中文](../README-zh_CN.md)
- Workspace home: [../../README.md](../../README.md) · [中文](../../README-zh_CN.md)
