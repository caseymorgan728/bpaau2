#!/usr/bin/env python3
"""Exhaustive internal-link auditor for bpaau.org.

Crawls every HTML file under public/, extracts EVERY url reference
(a/href, img src/srcset, canonical, og:url/og:image, favicon/apple-touch,
stylesheet, script src, JSON-LD url/item/logo/image, picture source srcset,
data-slot, inline CSS url()), resolves internal paths, and reports broken ones.
"""
import os, re, json, csv, sys
from urllib.parse import urlparse, unquote, urljoin
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
DOMAIN = "bpaau.org"
EXCLUDE = {"google6c4a857337176f53.html", "404.html"}

# --- Build set of all existing files (public paths, forward slash) ---
existing_files = set()      # e.g. "assets/foo.webp", "blog/index.html"
existing_pages_slug = set() # e.g. "ausmegaways-review" (file ausmegaways-review.html)
for dirpath, dirnames, filenames in os.walk(PUB):
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, PUB).replace("\\", "/")
        existing_files.add(rel)

# Build a lookup: given a root-relative path like "/slug" or "/blog/category",
# return whether a backing file exists.
def path_exists(relpath):
    """relpath is a decoded root-relative path starting with '/' (or empty)."""
    p = relpath
    if p.startswith("/"):
        p = p[1:]
    if p == "":
        p = "index.html"
    # Direct candidate files
    candidates = [p]
    # /slug -> /slug.html
    if not os.path.splitext(p)[1]:
        candidates.append(p + ".html")
        candidates.append(p + "/index.html")
        candidates.append(os.path.join(p, "index.html").replace("\\","/"))
    # trailing-slash directory index
    if p.endswith("/"):
        candidates.append(p + "index.html")
    for c in candidates:
        if c in existing_files:
            return True, c
    return False, None

# --- Gather HTML files ---
html_files = []
for dirpath, dirnames, filenames in os.walk(PUB):
    for fn in filenames:
        if fn.lower().endswith(".html") and fn not in EXCLUDE:
            html_files.append(os.path.join(dirpath, fn))
html_files.sort()

report = []   # rows
total_refs = 0
checked_internal = 0

def add_row(srcfile, elem, kind, url, note=""):
    report.append({
        "source_file": srcfile,
        "element": elem,
        "category": kind,
        "url": url,
        "note": note,
    })

def is_internal(url):
    if url.startswith("//"):
        return True
    if url.startswith("http://") or url.startswith("https://"):
        host = urlparse(url).netloc.lower()
        return host == DOMAIN or host.endswith("." + DOMAIN)
    return True  # relative / root-relative

def check_url(src_abs, rel_name, elem, url, kind):
    """src_abs: absolute path of source file; rel_name: public-relative name for report."""
    global total_refs, checked_internal
    total_refs += 1
    srcfile = rel_name
    u = url.strip()
    if not u:
        return True
    # skip protocols
    if u.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:", "#")):
        return True
    # strip anchor / query
    frag = ""
    # separate fragment
    if "#" in u:
        u, frag = u.split("#", 1)
    if "?" in u:
        u = u.split("?", 1)[0]
    if u == "":
        return True
    # protocol-relative
    if u.startswith("//"):
        # treat as internal host
        parsed = urlparse("https:" + u)
        host = parsed.netloc.lower()
        if host == DOMAIN or host.endswith("." + DOMAIN):
            path = parsed.path
        else:
            return True  # external, skip
    elif u.startswith("http://") or u.startswith("https://"):
        parsed = urlparse(u)
        host = parsed.netloc.lower()
        if host != DOMAIN and not host.endswith("." + DOMAIN):
            return True  # external -> skip
        path = parsed.path
    else:
        if u.startswith("/"):
            path = u
        else:
            src_dir = os.path.dirname(src_abs)
            path = "/" + (os.path.normpath(os.path.relpath(os.path.join(src_dir, u), PUB)).replace("\\","/"))
    checked_internal += 1
    decoded = unquote(path)
    ok, backing = path_exists(decoded)
    if not ok:
        add_row(srcfile, elem, kind, url, f"path not found: {decoded}")
        return False
    return True

def parse_srcset(srcset, src_abs, srcfile, elem, kind):
    for part in srcset.split(","):
        part = part.strip()
        if not part:
            continue
        url = part.split()[0]
        check_url(src_abs, srcfile, elem, url, kind)

for hf in html_files:
    rel = os.path.relpath(hf, PUB).replace("\\","/")
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    # <a href>
    for a in soup.find_all("a", href=True):
        check_url(hf, rel, "a[href]", a["href"], "broken internal link")
    # img src / srcset
    for img in soup.find_all("img"):
        if img.get("src"):
            check_url(hf, rel, "img[src]", img["src"], "broken image")
        if img.get("srcset"):
            parse_srcset(img["srcset"], rel, "img[srcset]", "broken image")
    # source srcset
    for s in soup.find_all("source"):
        if s.get("srcset"):
            parse_srcset(s["srcset"], rel, "source[srcset]", "broken image")
        if s.get("src"):
            check_url(hf, rel, "source[src]", s["src"], "broken image")
    # link tags
    for lk in soup.find_all("link"):
        href = lk.get("href")
        if not href:
            continue
        relattr = (lk.get("rel") or [])
        relattr = relattr if isinstance(relattr, list) else [relattr]
        rl = " ".join(relattr).lower()
        if "canonical" in rl:
            check_url(hf, rel, "link[rel=canonical]", href, "broken canonical")
        elif "icon" in rl or "apple-touch-icon" in rl:
            check_url(hf, rel, "link[rel=icon]", href, "broken favicon")
        elif "stylesheet" in rl:
            check_url(hf, rel, "link[rel=stylesheet]", href, "broken CSS")
        elif "preload" in rl or "preload" in rl:
            check_url(hf, rel, "link[preload]", href, "broken preload")
        elif "manifest" in rl:
            check_url(hf, rel, "link[manifest]", href, "broken manifest")
        else:
            check_url(hf, rel, f"link[{rl}]", href, "broken link")
    # meta og:url, og:image, and any meta content that looks like url
    for m in soup.find_all("meta"):
        prop = (m.get("property") or m.get("name") or "").lower()
        content = m.get("content", "")
        if prop in ("og:url", "twitter:url"):
            check_url(hf, rel, f"meta[{prop}]", content, "broken OG")
        elif prop in ("og:image", "twitter:image"):
            check_url(hf, rel, f"meta[{prop}]", content, "broken OG image")
    # script src
    for sc in soup.find_all("script"):
        if sc.get("src"):
            check_url(hf, rel, "script[src]", sc["src"], "broken JS")
    # JSON-LD
    for sc in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(sc.string or "{}")
        except Exception:
            continue
        def walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, str) and k.lower() in ("url", "item", "logo", "image",
                                                            "contenturl", "embedurl"):
                        # logo/image may be dict
                        check_url(hf, rel, f"jsonld[{k}]", v, "broken JSON-LD")
                    else:
                        walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)
        walk(data)
    # inline <style> url(...)
    for st in soup.find_all("style"):
        txt = st.string or st.get_text() or ""
        for mm in re.finditer(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", txt):
            check_url(hf, rel, "style[url()]", mm.group(1), "broken CSS")

# --- Output ---
out_csv = os.path.join(ROOT, "_seo_scripts", "broken_links_report.csv")
out_md = os.path.join(ROOT, "_seo_scripts", "broken_links_report.md")

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["source_file","element","category","url","note"])
    w.writeheader()
    for r in report:
        w.writerow(r)

# Group by category
from collections import defaultdict
by_cat = defaultdict(list)
for r in report:
    by_cat[r["category"]].append(r)

with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Broken Link Audit Report\n\n")
    f.write(f"- HTML files scanned: {len(html_files)}\n")
    f.write(f"- Total URL references checked: {total_refs}\n")
    f.write(f"- Internal refs resolved: {checked_internal}\n")
    f.write(f"- **Broken refs found: {len(report)}**\n\n")
    for cat in sorted(by_cat):
        rows = by_cat[cat]
        f.write(f"## {cat} ({len(rows)})\n\n")
        f.write("| Source file | Element | URL | Note |\n")
        f.write("|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['source_file']} | {r['element']} | {r['url']} | {r['note']} |\n")
        f.write("\n")

print(f"HTML files: {len(html_files)}")
print(f"Total refs: {total_refs}")
print(f"Internal resolved: {checked_internal}")
print(f"BROKEN: {len(report)}")
for cat in sorted(by_cat):
    print(f"  {cat}: {len(by_cat[cat])}")
print(f"\nCSV: {out_csv}")
print(f"MD : {out_md}")
