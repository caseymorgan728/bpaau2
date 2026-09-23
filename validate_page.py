# -*- coding: utf-8 -*-
import io, os, re, json, sys, urllib.parse as up
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
slug = sys.argv[1]
f = os.path.join(PUB, slug + ".html")
s = io.open(f, encoding="utf-8").read()
t = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
print("TITLE (%d chars): %s" % (len(t), t))
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
for b in blocks: json.loads(b)
print("JSON-LD blocks OK:", len(blocks))
bad = []
for href in re.findall(r'href="([^"]+)"', s):
    if href.startswith(("http","tel:","mailto:","#")): continue
    path = up.unquote(href.split("#")[0].split("?")[0])
    if path == "": continue
    c = os.path.join(PUB, path.lstrip("/"))
    if os.path.exists(c) or os.path.exists(c+".html") or os.path.exists(os.path.join(c,"index.html")): continue
    bad.append(href)
for src in re.findall(r'src="([^"]+)"', s):
    if src.startswith("http"): continue
    path = up.unquote(src.split("?")[0])
    if not os.path.exists(os.path.join(PUB, path.lstrip("/"))): bad.append("SRC:"+src)
print("broken local refs:", bad if bad else "NONE")
inc = set()
for root, _, files in os.walk(PUB):
    for fn in files:
        if fn.endswith(".html"):
            txt = io.open(os.path.join(root, fn), encoding="utf-8").read()
            if ("/"+slug) in txt and fn != (slug+".html"):
                inc.add(os.path.relpath(os.path.join(root, fn), PUB))
print("pages linking IN (%d):" % len(inc))
for x in sorted(inc): print("  ", x)
print("word count approx:", len(re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>"," ",s))))
