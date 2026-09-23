# -*- coding: utf-8 -*-
import os, io, re, glob

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
htmls = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)

# Variant A: <section class="page-hero">  <img ...>  <p class="breadcrumb">
pat = re.compile(r'(<section class="page-hero">\s*)<img\b[^>]*>\s*(<p class="breadcrumb">)')
hits = []
for h in htmls:
    s = io.open(h, encoding="utf-8", errors="replace").read()
    if pat.search(s):
        hits.append(os.path.relpath(h, BASE))
print("pages with redundant old hero img:", len(hits))
for x in sorted(hits):
    print("   ", x)
