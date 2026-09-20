# -*- coding: utf-8 -*-
import os
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
p = os.path.join(PUB, "index.html")
s = open(p, encoding="utf-8").read()

if "/free-50-pokies" in s:
    print("homepage already links free-50")
else:
    card = (
    '<a class="blog-card" href="/free-50-pokies-no-deposit-sign-up-bonus-australia-2026">\n'
    '<div class="card__media"><img alt="Free $50 pokies no deposit sign up bonus Australia 2026" decoding="async" height="360" loading="lazy" src="/blog%20banner/blogpost%2012.webp" width="640"/></div>\n'
    '<div class="blog-card__body">\n'
    '<span class="card__tag">No Deposit</span>\n'
    '<h3>Free $50 Pokies No Deposit Sign-Up Bonus Australia (2026)</h3>\n'
    '<p class="card__excerpt">How the A$50 no-deposit sign-up chip really works &mdash; wagering, max cashout, PayID payout, and operators advertising up to $199 free sign-up credit.</p>\n'
    '<p class="blog-card__meta">Read the guide &rarr;</p>\n'
    '</div>\n</a>\n')
    marker = '<!-- ============ LATEST GUIDES ============ -->'
    mi = s.find(marker)
    gi = s.find('blog-card-grid', mi)
    pos = s.find('>', gi) + 1
    s = s[:pos] + "\n" + card + s[pos:]
    open(p, "w", encoding="utf-8").write(s)
    print("inserted free-50 card on homepage at", pos)
