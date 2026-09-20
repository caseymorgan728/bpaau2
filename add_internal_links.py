# -*- coding: utf-8 -*-
import os
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"

def bcard(href, tag, title, excerpt, img, alt, date, mins):
    return (
'<a class="blog-card" href="/%s">\n'
'<div class="card__media"><img alt="%s" decoding="async" height="784" loading="lazy" src="%s" width="1168"/></div>\n'
'<div class="blog-card__body">\n'
'<span class="card__tag">%s</span>\n'
'<h3>%s</h3>\n'
'<p class="card__excerpt">%s</p>\n'
'<p class="blog-card__meta">%s · %s min read · Read the guide &rarr;</p>\n'
'</div>\n</a>\n'
    ) % (href, alt, img, tag, title, excerpt, date, mins)

FREE50 = bcard("free-50-pokies-no-deposit-sign-up-bonus-australia-2026","Bonus Guides",
 "Free $50 Pokies No Deposit Sign-Up Bonus Australia 2026",
 "How the A$50 no-deposit sign-up chip works &mdash; real wagering, max-cashout and PayID payout rules, plus operators with up to $199 sign-up credit.",
 "/blog%20banner/blogpost%2012.webp","Free $50 pokies no deposit sign up bonus Australia","2026-09-21","5")
WOLF = bcard("wolf-treasure-pokies-australia-2026","Top Pokies",
 "Wolf Treasure Pokies Australia 2026 &mdash; Free Spins &amp; Jackpot Guide",
 "How the golden-moon Money Respin and Mini/Major/Mega jackpots work, and where to claim Wolf Treasure free spins with no deposit.",
 "/blog%20banner/for%20blogpost%201%20and%206.webp","Wolf Treasure pokies Australia free spins","2026-09-21","5")
PAYIDNV = bcard("payid-pokies-no-verification-australia-2026","Fast Cashouts",
 "PayID Pokies No Verification Australia 2026 &mdash; The Truth About KYC",
 "What no-KYC pokies really mean, why licensed casinos verify before payout, and how to make first PayID withdrawals near-instant.",
 "/blog%20banner/blogpost%208.webp","PayID pokies no verification Australia","2026-09-21","5")

jobs = [
 ("no-deposit-free-bonus-guide-australia-2026.html", ["free-50-pokies","wolf-treasure-pokies"], FREE50+WOLF),
 ("payid-cashouts-australia-2026.html", ["payid-pokies-no-verification"], PAYIDNV),
 ("hot-pokies-australia-2026-popular-slots.html", ["wolf-treasure-pokies"], WOLF),
 ("hold-and-win-pokies-australia-2026.html", ["wolf-treasure-pokies"], WOLF),
]

for fname, needles, block in jobs:
    p = os.path.join(PUB, fname)
    s = open(p, encoding="utf-8").read()
    missing = [n for n in needles if ("/"+n) not in s]
    if not missing:
        print("already linked:", fname); continue
    marker = '<div class="blog-card-grid">'
    idx = s.find(marker)
    if idx < 0:
        print("NO GRID:", fname); continue
    pos = idx + len(marker)
    s = s[:pos] + "\n" + block + s[pos:]
    open(p, "w", encoding="utf-8").write(s)
    print("linked in", fname, "->", [m.split('-pokies')[0] for m in missing])
print("done")
