"""PR Language Check — enforces English as the primary language in PR titles and bodies.

Non-English content (e.g. CJK characters, special char blocks) is allowed only as
a minority. The check fails if non-English text dominates the PR title or body.

Ratio thresholds: 40 % for titles (stricter), 50 % for bodies (permissive).
Short boilerplate snippets in other languages will pass; a PR written entirely
in Chinese/Japanese/Korean will be blocked.
"""

import json
import os
import re
import sys


# ── Unicode ranges treated as "non-English" proxies ──────────────────────
CJK     = r'\u4e00-\u9fff\u3400-\u4dbf'          # CJK Unified Ideographs
JP_KANA = r'\u3040-\u309f\u30a0-\u30ff'          # Hiragana + Katakana
HANGUL  = r'\uac00-\ud7af\u1100-\u11ff\u3130-\u318f'  # Hangul
CYRILLIC = r'\u0400-\u04ff\u0500-\u052f'         # Cyrillic
ARABIC  = r'\u0600-\u06ff\u0750-\u077f'          # Arabic
THAI    = r'\u0e00-\u0e7f'                        # Thai

NON_EN_RE = re.compile(
    rf'[{CJK}{JP_KANA}{HANGUL}{CYRILLIC}{ARABIC}{THAI}]'
)

TITLE_MAX = 0.40  # stricter for short title
BODY_MAX  = 0.50  # permissive for longer body


def non_en_ratio(text: str) -> float:
    text = text or ''
    total = len(text)
    if total == 0:
        return 0.0
    return len(NON_EN_RE.findall(text)) / total


def main() -> int:
    event_path = os.environ.get('GITHUB_EVENT_PATH', '')
    title = ''
    body = ''

    if event_path:
        with open(event_path, 'r', encoding='utf-8') as fh:
            event = json.load(fh)
        pr = event.get('pull_request', {})
        title = (pr.get('title') or '').strip()
        body  = (pr.get('body')  or '').strip()

    # env-var fallback for manual testing
    title = title or (os.environ.get('PR_TITLE', '')).strip()
    body  = body  or (os.environ.get('PR_BODY',  '')).strip()

    if not title:
        print('::error::PR title is empty.')
        return 1

    errors = []
    rt = non_en_ratio(title)
    if rt > TITLE_MAX:
        errors.append(
            f'PR title is {rt:.0%} non-English (max {TITLE_MAX:.0%}). '
            'Write the title primarily in English.'
        )

    rb = non_en_ratio(body)
    if rb > BODY_MAX:
        errors.append(
            f'PR body is {rb:.0%} non-English (max {BODY_MAX:.0%}). '
            'Write the body primarily in English.'
        )

    if errors:
        for err in errors:
            print(f'::error::{err}')
        return 1

    print(f'OK — title {rt:.0%} non-EN, body {rb:.0%} non-EN')
    return 0


if __name__ == '__main__':
    sys.exit(main())
