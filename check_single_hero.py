# -*- coding: utf-8 -*-
import os, io, re, glob

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
htmls = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)

hero_pat = re.compile(r'<section class="page-hero">(.*?)</section>', re.S)
fig_pat = re.compile(r'<figure class="page-banner">.*?</figure>', re.S)
bad = []
for h in htmls:
    s = io.open(h, encoding="utf-8", errors="replace").read()
    if 'class="page-banner"' not in s:
        continue
    m = hero_pat.search(s)
    if not m:
        bad.append((os.path.relpath(h, BASE), "NO page-hero section")); continue
    body = fig_pat.sub("", m.group(1))
    imgs = re.findall(r'<img\b', body)
    if imgs:
        bad.append((os.path.relpath(h, BASE), "extra img x%d" % len(imgs)))
if bad:
    for b in bad: print(b)
else:
    print("CLEAN: every banner page has exactly one hero image (the new banner)")
