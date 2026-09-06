#!/usr/bin/env python3
"""Inject WebSite + Organization JSON-LD into utility pages that lack top-level ones."""
import io, os, re

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

WEBSITE_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite",'
              '"name":"BPAAU","url":"https://bpaau.org/","inLanguage":"en-AU",'
              '"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint",'
              '"urlTemplate":"https://bpaau.org/?q={search_term_string}"},'
              '"query-input":"required name=search_term_string"}}</script>')

ORG_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization",'
          '"name":"BPAAU","url":"https://bpaau.org/","logo":"https://bpaau.org/assets/logo.png"}</script>')

# Pages that need both WebSite and Organization top-level blocks
NEED_BOTH = [
    "methodology.html", "research.html", "press.html",
]
# Pages that need only WebSite (they already have top-level Organization)
NEED_WEBSITE_ONLY = [
    "about.html", "contact.html", "privacy.html", "terms.html",
    "responsible-gambling.html",
]

def inject(path, blocks):
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        html = f.read()
    # Detect if already has top-level WebSite
    has_website = bool(re.search(r'"@type":\s*"WebSite"', html))
    has_org = bool(re.search(r'"@type":\s*"Organization"', html))
    insert_blocks = []
    if not has_website:
        insert_blocks.append(WEBSITE_LD)
    if "ORG" in blocks and not has_org:
        insert_blocks.append(ORG_LD)
    if not insert_blocks:
        return False
    injection = "".join(insert_blocks)
    # Insert right before <link rel="stylesheet"
    marker = '<link rel="stylesheet" href="/assets/theme.css"/>'
    if marker in html:
        html = html.replace(marker, injection + marker, 1)
    else:
        # fallback: before </head>
        html = html.replace("</head>", injection + "</head>", 1)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    return True

for fn in NEED_BOTH:
    p = os.path.join(PUB, fn)
    ok = inject(p, ["WEB", "ORG"])
    print(f"{fn}: {'injected' if ok else 'already had both'}")

for fn in NEED_WEBSITE_ONLY:
    p = os.path.join(PUB, fn)
    ok = inject(p, ["WEB"])
    print(f"{fn}: {'injected WebSite' if ok else 'already had WebSite'}")
