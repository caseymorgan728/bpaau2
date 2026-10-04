# -*- coding: utf-8 -*-
"""Wire the 7 new pages into home, blog hub, category grids, sibling related-grids, legality."""
import io, os, re

ROOT = os.path.dirname(__file__)
PUB = os.path.join(ROOT, "public")
BN = "/assets/banners/%s-banner.jpg"

DATA = {
 "free-100-no-deposit-bonus-australia-2026": dict(
   img=BN % "free-100-no-deposit-bonus-australia-2026", tag="NO DEPOSIT",
   h3="$100 No Deposit Bonus Australia 2026: The Real Terms",
   ex="Do $100 free no-deposit chips exist for Australian pokies? The honest math on wagering, caps and conversion, plus verified automatic sign-up credit up to $199.",
   meta="2026-10-04 · 8 min read · Read the guide &rarr;"),
 "free-spins-no-deposit-pokies-australia-2026": dict(
   img=BN % "free-spins-no-deposit-pokies-australia-2026", tag="FREE SPINS",
   h3="Free Spins No Deposit Australia 2026: Keep Winnings",
   ex="How to claim registration free spins on Australian pokies, the wagering and max-cashout rules that decide what you keep, and the PayID payout steps.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
 "10-payid-no-deposit-bonus-australia-2026": dict(
   img=BN % "10-payid-no-deposit-bonus-australia-2026", tag="PAYID",
   h3="$10 PayID No Deposit Bonus Australia 2026: Free Chip",
   ex="Where to get a small $10 no-deposit chip and withdraw through PayID, the playthrough reality, and the fastest verified Australian-facing operators.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
 "lightning-link-online-australia-legal": dict(
   img=BN % "lightning-link-online-australia-legal", tag="LEGAL GUIDE",
   h3="Lightning Link Online Australia: Real-Money Truth",
   ex="Why there is no legal real-money online Lightning Link in Australia, what the social app really is, how to spot offshore clones, and safer jackpot pokies.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
 "dragon-link-online-pokies-australia-legal": dict(
   img=BN % "dragon-link-online-pokies-australia-legal", tag="LEGAL GUIDE",
   h3="Dragon Link Online Pokies Australia: Legal Status",
   ex="Where Aristocrat's Dragon Link is legal to play, why real-money online clones targeting Australia are scams, and the safest jackpot-style pokies online.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
 "big-bass-bonanza-pokies-australia-2026": dict(
   img=BN % "big-bass-bonanza-pokies-australia-2026", tag="GAME GUIDE",
   h3="Big Bass Bonanza Pokies Australia: RTP & Free Spins",
   ex="The fishing pokie's free-spins ladder, fisherman wild and 2x/3x/10x multipliers explained, with 96.71% RTP, high variance and PayID cashout.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
 "sweet-bonanza-pokies-australia-2026": dict(
   img=BN % "sweet-bonanza-pokies-australia-2026", tag="GAME GUIDE",
   h3="Sweet Bonanza Pokies Australia: RTP & Tumble Wins",
   ex="How the pays-anywhere tumble engine and 2x-100x multiplier bombs work, the RTP variants you must check, and where to play with registration free credit.",
   meta="2026-10-04 · 7 min read · Read the guide &rarr;"),
}

def bcard(slug, w=1168, h=784):
    d = DATA[slug]
    return (f'<a class="blog-card" href="/{slug}">\n'
            f'<div class="card__media"><img alt="{d["h3"]}" decoding="async" height="{h}" loading="lazy" src="{d["img"]}" width="{w}"/></div>\n'
            f'<div class="blog-card__body">\n<span class="card__tag">{d["tag"]}</span>\n'
            f'<h3>{d["h3"]}</h3>\n<p class="card__excerpt">{d["ex"]}</p>\n'
            f'<p class="blog-card__meta">{d["meta"]}</p>\n</div>\n</a>\n')

def ccard(slug):
    d = DATA[slug]
    return (f'<article class="card">\n<div class="card__media">\n'
            f'<img alt="{d["h3"]}" decoding="async" height="400" loading="lazy" src="{d["img"]}" width="600"/>\n'
            f'</div>\n<div class="card__body">\n<span class="card__tag">{d["tag"]}</span>\n'
            f'<h2 class="card__title"><a href="/{slug}">{d["h3"]}</a></h2>\n'
            f'<p class="card__excerpt">{d["ex"]}</p>\n'
            f'<a class="btn btn--primary btn--small" href="/{slug}">Read Article</a>\n</div>\n</article>\n')

def insert_after_grid(rel, slugs, renderer, w=None, h=None):
    fp = os.path.join(PUB, rel)
    if not os.path.exists(fp):
        print("MISSING FILE, skip:", rel); return
    t = io.open(fp, encoding="utf-8").read()
    added = []
    for s in slugs:
        if ("/%s" % s) in t:
            continue
        added.append(s)
    if not added:
        print("already wired:", rel); return
    m = re.search(r'<div class="blog-card-grid">', t)
    if not m:
        print("NO GRID, skip:", rel); return
    if renderer == "b":
        block = "".join(bcard(s, w or 1168, h or 784) for s in added)
    else:
        block = "".join(ccard(s) for s in added)
    pos = m.end()
    t = t[:pos] + "\n" + block + t[pos:]
    io.open(fp, "w", encoding="utf-8", newline="\n").write(t)
    print("wired %d into %s" % (len(added), rel))

# --- category / hub (article.card, 600x400) ---
insert_after_grid(os.path.join("blog","index.html"),
    ["free-100-no-deposit-bonus-australia-2026","free-spins-no-deposit-pokies-australia-2026",
     "10-payid-no-deposit-bonus-australia-2026","lightning-link-online-australia-legal",
     "dragon-link-online-pokies-australia-legal","big-bass-bonanza-pokies-australia-2026",
     "sweet-bonanza-pokies-australia-2026"], "c")
insert_after_grid(os.path.join("blog","bonus-guides","index.html"),
    ["free-100-no-deposit-bonus-australia-2026","free-spins-no-deposit-pokies-australia-2026",
     "10-payid-no-deposit-bonus-australia-2026"], "c")
insert_after_grid(os.path.join("blog","top-pokies","index.html"),
    ["big-bass-bonanza-pokies-australia-2026","sweet-bonanza-pokies-australia-2026"], "c")
insert_after_grid(os.path.join("blog","winning-tips","index.html"),
    ["lightning-link-online-australia-legal","dragon-link-online-pokies-australia-legal"], "c")

# --- home (blog-card, 640x360) ---
insert_after_grid("index.html",
    ["free-100-no-deposit-bonus-australia-2026","free-spins-no-deposit-pokies-australia-2026",
     "10-payid-no-deposit-bonus-australia-2026"], "b", w=640, h=360)

# --- sibling content related grids (blog-card, 1168x784) ---
content_targets = [
 ("free-50-pokies-no-deposit-sign-up-bonus-australia-2026.html",
   ["free-100-no-deposit-bonus-australia-2026","free-spins-no-deposit-pokies-australia-2026"]),
 ("10-20-25-free-chip-no-deposit-australia-2026.html",
   ["10-payid-no-deposit-bonus-australia-2026","free-100-no-deposit-bonus-australia-2026"]),
 ("no-deposit-bonus-codes-australia-2026.html",
   ["free-spins-no-deposit-pokies-australia-2026","free-100-no-deposit-bonus-australia-2026"]),
 ("wolf-treasure-pokies-australia-2026.html",
   ["lightning-link-online-australia-legal","dragon-link-online-pokies-australia-legal"]),
 ("payid-cashouts-australia-2026.html",
   ["10-payid-no-deposit-bonus-australia-2026"]),
 ("hold-and-win-pokies-australia-2026.html",
   ["lightning-link-online-australia-legal"]),
 ("best-high-rtp-pokies-australia-2026.html",
   ["big-bass-bonanza-pokies-australia-2026","sweet-bonanza-pokies-australia-2026"]),
 ("gate-of-olympus-pokies-australia-2026.html",
   ["sweet-bonanza-pokies-australia-2026","big-bass-bonanza-pokies-australia-2026"]),
 ("5-dragons-pokies-australia-2026.html",
   ["dragon-link-online-pokies-australia-legal"]),
 ("same-day-pokies-withdrawals-australia.html",
   ["10-payid-no-deposit-bonus-australia-2026"]),
 ("curacao-casino-licence-check-australia-2026.html",
   ["lightning-link-online-australia-legal"]),
]
for rel, slugs in content_targets:
    insert_after_grid(rel, slugs, "b")

# --- legality page: inject a related legal-guides section before container/main close ---
leg = os.path.join(PUB, "online-pokies-legality-australia-2026.html")
t = io.open(leg, encoding="utf-8").read()
if "/lightning-link-online-australia-legal" not in t:
    section = (
      '\n      <section class="section">\n'
      '      <div class="section-title"><span class="section-title__label">Related legal guides</span>'
      '<h2>Brand-Specific Legal Questions Australians Ask</h2></div>\n'
      '      <div class="blog-card-grid">\n'
      + bcard("lightning-link-online-australia-legal")
      + bcard("dragon-link-online-pokies-australia-legal")
      + '      </div>\n      </section>\n')
    anchor = "    </div>\n  </main>"
    if anchor in t:
        t = t.replace(anchor, section + anchor, 1)
        io.open(leg, "w", encoding="utf-8", newline="\n").write(t)
        print("wired legality related section")
    else:
        print("legality anchor not found")
else:
    print("legality already wired")
print("done")
