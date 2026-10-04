# -*- coding: utf-8 -*-
import io, os, re, glob
PUB = os.path.join(os.path.dirname(__file__), "public")
os.chdir(PUB)

slugs = ["free-100-no-deposit-bonus-australia-2026","free-spins-no-deposit-pokies-australia-2026",
"10-payid-no-deposit-bonus-australia-2026","lightning-link-online-australia-legal",
"dragon-link-online-pokies-australia-legal","big-bass-bonanza-pokies-australia-2026",
"sweet-bonanza-pokies-australia-2026"]

# 1. banner files exist
print("=== banners ===")
for s in slugs:
    p = os.path.join("assets","banners", s+"-banner.jpg")
    print(("OK " if os.path.exists(p) else "MISSING "), p, os.path.getsize(p) if os.path.exists(p) else "")

# 2. inbound link counts
print("=== inbound links ===")
allhtml = glob.glob("**/*.html", recursive=True)
texts = {}
for f in allhtml:
    texts[f] = io.open(f, encoding="utf-8", errors="ignore").read()
for s in slugs:
    n = sum(1 for f,t in texts.items() if ("/%s" % s) in t and not f.endswith(s+".html"))
    print("%-55s inbound=%d" % (s, n))

# 3. broken local hrefs across the 7 new pages
print("=== broken local refs in new pages ===")
def local_exists(href):
    href = href.split("#")[0].split("?")[0]
    if not href or href.startswith("http") or href.startswith("mailto:") or href.startswith("tel:"):
        return True
    if href.endswith("/"):
        cand = href.strip("/")
        return os.path.isdir(cand) or os.path.exists(os.path.join(cand,"index.html")) or cand==""
    cand = href.lstrip("/")
    return os.path.exists(cand) or os.path.exists(cand+".html") or os.path.isdir(cand)
bad = 0
for s in slugs:
    t = texts[s+".html"]
    refs = re.findall(r'(?:href|src)="([^"]+)"', t)
    broken = sorted({r for r in refs if not local_exists(r)})
    if broken:
        bad += 1
        print(s, "BROKEN:", broken)
print("pages with broken refs:", bad)
