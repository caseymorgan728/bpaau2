# -*- coding: utf-8 -*-
import os, re
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"

# 1) Update sitemap.xml
sp = os.path.join(PUB, "sitemap.xml")
s = open(sp, encoding="utf-8").read()
new_urls = [
    ("free-50-pokies-no-deposit-sign-up-bonus-australia-2026", "0.9"),
    ("wolf-treasure-pokies-australia-2026", "0.8"),
    ("payid-pokies-no-verification-australia-2026", "0.8"),
]
add = ""
for slug, pri in new_urls:
    if slug not in s:
        add += ('  <url><loc>https://bpaau.org/%s</loc><lastmod>2026-09-21</lastmod>'
                '<changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (slug, pri))
s = s.replace("</urlset>", add + "</urlset>")
open(sp, "w", encoding="utf-8").write(s)
print("sitemap loc count now:", s.count("<loc>"))

# 2) Show blog hub card structure
bp = os.path.join(PUB, "blog", "index.html")
b = open(bp, encoding="utf-8").read()
print("blog index size:", len(b))
# print first blog-card block
m = re.search(r'<a class="blog-card".*?</a>', b, re.S)
print("--- sample blog hub card ---")
print(m.group(0)[:900] if m else "NO CARD FOUND")
