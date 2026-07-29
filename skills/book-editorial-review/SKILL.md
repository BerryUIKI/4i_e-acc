---
name: book-editorial-review
description: >-
  Structural and editorial review of non-fiction book manuscripts before revision.
  This skill should be used when the user asks for an editorial review of a book
  manuscript, manuscript evaluation, book editing feedback, publishing readiness
  assessment, or when they want a professional editor's perspective on their draft.
  The review focuses on book-readability, depth, narrative flow, paragraph style,
  repetition, timelessness, and emotional tone — not line editing or grammar.
agent_created: true
---

# Book Editorial Review

## Purpose

Perform a structural and editorial review of a non-fiction book manuscript before revision. The review evaluates whether the manuscript reads like a published book or like content from other media (blogs, social media, AI-generated explanations). Output follows the format expected by traditional Chinese publishers (e.g. CITIC Press, China Machine Press).

## When to Use

Trigger this skill when:
- The user says "review this manuscript", "editorial review", "编辑审读", "出版社审读"
- The user wants to know if a manuscript is "ready for publication" or "publishing quality"
- The user asks for a "book-level review" rather than grammar/language editing
- The user references this skill by name

## Workflow

### Step 1: Read the entire manuscript

Read every chapter file. Also read the outline (`outline.md` or equivalent) to understand the intended structure and compare it against what was delivered. Note any unfinished chapters.

### Step 2: Evaluate each chapter against 8 criteria

For every completed chapter, apply the evaluation rubric in `references/rubric.md`. Score each criterion and produce a per-chapter verdict.

### Step 3: Identify cross-cutting issues

After evaluating all chapters individually, identify patterns across the manuscript:

1. **Structural repetition** — Which core ideas are repeated across multiple chapters? Count occurrences and identify which chapters contain the "canonical" version.
2. **Template fatigue** — Does every chapter follow the same structure? At what point does the reader stop engaging?
3. **Data vacuum** — Are there any specific numbers, historical data points, or concrete examples? Or is the manuscript entirely abstract?
4. **Missing stories** — Are there real people, companies, or historical events cited? Or only hypothetical examples?
5. **Section redundancy** — Do any recurring sections (e.g. summaries, sidebar columns, Q&A) provide new value or simply restate the chapter?

### Step 4: Score and rank

Produce:
- Per-chapter scores (with verdict: Keep / Minor Revision / Major Rewrite / Rewrite from Scratch)
- Top 5 strongest and weakest chapters
- Chapters that must be rewritten, ranked by priority
- Overall book score

### Step 5: Final verdict

Answer: "If this manuscript were submitted to a major publisher today, would it pass editorial review?"

Choose one:
- **Ready for publication** — Polished, distinctive, data-backed, commercially viable.
- **Needs revision** — Good bones but needs strengthening (more data, less repetition, deeper narrative).
- **Major revision required** — Cannot pass editorial review. Needs structural reorganization, data, stories, and voice work.

## Tone and Style

- Role: Chief editor of a major publishing house (e.g. CITIC Press, China Machine Press).
- Be brutally honest. Do not protect the author's feelings.
- Evaluate by publication quality — assume readers will pay for this book.
- Write in Chinese unless the manuscript is in English.
- Reference comparable published books (e.g. 《金钱心理学》The Psychology of Money, 《漫步华尔街》A Random Walk Down Wall Street) for quality benchmarks.

## Output Format

Detailed format is defined in `references/review-format.md`. The output must include:
- Per-chapter reviews with scores and verdicts
- Cross-cutting issues section
- Overall score with dimension breakdown
- Top 5 strongest and weakest chapters
- Priority-ranked rewrite list
- Final verdict with explanation

Output the review as `EDITORIAL-REVIEW.md` in the manuscript directory.
