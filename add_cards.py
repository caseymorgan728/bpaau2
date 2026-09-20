# -*- coding: utf-8 -*-
import os, re
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"

def card(href, tag, title, excerpt, img, alt, indent=""):
    return (
'{i}<article class="card">\n'
'{i}<div class="card__media">\n'
'{i}<img alt="{alt}" decoding="async" height="400" loading="lazy" src="{img}" width="600"/>\n'
'{i}</div>\n'
'{i}<div class="card__body">\n'
'{i}<span class="card__tag">{tag}</span>\n'
'{i}<h2 class="card__title"><a href="/{href}">{title}</a></h2>\n'
'{i}<p class="card__excerpt">{excerpt}</p>\n'
'{i}<a class="btn btn--primary btn--small" href="/{href}">Read Article</a>\n'
'{i}</div>\n'
'{i}</article>\n'
    ).format(i=indent, alt=alt, img=img, tag=tag, href=href, title=title, excerpt=excerpt)

free50 = dict(
    href="free-50-pokies-no-deposit-sign-up-bonus-australia-2026",
    tag="NO DEPOSIT",
    title="Free $50 Pokies No Deposit Sign-Up Bonus Australia 2026",
    excerpt="How a free $50 pokies no deposit sign-up bonus really works in Australia &mdash; wagering, max cashout and expiry rules, PayID payouts, and operators advertising up to $199 sign-up credit.",
    img="/blog%20banner/blogpost%2012.webp",
    alt="Free $50 pokies no deposit sign up bonus Australia 2026",
)
wolf = dict(
    href="wolf-treasure-pokies-australia-2026",
    tag="TOP POKIES",
    title="Wolf Treasure Pokies Australia 2026 &mdash; Free Spins &amp; Jackpot Guide",
    excerpt="How Wolf Treasure&rsquo;s golden-moon Money Respin and Mini, Major and Mega jackpots work, where to claim Wolf Treasure free spins with no deposit, and how to cash out via PayID.",
    img="/blog%20banner/for%20blogpost%201%20and%206.webp",
    alt="Wolf Treasure pokies Australia free spins guide",
)
payidnv = dict(
    href="payid-pokies-no-verification-australia-2026",
    tag="FAST CASHOUTS",
    title="PayID Pokies No Verification Australia 2026 &mdash; The Truth About KYC",
    excerpt="Can you really play PayID pokies with no verification? What &lsquo;no KYC&rsquo; means, why licensed casinos verify before payout, and how to make first PayID withdrawals near-instant.",
    img="/blog%20banner/blogpost%208.webp",
    alt="PayID pokies no verification Australia fast withdrawal",
)

def insert_first(path, cards, indent):
    s = open(path, encoding="utf-8").read()
    marker = indent + '<article class="card">'
    if 'href="/free-50-pokies' in s or 'href="/wolf-treasure' in s or 'href="/payid-pokies-no-verification' in s:
        print("SKIP (already has new card):", os.path.basename(os.path.dirname(path)) or path)
        return
    block = "".join(card(indent=indent, **c) for c in cards)
    idx = s.find(marker)
    if idx < 0:
        print("MARKER NOT FOUND in", path); return
    s = s[:idx] + block + s[idx:]
    open(path, "w", encoding="utf-8").write(s)
    print("inserted", len(cards), "card(s) into", path.replace(PUB,""))

# Blog hub (no indent)
insert_first(os.path.join(PUB,"blog","index.html"), [free50, wolf, payidnv], "")
# Category pages (4-space indent)
insert_first(os.path.join(PUB,"blog","bonus-guides","index.html"), [free50], "    ")
insert_first(os.path.join(PUB,"blog","top-pokies","index.html"), [wolf], "    ")
insert_first(os.path.join(PUB,"blog","fast-cashouts","index.html"), [payidnv], "    ")
print("done")
