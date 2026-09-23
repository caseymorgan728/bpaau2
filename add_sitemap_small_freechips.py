# -*- coding: utf-8 -*-
import io
p = r"C:\Users\User\Documents\GitHub\bpaau2\public\sitemap.xml"
slug = "10-20-25-free-chip-no-deposit-australia-2026"
entry = ('  <url><loc>https://bpaau.org/%s</loc><lastmod>2026-09-23</lastmod>'
         '<changefreq>weekly</changefreq><priority>0.9</priority></url>\n') % slug
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
if slug in s:
    print("already in sitemap")
else:
    s = s.replace("</urlset>", entry + "</urlset>", 1)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("added to sitemap")
print("url count:", s.count("<loc>"))
