# -*- coding: utf-8 -*-
import re, os, html, json

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
for p in pages:
    with open(os.path.join("public",p), encoding="utf-8") as f:
        src=f.read()
    print("\n"+"#"*90)
    print("PAGE:",p)
    for m in re.finditer(r'<details class="faq">(.*?)</details>', src, re.S):
        q=re.search(r"<summary>(.*?)</summary>",m.group(1),re.S).group(1)
        b=re.search(r'<div class="faq__body">(.*?)</div>',m.group(1),re.S).group(1)
        print(f"\n  Q: {q}")
        print(f"  A: {b}")
