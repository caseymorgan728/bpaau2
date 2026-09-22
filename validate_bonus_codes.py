# -*- coding: utf-8 -*-
import io, os, re, json, urllib.parse as up
PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
f = os.path.join(PUB, "no-deposit-bonus-codes-australia-2026.html")
s = io.open(f, encoding="utf-8").read()

# title length
t = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
print("TITLE (%d chars): %s" % (len(t), t))

# JSON-LD blocks parse
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
for i, b in enumerate(blocks):
    json.loads(b)
print("JSON-LD blocks OK:", len(blocks))

# local hrefs resolve
bad = []
for href in re.findall(r'href="([^"]+)"', s):
    if href.startswith(("http", "tel:", "mailto:", "#")): continue
    path = up.unquote(href.split("#")[0])
    if path == "": continue
    cand = os.path.join(PUB, path.lstrip("/"))
    # clean URLs map to .html or directory index
    if os.path.exists(cand): continue
    if os.path.exists(cand + ".html"): continue
    if os.path.exists(os.path.join(cand, "index.html")): continue
    bad.append(href)
for src in re.findall(r'src="([^"]+)"', s):
    if src.startswith("http"): continue
    path = up.unquote(src.split("?")[0])
    if not os.path.exists(os.path.join(PUB, path.lstrip("/"))):
        bad.append("SRC:"+src)
print("broken local refs:", bad if bad else "NONE")

# inbound links to new page
inc = []
for root, _, files in os.walk(PUB):
    for fn in files:
        if fn.endswith(".html"):
            txt = io.open(os.path.join(root, fn), encoding="utf-8").read()
            if "/no-deposit-bonus-codes-australia-2026" in txt and fn != "no-deposit-bonus-codes-australia-2026.html":
                inc.append(fn)
print("pages linking IN (%d):" % len(inc), sorted(set(inc)))
print("word count approx:", len(re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>", " ", s))))
