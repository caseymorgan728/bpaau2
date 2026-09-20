# -*- coding: utf-8 -*-
import os
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
SLUG = "pokies-tournaments-australia-2026"
IMG = "/blog%20banner/blogpost%2011.webp"
ALT = "Australian online pokies tournaments and slot leaderboard guide"
TITLE = "Pokies Tournaments Australia 2026 &mdash; Slot Leaderboard Guide"
EXCERPT_HUB = ("How online pokies tournaments and slot leaderboards work for Australian players &mdash; "
               "free-roll vs buy-in entry, scoring, prize pools, and PayID payout of leaderboard winnings.")
EXCERPT_REL = ("How slot leaderboards work for Australian players &mdash; free-roll vs buy-in entry, "
               "scoring, prize pools and PayID payout of tournament winnings.")

def hub_card(indent=""):
    return (
    '{i}<article class="card">\n'
    '{i}<div class="card__media">\n'
    '{i}<img alt="{alt}" decoding="async" height="400" loading="lazy" src="{img}" width="600"/>\n'
    '{i}</div>\n'
    '{i}<div class="card__body">\n'
    '{i}<span class="card__tag">TOP POKIES</span>\n'
    '{i}<h2 class="card__title"><a href="/{href}">{title}</a></h2>\n'
    '{i}<p class="card__excerpt">{ex}</p>\n'
    '{i}<a class="btn btn--primary btn--small" href="/{href}">Read Article</a>\n'
    '{i}</div>\n'
    '{i}</article>\n'
    ).format(i=indent, alt=ALT, img=IMG, href=SLUG, title=TITLE, ex=EXCERPT_HUB)

def rel_card():
    return (
    '<a class="blog-card" href="/%s">\n'
    '<div class="card__media"><img alt="%s" decoding="async" height="784" loading="lazy" src="%s" width="1168"/></div>\n'
    '<div class="blog-card__body">\n'
    '<span class="card__tag">Top Pokies</span>\n'
    '<h3>%s</h3>\n'
    '<p class="card__excerpt">%s</p>\n'
    '<p class="blog-card__meta">2026-09-21 &middot; 8 min read &middot; Read the guide &rarr;</p>\n'
    '</div>\n</a>\n'
    ) % (SLUG, ALT, IMG, TITLE, EXCERPT_REL)

def insert_hub_card(relpath, indent):
    p = os.path.join(PUB, relpath)
    s = open(p, encoding="utf-8").read()
    if ('href="/%s"' % SLUG) in s:
        print("already has card:", relpath); return
    marker = indent + '<article class="card">'
    idx = s.find(marker)
    if idx < 0:
        print("MARKER NOT FOUND:", relpath); return
    s = s[:idx] + hub_card(indent) + s[idx:]
    open(p, "w", encoding="utf-8").write(s)
    print("hub/category card inserted:", relpath)

def insert_rel(relpath):
    p = os.path.join(PUB, relpath)
    s = open(p, encoding="utf-8").read()
    if ('href="/%s"' % SLUG) in s:
        print("already linked:", relpath); return
    marker = '<div class="blog-card-grid">'
    idx = s.find(marker)
    if idx < 0:
        print("NO GRID:", relpath); return
    pos = idx + len(marker)
    s = s[:pos] + "\n" + rel_card() + s[pos:]
    open(p, "w", encoding="utf-8").write(s)
    print("related link inserted:", relpath)

# 1) blog hub (no indent), 2) top-pokies category (4-space)
insert_hub_card(os.path.join("blog","index.html"), "")
insert_hub_card(os.path.join("blog","top-pokies","index.html"), "    ")
# 3) contextual related links on the 3 most relevant guides
for f in ["progressive-jackpot-pokies-australia-2026.html",
          "hot-pokies-australia-2026-popular-slots.html",
          "daily-free-credit-pokies-australia-2026.html"]:
    insert_rel(f)
print("done")
