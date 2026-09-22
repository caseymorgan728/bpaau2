# -*- coding: utf-8 -*-
import io, os
p = r"C:\Users\User\Documents\GitHub\bpaau2\public\sitemap.xml"
slug = "no-deposit-bonus-codes-australia-2026"
entry = ('  <url><loc>https://bpaau.org/%s</loc><lastmod>2026-09-22</lastmod>'
         '<changefreq>weekly</changefreq><priority>0.9</priority></url>\n') % slug
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
if slug in s:
    print("already in sitemap")
else:
    assert "</urlset>" in s
    s = s.replace("</urlset>", entry + "</urlset>", 1)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("added to sitemap")
print("url count:", s.count("<loc>"))
