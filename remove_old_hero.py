# -*- coding: utf-8 -*-
import os, io, re, glob

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
htmls = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)

pat = re.compile(r'(<section class="page-hero">\s*)<img\b[^>]*>\s*(<p class="breadcrumb">)')
n = 0
for h in htmls:
    s = io.open(h, encoding="utf-8", errors="replace").read()
    new, c = pat.subn(r'\1\2', s)
    if c:
        io.open(h, "w", encoding="utf-8").write(new)
        n += c
        print("cleaned:", os.path.relpath(h, BASE))
print("total old heroes removed:", n)
