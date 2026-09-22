# -*- coding: utf-8 -*-
"""Wire the new no-deposit bonus codes page into hub, category and related guides."""
import os
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
SLUG = "no-deposit-bonus-codes-australia-2026"

def hub_card(indent=""):
    return (
'{i}<article class="card">\n'
'{i}<div class="card__media">\n'
'{i}<img alt="No deposit bonus codes Australia 2026 free pokies coupons" decoding="async" height="400" loading="lazy" src="/blog%20banner/blogpost%204.webp" width="600"/>\n'
'{i}</div>\n'
'{i}<div class="card__body">\n'
'{i}<span class="card__tag">NO DEPOSIT</span>\n'
'{i}<h2 class="card__title"><a href="/{h}">No Deposit Bonus Codes Australia 2026 &mdash; Free Pokies Coupons</a></h2>\n'
'{i}<p class="card__excerpt">How free pokies bonus codes really work, why most coupons expire, the wagering and max-cashout rules to check, and verified sign-up free credit up to $199 that needs no code at all.</p>\n'
'{i}<a class="btn btn--primary btn--small" href="/{h}">Read Article</a>\n'
'{i}</div>\n'
'{i}</article>\n'
    ).format(i=indent, h=SLUG)

def bcard():
    return (
'<a class="blog-card" href="/%s">\n'
'<div class="card__media"><img alt="No deposit bonus codes Australia 2026 free pokies coupons" decoding="async" height="784" loading="lazy" src="/blog%%20banner/blogpost%%204.webp" width="1168"/></div>\n'
'<div class="blog-card__body">\n'
'<span class="card__tag">Bonus Guides</span>\n'
'<h3>No Deposit Bonus Codes Australia 2026: Free Pokies Coupons</h3>\n'
'<p class="card__excerpt">How free pokies coupon codes work, why most expire or fail, the five terms that decide a payout, and verified sign-up credit up to $199 &mdash; no code needed.</p>\n'
'<p class="blog-card__meta">2026-09-22 · 6 min read · Read the guide &rarr;</p>\n'
'</div>\n</a>\n'
    ) % SLUG

def insert_hub(rel, indent):
    p = os.path.join(PUB, rel)
    s = open(p, encoding="utf-8").read()
    if ("/" + SLUG) in s:
        print("SKIP already:", rel); return
    marker = indent + '<article class="card">'
    idx = s.find(marker)
    if idx < 0:
        print("MARKER NOT FOUND:", rel); return
    s = s[:idx] + hub_card(indent) + s[idx:]
    open(p, "w", encoding="utf-8").write(s)
    print("hub/category card ->", rel)

def insert_related(rel):
    p = os.path.join(PUB, rel)
    s = open(p, encoding="utf-8").read()
    if ("/" + SLUG) in s:
        print("SKIP already:", rel); return
    marker = '<div class="blog-card-grid">'
    idx = s.find(marker)
    if idx < 0:
        print("NO GRID:", rel); return
    pos = idx + len(marker)
    s = s[:pos] + "\n" + bcard() + s[pos:]
    open(p, "w", encoding="utf-8").write(s)
    print("related card ->", rel)

insert_hub(os.path.join("blog", "index.html"), "")
insert_hub(os.path.join("blog", "bonus-guides", "index.html"), "    ")
for rel in [
    "no-deposit-free-bonus-guide-australia-2026.html",
    "free-chips-australia-guide-2026.html",
    "free-50-pokies-no-deposit-sign-up-bonus-australia-2026.html",
]:
    insert_related(rel)
print("done")
