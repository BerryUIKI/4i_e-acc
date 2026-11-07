#!/usr/bin/env python3
"""Build 16:9 screen-format presentation decks from the book manuscript.

One PDF per book part, so each part can be presented on its own.

Usage (from the repository root):
    python skills/screen-deck/scripts/build_decks.py
    python skills/screen-deck/scripts/build_decks.py --part A --part B
    python skills/screen-deck/scripts/build_decks.py --html-only

Output: output/decks/<part-letter>-<slug>.pdf
HTML intermediates: output/decks/html/
"""

from __future__ import annotations

import argparse
import html as htmllib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / "articles" / "2026-quadruple-long-life"
FONTS = ROOT / "skills" / "pdf-toolbook" / "assets" / "fonts"
INDEX = ROOT / "book-task.md"
OUT_DIR = ROOT / "output" / "decks"
CHARTS = OUT_DIR / "charts"

# Part letter -> (number, Chinese title, English subtitle)
PARTS: dict[str, tuple[str, str, str]] = {
    "FM": ("00", "开篇", "Before We Begin"),
    "A": ("01", "先看清自己的财务生活", "See Your Finances Clearly First"),
    "B": ("02", "理解收益、复利与风险", "Returns, Compounding and Risk"),
    "C": ("03", "钱到底可以放在哪里", "Where Money Can Live"),
    "D": ("04", "ETF 与基金的完整操作逻辑", "ETFs and Funds, End to End"),
    "E": ("05", "家庭资产配置", "Household Asset Allocation"),
    "F": ("06", "真正开始投资", "Actually Start Investing"),
    "G": ("07", "面对市场周期与人性", "Cycles and Human Nature"),
    "I": ("08", "使用 AI 管理你的财务计划", "AI for Your Financial Plan"),
    "H": ("09", "终章 · 财富的作用", "The Point of It All"),
}

PART_ORDER = ["FM", "A", "B", "C", "D", "E", "F", "G", "I", "H"]


# ---------------------------------------------------------------- parsing


def parse_index(text: str) -> list[dict]:
    """Return [{num, title, path, part}] from book-task.md."""
    entries = []
    for line in text.splitlines():
        m = re.match(r"^\s*(\d+)\.\s*\[([^\]]+)\]\(([^)]+)\)", line)
        if not m:
            continue
        path = BOOK.parent.parent / m.group(3)
        name = Path(m.group(3)).name
        pm = re.match(r"^([A-Z]+)\d{3}-", name)
        part = pm.group(1) if pm else "H"
        entries.append(
            {"num": int(m.group(1)), "title": m.group(2), "path": path, "part": part}
        )
    return entries


def split_sections(body: str) -> tuple[str, str, list[tuple[str, str]]]:
    """Split a chapter into (title, epigraph, [(section_title, section_body)])."""
    lines = body.splitlines()

    title = ""
    for i, line in enumerate(lines):
        if line.startswith("## "):
            title = line[3:].strip()
            lines = lines[i + 1 :]
            break

    epigraph = ""
    ep_match = re.search(r"^>\s*(.+)$", "\n".join(lines), re.MULTILINE)
    if ep_match and lines and any(l.strip().startswith(">") for l in lines[:8]):
        # take only the first blockquote that appears before the first ###
        head = "\n".join(lines).split("### ")[0]
        bq = re.search(r"^>\s*\*\*(.+?)\*\*", head, re.MULTILINE) or re.search(
            r"^>\s*(.+)$", head, re.MULTILINE
        )
        if bq:
            epigraph = bq.group(1).strip()
            epigraph = epigraph.replace("**", "")

    sections: list[tuple[str, str]] = []
    current_title, buf = "", []
    for line in lines:
        if line.startswith("### "):
            if buf:
                sections.append((current_title, "\n".join(buf)))
            current_title = line[4:].strip()
            buf = []
        elif line.startswith("## "):
            continue
        else:
            buf.append(line)
    if buf:
        sections.append((current_title, "\n".join(buf)))
    return title, epigraph, sections


def paragraphs(block: str) -> list[str]:
    """Split a markdown block into cleaned paragraph strings."""
    out = []
    for raw in re.split(r"\n\s*\n", block):
        p = raw.strip()
        if not p or p == "---" or p.startswith("```"):
            continue
        if p.startswith("|"):
            continue
        p = re.sub(r"^>\s?", "", p, flags=re.MULTILINE).strip()
        # Inline emphasis is carried by the layout (claim line, lead paragraph),
        # so drop the markers rather than trying to balance them across slides.
        p = p.replace("**", "")
        if p:
            out.append(p)
    return out


def sentences(text: str) -> list[str]:
    """Split Chinese prose into sentences with balanced bold markers."""
    parts = re.split(r"(?<=[。！？])", text)
    out: list[str] = []
    carry_bold = False
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # A ** pair split across a sentence boundary would render literally;
        # rebalance so each piece carries whole emphasis runs.
        if carry_bold:
            p = "**" + p
        if p.count("**") % 2:
            p = p + "**"
            carry_bold = True
        else:
            carry_bold = False
        out.append(p)
    return out


def strip_markdown(text: str) -> str:
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.strip()


def inline_markup(text: str, esc: bool = True) -> str:
    """Escape, then apply Chinese quote glyphs to prose."""
    t = htmllib.escape(text) if esc else text
    t = re.sub(r'"([^"\n]*[㐀-鿿][^"\n]*)"', r"“\1”", t)
    return t


def is_short_claim(sentence: str) -> bool:
    return 8 <= len(sentence) <= 34 and not sentence.startswith(("（", "("))


# ---------------------------------------------------------------- slides


def el(tag: str, cls: str = "", inner: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c}>{inner}</{tag}>"


def slide(inner: str, extra: str = "", kind: str = "") -> str:
    cls = "slide" + (f" {kind}" if kind else "")
    return f'<section class="{cls}" {extra}>{inner}</section>'


def part_opener(part: str, chapters: list[dict]) -> str:
    num, name, en = PARTS[part]
    inner = f"""
      <div class="part-num">{num}</div>
      <div class="part-body">
        <div class="eyebrow">{en}</div>
        <h1 class="part-title">{htmllib.escape(name)}</h1>
        <div class="rule"></div>
        <div class="part-meta">{len(chapters)} 章 · 四倍做多认知，长期做多人生</div>
      </div>"""
    return slide(inner, kind="cover")


def deck_toc(part: str, chapters: list[dict]) -> str:
    items = []
    for i, ch in enumerate(chapters, 1):
        title = re.sub(r"^第.+?章\s*·\s*", "", ch["title"])
        items.append(
            f'<li><span class="toc-n">{i:02d}</span>'
            f'<span class="toc-t">{htmllib.escape(title)}</span></li>'
        )
    inner = f"""
      <div class="eyebrow">Contents</div>
      <h2 class="toc-title">本册目录</h2>
      <ol class="toc-list">{''.join(items)}</ol>"""
    return slide(inner, kind="toc")


def chapter_opener(num: str, title: str, epigraph: str) -> str:
    ep = (
        f'<p class="epigraph">{inline_markup(epigraph)}</p>' if epigraph else ""
    )
    inner = f"""
      <div class="chap-ghost">{num}</div>
      <div class="chap-body">
        <div class="eyebrow">第 {int(num)} 章</div>
        <h2 class="chap-title">{htmllib.escape(title)}</h2>
        {ep}
      </div>"""
    return slide(inner, kind="chapter")


def section_lead(title: str, first: str) -> str:
    """Section opener: the heading plus its opening statement, set large."""
    body = sentences(first)
    lead = body[0] if body else first
    inner = f"""
      <div class="eyebrow">Section</div>
      <h3 class="lead-h">{htmllib.escape(title)}</h3>
      <p class="lead-p">{inline_markup(lead)}</p>"""
    return slide(inner, kind="lead")


def content_slide(text: str, section: str, index: int) -> str:
    """One idea per slide: a claim line plus the supporting prose."""
    sents = sentences(text)
    claim, rest = "", sents
    if sents and is_short_claim(strip_markdown(sents[0])):
        claim, rest = strip_markdown(sents[0]), sents[1:]
    body = "".join(rest) if rest else strip_markdown(text)
    claim_html = (
        f'<p class="claim">{inline_markup(claim)}</p>' if claim else ""
    )
    inner = f"""
      <div class="slide-head"><span class="sh-sec">{htmllib.escape(section)}</span></div>
      {claim_html}
      <p class="body">{inline_markup(body)}</p>"""
    return slide(inner, kind="content")


def split_long(body: str, limit: int = 112) -> list[str]:
    """Break one paragraph into slide-sized pieces at sentence boundaries."""
    sents = sentences(body)
    chunks: list[str] = []
    buf = ""
    for s in sents:
        cand = buf + s
        if buf and len(strip_markdown(cand)) > limit:
            chunks.append(buf)
            buf = s
        else:
            buf = cand
    if buf:
        chunks.append(buf)
    return chunks or [body]


def content_slides(text: str, section: str) -> list[str]:
    """Emit one or more content slides for a paragraph."""
    sents = sentences(text)
    claim, rest = "", sents
    if sents and is_short_claim(strip_markdown(sents[0])):
        claim, rest = strip_markdown(sents[0]), sents[1:]

    body_sents = rest if rest else sents
    merged = "".join(body_sents)

    if len(strip_markdown(merged)) <= 112 and claim:
        return [content_slide(text, section, 0)]

    pieces = split_long(merged)
    out: list[str] = []
    for i, piece in enumerate(pieces):
        this_claim = claim if i == 0 else ""
        claim_html = (
            f'<p class="claim">{inline_markup(this_claim)}</p>'
            if this_claim
            else ""
        )
        inner = f"""
      <div class="slide-head"><span class="sh-sec">{htmllib.escape(section)}</span></div>
      {claim_html}
      <p class="body">{inline_markup(piece)}</p>"""
        out.append(slide(inner, kind="content"))
    return out



def quote_slide(text: str) -> str:
    inner = f"""
      <div class="quote-mark">“</div>
      <blockquote>{inline_markup(text)}</blockquote>"""
    return slide(inner, kind="quote")


def figure_slide(src: str, alt: str, part: str, caption: str = "") -> str:
    """Full-bleed chart slide; deck charts already carry title + takeaway."""
    name = Path(src).name
    redrawn = CHARTS / name.replace("_", "-")
    if redrawn.exists():
        uri = redrawn.as_posix()
    else:
        rel = src
        if rel.startswith("../"):
            rel = "articles/2026-quadruple-long-life/" + rel[3:]
        elif not rel.startswith(("http", "/")):
            rel = str((BOOK / rel).relative_to(ROOT))
        uri = (ROOT / rel).as_posix()
    cap = f'<figcaption>{htmllib.escape(caption)}</figcaption>' if caption else ""
    inner = f"""
      <div class="fig-wrap">
        <img src="file:///{uri}" alt="{htmllib.escape(alt)}">
      </div>
      {cap}"""
    return slide(inner, kind="figure")



def closing_slide(part: str) -> str:
    num, name, en = PARTS[part]
    inner = f"""
      <div class="closing-body">
        <div class="rule"></div>
        <p class="closing-t">{htmllib.escape(en)}</p>
        <p class="closing-s">四倍做多认知，长期做多人生</p>
      </div>"""
    return slide(inner, kind="cover closing")


# ---------------------------------------------------------------- chapter


def build_chapter(ch: dict, part: str) -> list[str]:
    body = ch["path"].read_text(encoding="utf-8")
    title, epigraph, sections = split_sections(body)

    clean_title = re.sub(r"^第.+?章\s*·\s*", "", title or ch["title"])
    num_m = re.search(r"第(\w+?)章", ch["title"])
    cn_num = num_m.group(1) if num_m else "1"
    arabic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
              "八": 8, "九": 9, "十": 10}.get(cn_num[0], 1)
    if len(cn_num) > 1:
        arabic = 10 + {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
                       "六": 6, "七": 7, "八": 8, "九": 9}.get(cn_num[1], 0)
    chapter_num = f"{arabic:02d}"

    slides = [chapter_opener(chapter_num, clean_title, epigraph)]

    for sec_title, sec_body in sections:
        paras = paragraphs(sec_body)
        if not paras:
            continue

        # images anywhere in the section become their own figures
        imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", sec_body)
        for alt, src in imgs:
            slides.append(figure_slide(src, alt, part))
        if imgs:
            paras = [
                p for p in paras if not re.search(r"!\[[^\]]*\]\([^)]+\)", p)
            ]
            if not paras:
                continue

        if sec_title:
            slides.append(section_lead(sec_title, paras[0]))
            paras = paras[1:]

        for i, p in enumerate(paras):
            if p.strip().startswith("（来源") or p.strip().startswith("来源："):
                continue  # provenance notes belong to the book, not the deck
            slides.extend(content_slides(p, sec_title or clean_title))

    return slides


# ---------------------------------------------------------------- styles


CSS = """
@font-face{font-family:"HSerif";src:url("@F@SourceHanSerifSC-Regular.otf");
  font-weight:400;font-display:block}
@font-face{font-family:"HSerif";src:url("@F@SourceHanSerifSC-Bold.otf");
  font-weight:700;font-display:block}
@font-face{font-family:"HSans";src:url("@F@SourceHanSansSC-Light.otf");
  font-weight:300;font-display:block}
@font-face{font-family:"HSans";src:url("@F@SourceHanSansSC-Regular.otf");
  font-weight:400;font-display:block}
@font-face{font-family:"HSans";src:url("@F@SourceHanSansSC-Medium.otf");
  font-weight:500;font-display:block}
@font-face{font-family:"HSans";src:url("@F@SourceHanSansSC-Bold.otf");
  font-weight:700;font-display:block}

:root{
  --cream:#FBF7F0; --paper:#FFFDFA;
  --navy:#1D1E50; --navy-soft:#4A4B78; --navy-faint:#8B8CAE;
  --pink:#FEC6CD; --blossom:#F3A6AF; --bronze:#B86C40; --rule:#E2DED6;
}
*{margin:0;padding:0;box-sizing:border-box}
@page{size:13.333in 7.5in;margin:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"HSans",sans-serif;background:var(--cream);color:var(--navy);
  font-feature-settings:"palt" 1}

.slide{width:13.333in;height:7.5in;position:relative;overflow:hidden;
  page-break-after:always;break-after:page;background:var(--cream);
  padding:0.85in 0.95in;display:flex;flex-direction:column;
  justify-content:center}
.slide:last-child{page-break-after:auto;break-after:auto}

/* ---- eyebrow ---- */
.eyebrow{font-family:"HSans";font-weight:500;font-size:11.5pt;letter-spacing:.22em;
  text-transform:uppercase;color:var(--bronze);margin-bottom:18pt}
.rule{width:74pt;height:1.5pt;background:var(--blossom);margin:22pt 0}

/* ---- cover ---- */
.cover{background:var(--navy);color:var(--cream);justify-content:center}
.cover .part-num{position:absolute;right:-0.02in;top:-0.55in;
  font-family:"HSans";font-weight:300;font-size:300pt;line-height:1;
  color:rgba(254,198,205,.10);letter-spacing:-.02em}
.cover .part-body{position:relative;z-index:2;max-width:8.4in}
.cover .eyebrow{color:var(--blossom)}
.cover .rule{background:var(--blossom);width:96pt}
.part-title{font-family:"HSerif";font-weight:700;font-size:46pt;line-height:1.35;
  letter-spacing:.01em}
.part-meta{font-size:13pt;font-weight:300;color:var(--navy-faint);
  letter-spacing:.06em}
.closing{background:var(--navy);color:var(--cream);align-items:flex-start}
.closing-body{padding-left:0.1in}
.closing .rule{background:var(--blossom)}
.closing-t{font-family:"HSerif";font-size:34pt;line-height:1.4;color:var(--cream)}
.closing-s{margin-top:14pt;font-size:13pt;font-weight:300;color:var(--navy-faint);
  letter-spacing:.1em}

/* ---- toc ---- */
.toc-title{font-family:"HSerif";font-weight:700;font-size:32pt;margin-bottom:26pt}
.toc-list{list-style:none;column-count:2;column-gap:0.9in}
.toc-list li{display:flex;gap:14pt;align-items:baseline;padding:7pt 0;
  border-bottom:.6pt solid var(--rule);break-inside:avoid}
.toc-n{font-size:10pt;font-weight:500;color:var(--bronze);letter-spacing:.1em}
.toc-t{font-size:15pt;font-weight:400;color:var(--navy)}

/* ---- chapter ---- */
.chapter{justify-content:center}
.chap-ghost{position:absolute;right:0.7in;top:0.25in;font-family:"HSerif";
  font-size:250pt;font-weight:700;line-height:1;color:rgba(29,30,80,.055)}
.chap-body{position:relative;z-index:2;max-width:8.6in}
.chap-title{font-family:"HSerif";font-weight:700;font-size:44pt;line-height:1.35}
.epigraph{margin-top:26pt;padding-left:20pt;border-left:2pt solid var(--blossom);
  font-family:"HSerif";font-size:16pt;line-height:1.85;color:var(--navy-soft);
  font-style:italic;max-width:7.6in}

/* ---- section lead ---- */
.lead{justify-content:center}
.lead-h{font-family:"HSerif";font-weight:700;font-size:34pt;line-height:1.35;
  max-width:9in;margin-bottom:24pt}
.lead-p{font-family:"HSerif";font-size:22pt;line-height:1.85;color:var(--navy);
  max-width:9.4in}

/* ---- content ---- */
.content{justify-content:center}
.content::before{content:"";position:absolute;left:0.95in;top:1.7in;bottom:1.7in;
  width:2pt;background:linear-gradient(180deg,var(--blossom),var(--pink) 65%,transparent)}
.content .slide-head,.content .claim,.content .body{padding-left:30pt}
.content .body{margin-top:4pt}
.slide-head{margin-bottom:20pt}
.sh-sec{font-size:11pt;font-weight:500;letter-spacing:.14em;color:var(--bronze);
  text-transform:uppercase}
.claim{font-family:"HSerif";font-weight:700;font-size:28pt;line-height:1.6;
  color:var(--navy);margin-bottom:22pt;max-width:10.2in}
.body{font-family:"HSerif";font-size:22pt;line-height:1.95;color:var(--navy-soft);
  max-width:10.2in}
.content .body:only-of-type{font-size:23pt}

/* ---- quote ---- */
.quote{background:var(--navy);color:var(--cream);justify-content:center;
  padding-left:1.5in;padding-right:1.5in}
.quote-mark{font-family:"HSerif";font-size:120pt;line-height:.7;color:var(--blossom);
  opacity:.5;margin-bottom:12pt}
blockquote{font-family:"HSerif";font-size:28pt;line-height:1.75;color:var(--cream);
  font-style:italic}

/* ---- figure ---- */
.figure{justify-content:center;align-items:center;padding:0.30in 0.38in}
.fig-wrap{flex:1;display:flex;align-items:center;justify-content:center;
  width:100%;min-height:0}
.fig-wrap img{max-width:100%;max-height:6.9in;object-fit:contain}
figcaption{margin-top:14pt;font-size:11.5pt;color:var(--navy-faint);
  letter-spacing:.04em;text-align:center}

/* ---- page number ---- */
.pgno{position:absolute;right:0.62in;bottom:0.42in;font-size:9.5pt;
  font-weight:400;color:var(--navy-faint);letter-spacing:.12em}
.cover .pgno,.quote .pgno{color:rgba(251,247,240,.42)}
"""


def render_html(part: str, chapters: list[dict], slides: list[str], out: Path) -> None:
    font_dir = FONTS.as_posix()
    css = CSS.replace("@F@", f"file:///{font_dir}/")
    body = []
    for i, s in enumerate(slides, 1):
        pg = f'<div class="pgno">{i:02d}</div>'
        body.append(s[:-len("</section>")] + pg + "</section>")
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{htmllib.escape(PARTS[part][1])} · 四倍做多认知</title>
<style>{css}</style></head>
<body>
{''.join(body)}
</body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


# ---------------------------------------------------------------- driver


def find_chrome() -> str | None:
    for p in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    ]:
        if Path(p).exists():
            return p
    return None


def to_pdf(chrome: str, src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        f"--print-to-pdf={dst}",
        src.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return dst.exists() and dst.stat().st_size > 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--part", action="append", help="limit to these part letters")
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"error: {INDEX} not found", file=sys.stderr)
        return 1

    entries = parse_index(INDEX.read_text(encoding="utf-8"))

    by_part: dict[str, list[dict]] = {}
    for e in entries:
        if "目录" in e["title"]:
            continue
        by_part.setdefault(e["part"], []).append(e)

    # Appendices stay in the book's print edition; the decks cover the talk.
    parts = [p for p in PART_ORDER if p in by_part]
    if args.part:
        parts = [p for p in parts if p in set(args.part)]

    chrome = None if args.html_only else find_chrome()
    if not args.html_only and not chrome:
        print("error: no Chrome/Edge found for PDF rendering", file=sys.stderr)
        return 1

    total = 0
    for part in parts:
        chapters = by_part[part]
        num, name, _en = PARTS.get(part, ("00", part, ""))
        slug = re.sub(r"[^a-z0-9]+", "-", f"{part}{num}".lower()).strip("-")
        slides = [part_opener(part, chapters), deck_toc(part, chapters)]
        for ch in chapters:
            slides.extend(build_chapter(ch, part))
        slides.append(closing_slide(part))

        html_path = OUT_DIR / "html" / f"{slug}.html"
        render_html(part, chapters, slides, html_path)

        if args.html_only:
            print(f"  HTML  {html_path.relative_to(ROOT)}  ({len(slides)} slides)")
            total += len(slides)
            continue

        pdf_path = OUT_DIR / f"{slug}.pdf"
        ok = to_pdf(chrome, html_path.resolve(), pdf_path.resolve())
        mark = "OK " if ok else "FAIL"
        size = f"{pdf_path.stat().st_size / 1048576:.1f} MB" if ok else ""
        print(f"  {mark} {pdf_path.name:<22} {len(slides):>4} slides  {size}")
        total += len(slides)

    print(f"\n{total} slides across {len(parts)} deck(s) -> output/decks/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
