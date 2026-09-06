#!/usr/bin/env python3
"""Inject visible <details> FAQ sections on pages that have FAQPage JSON-LD
but no visible FAQ in the body."""
import os, json
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
TARGETS = ["about.html", "methodology.html", "blog/index.html"]

for rel in TARGETS:
    fp = os.path.join(PUB, rel.replace("/", os.sep))
    soup = BeautifulSoup(open(fp, encoding="utf-8").read(), "html.parser")

    # Already has visible FAQ?
    if soup.find("details", class_=lambda c: c and "faq" in c):
        print(f"skip {rel}: already has visible FAQ")
        continue

    # Collect Q/A from JSON-LD
    items = []
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            d = json.loads(s.string or s.get_text())
        except Exception:
            continue
        if d.get("@type") == "FAQPage":
            for q in d.get("mainEntity", []):
                items.append((q["name"], q["acceptedAnswer"]["text"]))
    if not items:
        print(f"skip {rel}: no FAQPage JSON-LD")
        continue

    # Build FAQ section
    out = ['<section class="section">']
    out.append('<div class="section-title"><span class="section-title__label">FAQ</span><h2>Frequently Asked Questions</h2></div>')
    for q, a in items:
        out.append(f'<details class="faq"><summary>{q}</summary><div class="faq__body"><p>{a}</p></div></details>')
    out.append('</section>')
    faq_html = "\n".join(out)

    # Insert before </main>
    main = soup.find("main")
    if main is None:
        print(f"skip {rel}: no main")
        continue
    main.append(BeautifulSoup(faq_html, "html.parser"))

    with open(fp, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"injected FAQ into {rel} ({len(items)} questions)")
