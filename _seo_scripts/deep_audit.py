# -*- coding: utf-8 -*-
"""Deeper checks: game CTAs, sitemap, robots, _worker, CSS, JSON-LD types, product grids."""
import os, re, json, urllib.parse
from html.parser import HTMLParser

ROOT = r"C:\Users\User\Documents\GitHub\Australia igaming website"
PUB = os.path.join(ROOT, "public")
OP_SET = {
    "https://1xaud.com/register",
    "https://gd8au.com/register",
    "https://mrblueyau.com/register",
    "https://1xaceau.com/register",
    "https://garcat8.com/register",
    "https://toystory9au.com/register",
}

def list_html():
    out = []
    for dp, dn, fn in os.walk(PUB):
        for f in fn:
            if f.lower().endswith(".html"):
                out.append(os.path.join(dp, f))
    return sorted(out)

def relpath(p):
    return os.path.relpath(p, PUB).replace("\\", "/")

# ---- Game CTA + product grid check ----
class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ctas = []
        self.product_operators = set()
        self.in_product_grid = False
        self.in_grid = False
        self.cur_card_op = None
        self.ld_types = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "div" and "product-grid" in cls:
            self.in_product_grid = True
        if tag == "a" and "game-card__cta" in cls:
            self.ctas.append(a.get("href", ""))
        if tag == "p" and "product-card__brand" in cls:
            self._want_brand = True
    def handle_data(self, data):
        if getattr(self, "_want_brand", False):
            self.product_operators.add(data.strip())
            self._want_brand = False

print("=== GAME CTA CHECK ===")
bad_ctas = []
total_ctas = 0
for h in list_html():
    txt = open(h, encoding="utf-8").read()
    p = P()
    p.feed(txt)
    for c in p.ctas:
        total_ctas += 1
        if c not in OP_SET:
            bad_ctas.append((relpath(h), c))
print("total game CTAs:", total_ctas)
print("bad game CTAs:", len(bad_ctas))
for b in bad_ctas[:20]:
    print("  ", b)

print("\n=== PRODUCT GRID OPERATOR COVERAGE ===")
pages_with_grid = []
for h in list_html():
    txt = open(h, encoding="utf-8").read()
    if 'class="product-grid"' in txt:
        p = P()
        p.feed(txt)
        pages_with_grid.append((relpath(h), p.product_operators))
print("pages with product-grid:", len(pages_with_grid))
missing = []
for rel, ops in pages_with_grid:
    for required in ["1XAUD","GD8","MR BLUEY","TOY STORY 9","GARCAT8","1XACE"]:
        if required not in ops:
            missing.append((rel, required))
print("product-grid operator gaps:", len(missing))
for m in missing[:20]:
    print("  ", m)

print("\n=== JSON-LD TYPE COVERAGE ===")
# which pages have which required types
type_need = {
    "all": {"WebSite","Organization","BreadcrumbList"},
}
counts = {}
for h in list_html():
    txt = open(h, encoding="utf-8").read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S)
    types = set()
    for b in blocks:
        try:
            d = json.loads(b)
            t = d.get("@type")
            if isinstance(t, str): types.add(t)
        except Exception:
            pass
    for t in types:
        counts[t] = counts.get(t, 0) + 1
for t, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c} pages")

# pages missing WebSite/Organization/BreadcrumbList
print("\n=== PAGES MISSING CORE TYPES (excluding google verify) ===")
for h in list_html():
    rel = relpath(h)
    if rel.startswith("google"):
        continue
    txt = open(h, encoding="utf-8").read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S)
    types = set()
    for b in blocks:
        try:
            d = json.loads(b)
            t = d.get("@type")
            if isinstance(t, str): types.add(t)
        except Exception:
            pass
    missing_core = {"WebSite","Organization","BreadcrumbList"} - types
    if missing_core:
        print(f"  {rel}: missing {sorted(missing_core)}")

print("\n=== SITEMAP ===")
sm = open(os.path.join(PUB, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
print("sitemap URLs:", len(locs))
non_https = [l for l in locs if not l.startswith("https://bpaau.org/")]
print("non https://bpaau.org/ URLs:", len(non_https), non_https[:5])
# all indexable html pages
def url_to_file(u):
    path = u.replace("https://bpaau.org/", "")
    if path == "":
        return "index.html"
    cands = [path + ".html", path.rstrip("/") + "/index.html", os.path.join(path, "index.html")]
    for c in cands:
        if os.path.isfile(os.path.join(PUB, c)):
            return c
    return None
missing_from_sitemap = []
extra_in_sitemap = []
sitemap_files = set()
for l in locs:
    f = url_to_file(l)
    if f:
        sitemap_files.add(f)
    else:
        extra_in_sitemap.append(l)
# actual indexable pages
indexable = []
for h in list_html():
    rel = relpath(h)
    if rel == "404.html": continue
    if rel.startswith("google"): continue
    txt = open(h, encoding="utf-8").read()
    if re.search(r'name="robots"\s+content="[^"]*noindex', txt):
        continue
    indexable.append(rel)
for rel in indexable:
    if rel not in sitemap_files:
        missing_from_sitemap.append(rel)
print("indexable pages:", len(indexable))
print("indexable pages MISSING from sitemap:", len(missing_from_sitemap))
for m in missing_from_sitemap:
    print("  ", m)
print("sitemap URLs with no matching file:", len(extra_in_sitemap))
for e in extra_in_sitemap:
    print("  ", e)

print("\n=== CSS SIZE ===")
css = os.path.join(PUB, "assets", "theme.css")
if os.path.isfile(css):
    sz = os.path.getsize(css)
    print(f"theme.css: {sz} bytes ({sz/1024:.1f} KB)")

print("\n=== EXTERNAL FONTS / SCRIPTS ===")
ext_font = 0
ext_script = 0
for h in list_html():
    txt = open(h, encoding="utf-8").read()
    if re.search(r'<link[^>]+href="https?://[^"]*font', txt, re.I):
        ext_font += 1
    if re.search(r'<script[^>]+src="https?://', txt, re.I):
        ext_script += 1
print("pages with external font links:", ext_font)
print("pages with external script src:", ext_script)

print("\n=== HERO fetchpriority high ===")
hero_high = 0
for h in list_html():
    txt = open(h, encoding="utf-8").read()
    hero_high += len(re.findall(r'fetchpriority="high"', txt))
print("fetchpriority=high images:", hero_high)
