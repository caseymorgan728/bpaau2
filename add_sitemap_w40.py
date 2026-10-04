# -*- coding: utf-8 -*-
import io, os, re

FP = os.path.join("public", "sitemap.xml")
NEW = [
    ("free-100-no-deposit-bonus-australia-2026", "0.8"),
    ("free-spins-no-deposit-pokies-australia-2026", "0.8"),
    ("10-payid-no-deposit-bonus-australia-2026", "0.8"),
    ("lightning-link-online-australia-legal", "0.7"),
    ("dragon-link-online-pokies-australia-legal", "0.7"),
    ("big-bass-bonanza-pokies-australia-2026", "0.7"),
    ("sweet-bonanza-pokies-australia-2026", "0.7"),
]

t = io.open(FP, encoding="utf-8").read()
had_bom = t.startswith("\ufeff")
t = t.lstrip("\ufeff")

blocks = []
for slug, pri in NEW:
    url = "https://bpaau.org/" + slug
    if ("<loc>%s</loc>" % url) in t:
        print("exists, skip:", slug); continue
    blocks.append(
        '  <url>\n'
        '    <loc>%s</loc>\n'
        '    <lastmod>2026-10-04</lastmod>\n'
        '    <changefreq>weekly</changefreq>\n'
        '    <priority>%s</priority>\n'
        '  </url>\n' % (url, pri))

assert "</urlset>" in t
t = t.replace("</urlset>", "".join(blocks) + "</urlset>")
with io.open(FP, "w", encoding="utf-8", newline="\n") as f:
    f.write(("\ufeff" if had_bom else "") + t)
print("URL count now:", len(re.findall(r"<loc>", t)))
