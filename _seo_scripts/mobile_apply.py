#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply mobile-audit HTML fixes across all public pages. Idempotent."""
import os, re, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

CTA_HTML = (
    '<a class="back-to-top" href="#top" aria-label="Back to top">&#8593;</a>\n'
    '<div class="mobile-cta">'
    '<a class="btn btn--primary btn--block" href="https://1xaud.com/register" '
    'rel="sponsored nofollow noopener" target="_blank">Claim Free $199 Bonus</a>'
    '</div>\n'
)

files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
changed = []

for f in files:
    relp = os.path.relpath(f, ROOT)
    if "google" in os.path.basename(f):
        continue  # verification stub, no chrome
    raw = open(f, "r", encoding="utf-8").read()
    orig = raw
    notes = []

    # 1) viewport-fit=cover
    if "viewport-fit=cover" not in raw:
        raw2 = raw.replace("width=device-width, initial-scale=1",
                           "width=device-width, initial-scale=1, viewport-fit=cover")
        if raw2 != raw:
            raw = raw2; notes.append("viewport-fit=cover")

    # 2) id="top" on body
    if 'id="top"' not in raw:
        raw2 = re.sub(r"<body>", '<body id="top">', raw, count=1)
        if raw2 != raw:
            raw = raw2; notes.append("body#top")

    # 3) nav backdrop (as sibling of #nav-toggle, inside header-inner)
    if "nav-backdrop" not in raw:
        raw2 = re.sub(r'(</nav>)(\s*</div>\s*</div>\s*</header>)',
                      r'\1\n<div class="nav-backdrop"></div>\2', raw, count=1)
        if raw2 != raw:
            raw = raw2; notes.append("nav-backdrop")

    # 4) wrap tables in .table-wrap
    if "table-wrap" not in raw:
        def _wrap(m):
            return '<div class="table-wrap">' + m.group(0) + '</div>'
        raw2 = re.sub(r'<table\b[^>]*>.*?</table>', _wrap, raw, flags=re.S|re.I)
        if raw2 != raw:
            raw = raw2; notes.append("table-wrap")

    # 5) sticky CTA + back-to-top before </body>
    if "mobile-cta" not in raw:
        raw2 = raw.replace("</body>", CTA_HTML + "</body>", 1)
        if raw2 != raw:
            raw = raw2; notes.append("cta+btt")

    if raw != orig:
        open(f, "w", encoding="utf-8").write(raw)
        changed.append((relp, notes))

print(f"Modified {len(changed)} files:\n")
for relp, notes in changed:
    print(f"  {relp:55} -> {', '.join(notes)}")
