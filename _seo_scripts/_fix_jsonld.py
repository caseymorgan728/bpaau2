# -*- coding: utf-8 -*-
"""Repair broken FAQPage JSON-LD on 4 pages by rebuilding from visible <details>."""
import re, json, html, os

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"
FILES = [
    "blog/index.html",
    "curacao-casino-licence-check-australia-2026.html",
    "fastest-withdrawal-casinos-australia-under-1-hour-2026.html",
    "mobile-pokies-australia-2026.html",
]

def strip_tags(s):
    # remove tags
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

for rel in FILES:
    path = os.path.join(PUB, rel.replace("/", os.sep))
    txt = open(path, encoding="utf-8").read()

    # Find all visible <details class="faq">...<summary>Q</summary><div class="faq__body">A</div></details>
    details = re.findall(
        r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<div[^>]*class="faq__body"[^>]*>(.*?)</div>\s*</details>',
        txt, re.S)
    if not details:
        # fallback: generic details/summary
        details = re.findall(r"<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>", txt, re.S)

    entities = []
    for q, a in details:
        qt = strip_tags(q)
        at = strip_tags(a)
        entities.append({
            "@type": "Question",
            "name": qt,
            "acceptedAnswer": {"@type": "Answer", "text": at},
        })

    new_block = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    new_json = json.dumps(new_block, ensure_ascii=False)
    new_script = '<script type="application/ld+json">' + new_json + "</script>"

    # Replace the existing FAQPage script block (may be broken).
    # Find every ld+json script block; pick the one containing FAQPage.
    def repl(m):
        body = m.group(1)
        if '"FAQPage"' in body:
            return new_script
        return m.group(0)
    txt2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, txt, flags=re.S)
    if txt2 == txt:
        print("NO FAQ BLOCK REPLACED in", rel)
        continue
    open(path, "w", encoding="utf-8").write(txt2)
    print(f"FIXED {rel}: {len(entities)} questions rebuilt")

print("DONE")
