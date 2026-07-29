# DollarHua Brand Reference

> Color and typography specification for PDF toolbook generation.
> Authoritative source: `assets/dollarhua/color_standard.json`

## 8-Color Standard Palette

| Token | Name | Hex | RGB | PDF Usage |
|-------|------|-----|-----|-----------|
| `signature_pink` | Signature Pink | `#FEC6CD` | 254, 198, 205 | 🔑 Primary: chapter title decor lines, page numbers, emphasis |
| `blossom_pink` | Blossom Pink | `#F3A6AF` | 243, 166, 175 | Secondary emphasis, callout borders |
| `amber_gold` | Amber Gold | `#E3A04B` | 227, 160, 75 | Decorative accents (coins, stars), tip box icons |
| `outline_navy` | Bond Navy | `#1D1E50` | 29, 30, 80 | Body text, H1/H2 headings, dark decor bars |
| `pendant_bronze` | Pendant Bronze | `#B86C40` | 184, 108, 64 | Section dividers, coin pendant motifs |
| `warm_skin` | Warm Skin | `#F9DECE` | 249, 222, 206 | Card backgrounds, callout box fills |
| `soft_white` | Soft White | `#FCFDFD` | 252, 253, 253 | Page background, whitespace |
| `contextual_lucky_red` | Lucky Red | `#E85D61` | 232, 93, 97 | Limited: critical warnings, celebration accents |

## PDF Color Mapping

### Cover Page
- **Background:** Signature Pink (`#FEC6CD`) gradient to Blossom Pink (`#F3A6AF`)
- **Title text:** Bond Navy (`#1D1E50`)
- **Subtitle / Date:** Amber Gold (`#E3A04B`)
- **Decor:** Pendant Bronze coin motifs

### Inner Pages
- **Body text:** Bond Navy (`#1D1E50`)
- **Chapter title (H1):** Bond Navy, left Signature Pink vertical rule
- **Section title (H2):** Bond Navy, bottom Signature Pink horizontal rule
- **Page header:** Signature Pink separator line + chapter name / book title
- **Page numbers:** Signature Pink
- **Code block bg:** Soft White (`#FCFDFD`), Bond Navy border
- **Table header:** Signature Pink background + Bond Navy text

### Callout Boxes
- **Warning / Critical:** Lucky Red (`#E85D61`) left border
- **Info / Tip:** Signature Pink left border
- **Example / Case study:** Warm Skin (`#F9DECE`) background

## Typography Spec

| Element | Font | Size | Color |
|---------|------|------|-------|
| Chapter title | PingFang SC Semibold | 18pt | Bond Navy |
| Section title | PingFang SC Semibold | 14pt | Bond Navy |
| Subsection title | PingFang SC Medium | 12pt | Bond Navy |
| Body text | PingFang SC / STSongti | 10.5pt | Bond Navy |
| Code | SF Mono / Menlo | 9pt | Bond Navy |
| Table text | PingFang SC | 9pt | Bond Navy |
| Page header | PingFang SC Light | 8pt | Signature Pink |
| Page number | PingFang SC Medium | 9pt | Signature Pink |

## LaTeX Color Definitions

```tex
\definecolor{dh-pink}{HTML}{FEC6CD}
\definecolor{dh-blossom}{HTML}{F3A6AF}
\definecolor{dh-gold}{HTML}{E3A04B}
\definecolor{dh-navy}{HTML}{1D1E50}
\definecolor{dh-bronze}{HTML}{B86C40}
\definecolor{dh-skin}{HTML}{F9DECE}
\definecolor{dh-white}{HTML}{FCFDFD}
\definecolor{dh-red}{HTML}{E85D61}
```

## Key Rules

1. **Signature Pink (`#FEC6CD`) is the primary identity color** — never displace it as the dominant brand color
2. **Pendant Bronze (`#B86C40`)** — never recolor the coin pendant to bright yellow gold
3. **Bond Navy (`#1D1E50`)** — prefer this over pure black for text and line art
4. **Lucky Red (`#E85D61`)** — use sparingly; never let it dominate Signature Pink
