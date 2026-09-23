# -*- coding: utf-8 -*-
import os, io, re, glob

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
BAN = os.path.join(BASE, "assets", "banners")

# all banner files
bans = glob.glob(os.path.join(BAN, "*-banner.*"))
print("banner image files:", len(bans))

# every html file under public
htmls = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)
missing = []
withbanner = 0
for h in htmls:
    rel = os.path.relpath(h, BASE)
    s = io.open(h, encoding="utf-8", errors="replace").read()
    if 'class="page-banner"' in s:
        withbanner += 1
    else:
        missing.append(rel)
print("html files total:", len(htmls))
print("html with banner:", withbanner)
print("html WITHOUT banner:")
for m in sorted(missing):
    print("   ", m)
