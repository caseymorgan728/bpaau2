# -*- coding: utf-8 -*-
import io, re, os
os.chdir(os.path.join(os.path.dirname(__file__), "public"))
h = io.open("index.html", encoding="utf-8").read()
print("home blog-card-grid count:", h.count("blog-card-grid"))
for m in re.finditer(r'<div class="([^"]*grid[^"]*)"', h):
    print("  home grid class:", m.group(1))
print("--- sibling pages ---")
files = ['free-50-pokies-no-deposit-sign-up-bonus-australia-2026.html',
         '10-20-25-free-chip-no-deposit-australia-2026.html',
         'no-deposit-bonus-codes-australia-2026.html',
         'online-pokies-legality-australia-2026.html',
         'wolf-treasure-pokies-australia-2026.html',
         'payid-cashouts-australia-2026.html',
         'hold-and-win-pokies-australia-2026.html',
         'best-high-rtp-pokies-australia-2026.html',
         'free-pokies-australia-no-download.html']
for f in files:
    if os.path.exists(f):
        t = io.open(f, encoding="utf-8").read()
        print(f, "grids=", t.count("blog-card-grid"), "len=", len(t))
    else:
        print(f, "MISSING")
