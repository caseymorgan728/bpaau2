# -*- coding: utf-8 -*-
import re, os, html

pages = [
 "best-high-rtp-pokies-australia-2026.html",
 "free-chips-australia-guide-2026.html",
 "payid-cashouts-australia-2026.html",
 "no-deposit-free-bonus-guide-australia-2026.html",
 "hold-and-win-pokies-australia-2026.html",
 "hot-pokies-australia-2026-popular-slots.html",
 "best-bonus-types-australian-pokies-2026.html",
 "daily-free-credits-au-returning-players.html",
 "biggest-casino-wins-australia-2026.html",
 "how-to-read-casino-bonus-terms-australia-2026.html",
 "high-volatility-vs-high-rtp-free-spins.html",
 "same-day-pokies-withdrawals-australia.html",
]

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return s

for p in pages:
    path = os.path.join("public", p)
    with open(path, encoding="utf-8") as f:
        src = f.read()
    # meta description
    m = re.search(r'<meta content="([^"]*)" name="description"/>', src)
    desc = m.group(1) if m else "NO DESC"
    # body content: strip header/nav/footer/script/style, get text
    body = re.search(r"<main[^>]*>(.*?)</main>", src, re.S)
    bodytxt = strip_tags(body.group(1)) if body else ""
    # remove product grid? keep simple
    words = len(bodytxt.split())
    # FAQs
    details = re.findall(r'<details class="faq">(.*?)</details>', src, re.S)
    faq_info = []
    for d in details:
        q = re.search(r"<summary>(.*?)</summary>", d, re.S)
        qtxt = strip_tags(q.group(1)).strip() if q else "?"
        b = re.search(r'<div class="faq__body">(.*?)</div>', d, re.S)
        btxt = strip_tags(b.group(1)).strip() if b else ""
        faq_info.append((qtxt[:60], len(btxt.split())))
    # JSON-LD FAQPage
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    faq_ld_count = 0
    for l in ld:
        if '"FAQPage"' in l:
            faq_ld_count = l.count('"@type":"Question"')
    print("="*80)
    print(p)
    print(f"  desc_len={len(desc)}  body_words={words}  faq_count={len(details)}  faq_ld_questions={faq_ld_count}")
    for qn, w in faq_info:
        flag = "  <<< THIN/EMPTY" if w < 50 else ""
        print(f"    [{w:3d}w] {qn}{flag}")
