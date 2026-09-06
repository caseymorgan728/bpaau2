#!/usr/bin/env python3
"""
bpaau.org technical SEO audit.
Scans every .html file under public/ and reports pass/fail per check.
Outputs:
  - audit_report.md  (markdown table)
  - audit_report.csv (machine-readable)
"""
import os, re, csv, json, sys
from collections import defaultdict
from bs4 import BeautifulSoup

ROOT = r"C:\Users\User\Documents\GitHub\Australia igaming website"
PUB = os.path.join(ROOT, "public")

AFFILIATE_DOMAINS = [
    "1xaud.com", "gd8au.com", "mrblueyau.com",
    "toystory9au.com", "garcat8.com", "1xaceau.com",
]
NOINDEX_PAGES = {"top-10-easiest-profit-pokies-2026", "404"}
SKIP_PAGES = {"google6c4a857337176f53"}  # Google verification file — not a real page

# ---------------------------------------------------------------------------
# Collect all HTML pages
# ---------------------------------------------------------------------------
pages = []  # list of (rel_url, abs_path)
for dirpath, dirnames, filenames in os.walk(PUB):
    # skip backup folders
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, PUB).replace("\\", "/")
        # rel URL path: strip .html; root index.html -> /
        if rel.endswith("/index.html"):
            slug = "/" + rel[:-len("index.html")]
        elif rel == "index.html":
            slug = "/"
        else:
            slug = "/" + rel[:-5]  # strip .html
        pages.append((slug, full, rel))

# Build set of valid local routes (clean slugs)
valid_routes = set(p[0] for p in pages)
# also allow /blog/... which map to /blog/.../index.html
# Already covered above.
# Also allow assets (non-.html) — those are not linked via href="/..." typically
# but we'll allow any path under /assets/ or other dirs with real files.
asset_files = set()
for dirpath, dirnames, filenames in os.walk(PUB):
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        if fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel = "/" + os.path.relpath(full, PUB).replace("\\", "/")
        asset_files.add(rel)

# ---------------------------------------------------------------------------
# Audit each page
# ---------------------------------------------------------------------------
rows = []
titles_seen = defaultdict(list)
descs_seen = defaultdict(list)

# First pass: collect titles/descriptions for uniqueness check
meta_info = {}

for slug, full, rel in pages:
    with open(full, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag.get("content", "").strip() if desc_tag else ""

    meta_info[slug] = {"title": title, "desc": desc}
    titles_seen[title].append(slug)
    descs_seen[desc].append(slug)

# Second pass: full checks
for slug, full, rel in pages:
    if slug.strip("/") in SKIP_PAGES:
        continue
    with open(full, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    title = meta_info[slug]["title"]
    desc = meta_info[slug]["desc"]
    is_noindex = slug.strip("/") in NOINDEX_PAGES

    issues = []

    # 1. Title
    if not title:
        issues.append("TITLE_MISSING")
    elif len(title) > 60:
        issues.append("TITLE_LONG(%d)" % len(title))
    # uniqueness
    if len(titles_seen[title]) > 1 and title:
        issues.append("TITLE_DUP")

    # 2. Meta description
    if not desc:
        issues.append("DESC_MISSING")
    else:
        if len(desc) < 130:
            issues.append("DESC_SHORT(%d)" % len(desc))
        elif len(desc) > 160:
            issues.append("DESC_LONG(%d)" % len(desc))
    if desc and len(descs_seen[desc]) > 1:
        issues.append("DESC_DUP")

    # 3. Canonical
    canon = soup.find("link", attrs={"rel": "canonical"})
    if not canon:
        issues.append("CANONICAL_MISSING")
    else:
        href = canon.get("href", "")
        # Expected URL: strip trailing slash (except root)
        if slug == "/":
            expected = "https://bpaau.org/"
        else:
            expected = "https://bpaau.org" + slug.rstrip("/")
        if href != expected:
            issues.append("CANONICAL_MISMATCH(%s)" % href)
        if ".html" in href:
            issues.append("CANONICAL_HTML_EXT")

    # 4. H1 count
    h1s = soup.find_all("h1")
    if len(h1s) == 0:
        issues.append("H1_MISSING")
    elif len(h1s) > 1:
        issues.append("H1_MULTI(%d)" % len(h1s))

    # 5. Heading hierarchy
    headings = [int(h.name[1]) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    prev = 0
    for lv in headings:
        if prev and lv > prev + 1:
            issues.append("H_SKIP(%d->%d)" % (prev, lv))
            break
        prev = lv

    # 6. JSON-LD
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    ld_types = []
    for sc in scripts:
        try:
            data = json.loads(sc.string or "{}")
            nodes = []
            if isinstance(data, list):
                nodes = data
            elif isinstance(data, dict):
                if "@graph" in data and isinstance(data["@graph"], list):
                    nodes = data["@graph"]
                else:
                    nodes = [data]
            for d in nodes:
                if isinstance(d, dict):
                    t = d.get("@type", "")
                    if isinstance(t, list):
                        ld_types.extend(t)
                    else:
                        ld_types.append(t)
        except Exception:
            issues.append("JSONLD_INVALID")
    has_website = any(t == "WebSite" for t in ld_types)
    has_org = any(t == "Organization" for t in ld_types)
    has_bc = any(t == "BreadcrumbList" for t in ld_types)
    has_article = any(t in ("Article", "BlogPosting", "WebPage", "Report", "AboutPage", "ContactPage", "FAQPage") for t in ld_types)
    has_faq = any(t == "FAQPage" for t in ld_types)
    has_webpage_graph = any(t in ("WebPage", "Report", "AboutPage", "ContactPage") for t in ld_types)
    if not has_website:
        issues.append("LD_NO_WEBSITE")
    if not has_org:
        issues.append("LD_NO_ORG")
    if not has_bc and slug != "/":
        issues.append("LD_NO_BREADCRUMB")
    if not has_article and not has_faq and not has_webpage_graph:
        # content pages (blog articles) should have Article/BlogPosting or FAQ
        is_content = (slug not in ("/", "/blog") and not slug.startswith("/blog/")
                      and not slug.startswith("/assets") and not slug.endswith("-review")
                      and slug not in ("/privacy", "/terms", "/404", "/responsible-gambling"))
        if is_content:
            issues.append("LD_NO_CONTENT_SCHEMA")

    # 7. Image alt
    imgs = soup.find_all("img")
    missing_alt = [i for i in imgs if not i.get("alt") or not i.get("alt", "").strip()]
    if missing_alt:
        issues.append("IMG_NO_ALT(%d)" % len(missing_alt))

    # 8. Image dimensions
    missing_dim = [i for i in imgs if not i.get("width") or not i.get("height")]
    if missing_dim:
        issues.append("IMG_NO_DIM(%d)" % len(missing_dim))

    # 9. Lazy loading (non-hero)
    # Hero = first img in page-hero or has loading=eager/fetchpriority=high
    non_hero_no_lazy = []
    for i, img in enumerate(imgs):
        loading = (img.get("loading") or "").lower()
        fp = (img.get("fetchpriority") or "").lower()
        is_hero = (i == 0) or loading == "eager" or fp == "high"
        if not is_hero and loading != "lazy":
            non_hero_no_lazy.append(img.get("src", ""))
    if non_hero_no_lazy:
        issues.append("IMG_NOT_LAZY(%d)" % len(non_hero_no_lazy))

    # 10 & 18. Internal links
    links = soup.find_all("a", href=True)
    broken = []
    for a in links:
        href = a["href"].strip()
        if not href.startswith("/"):
            continue
        # strip query/hash
        path = href.split("#")[0].split("?")[0]
        if path == "":
            continue
        # check against valid routes or asset files
        # route normalization
        test_route = path if path.endswith("/") else path
        # map /foo -> /foo.html exists?
        if test_route in valid_routes:
            continue
        # try /foo -> /foo.html
        candidate = PUB + path.replace("/", os.sep)
        if os.path.isfile(candidate):
            continue
        if os.path.isfile(candidate + ".html"):
            continue
        # asset files
        if path in asset_files:
            continue
        # /blog/x -> /blog/x/index.html
        if os.path.isfile(os.path.join(PUB, path.lstrip("/").replace("/", os.sep), "index.html")):
            continue
        broken.append(href)
    if broken:
        issues.append("BROKEN_LINK(%d:%s)" % (len(broken), ",".join(broken[:3])))

    # 11. Affiliate links
    bad_aff = []
    for a in links:
        href = a.get("href", "")
        if not any(d in href for d in AFFILIATE_DOMAINS):
            continue
        rel_val = a.get("rel")
        if isinstance(rel_val, list):
            rel_attr = " ".join(rel_val).lower()
        else:
            rel_attr = (rel_val or "").lower()
        target = (a.get("target") or "").lower()
        if "sponsored" not in rel_attr or "nofollow" not in rel_attr or "noopener" not in rel_attr:
            bad_aff.append(href + "|rel=" + rel_attr)
        if target != "_blank":
            bad_aff.append(href + "|target=" + target)
    if bad_aff:
        issues.append("AFF_BAD_REL(%d)" % len(bad_aff))

    # 12. 18+ disclaimer
    text = soup.get_text(" ", strip=True)
    if "18+" not in text and "18 +" not in text:
        issues.append("NO_18PLUS")

    # 13. Responsible gambling link
    rg_ok = ("gamblinghelponline" in html.lower()) or ("1800 858 858" in text) or ("1800858858" in html)
    if not rg_ok:
        issues.append("NO_RG_LINK")

    # 14. Viewport
    vp = soup.find("meta", attrs={"name": "viewport"})
    if not vp:
        issues.append("NO_VIEWPORT")

    # 15. OG tags
    og_missing = []
    for prop in ["og:title", "og:description", "og:image"]:
        if not soup.find("meta", attrs={"property": prop}):
            og_missing.append(prop)
    if og_missing:
        issues.append("OG_MISSING(%s)" % ",".join(og_missing))

    # 16. Robots meta
    robots = soup.find("meta", attrs={"name": "robots"})
    if not robots:
        issues.append("NO_ROBOTS_META")
    else:
        rc = robots.get("content", "").lower()
        if is_noindex:
            if "noindex" not in rc:
                issues.append("ROBOTS_NOT_NOINDEX")
        else:
            if "noindex" in rc:
                issues.append("ROBOTS_UNEXPECTED_NOINDEX")
            if "follow" not in rc:
                issues.append("ROBOTS_NO_FOLLOW")

    # 17. Word count (content pages)
    # strip nav/footer/popout
    main = soup.find("main")
    if main:
        # remove script/style
        for t in main.find_all(["script", "style", "nav"]):
            t.decompose()
        words = len(main.get_text(" ", strip=True).split())
    else:
        words = 0
    # review/utility pages are exempt
    exempt = slug in ("/", "/blog", "/about", "/contact", "/privacy", "/terms",
                      "/methodology", "/research", "/press", "/responsible-gambling",
                      "/404") or slug.startswith("/blog/") or slug.endswith("-review")
    if not exempt and words < 800:
        issues.append("THIN_CONTENT(%d)" % words)

    rows.append({
        "page": slug,
        "title_len": len(title),
        "desc_len": len(desc),
        "h1_count": len(h1s),
        "words": words,
        "images": len(imgs),
        "issues": "; ".join(issues) if issues else "PASS",
        "issue_count": len(issues),
    })

# ---------------------------------------------------------------------------
# Write report
# ---------------------------------------------------------------------------
out_md = os.path.join(ROOT, "_seo_scripts", "audit_report.md")
out_csv = os.path.join(ROOT, "_seo_scripts", "audit_report.csv")

# Markdown
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# bpaau.org Technical SEO Audit — Initial Pass\n\n")
    f.write("Pages scanned: %d\n\n" % len(rows))
    f.write("| Page | Title len | Desc len | H1 | Words | Img | Issues |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for r in sorted(rows, key=lambda x: (-x["issue_count"], x["page"])):
        f.write("| `%s` | %d | %d | %d | %d | %d | %s |\n" % (
            r["page"], r["title_len"], r["desc_len"], r["h1_count"],
            r["words"], r["images"], r["issues"][:300]))

# CSV
with open(out_csv, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["page", "title_len", "desc_len", "h1_count", "words", "images", "issue_count", "issues"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

# Summary
total = len(rows)
fails = sum(1 for r in rows if r["issues"] != "PASS")
critical = 0
for r in rows:
    for issue in r["issues"].split("; "):
        if any(k in issue for k in ["BROKEN_LINK", "CANONICAL_MISSING", "CANONICAL_MISMATCH",
                                     "IMG_NO_ALT", "TITLE_LONG", "DESC_LONG", "DESC_SHORT",
                                     "H1_MISSING", "H1_MULTI", "NO_18PLUS", "NO_RG_LINK",
                                     "AFF_BAD_REL", "THIN_CONTENT"]):
            critical += 1
print("Pages scanned:", total)
print("Pages with issues:", fails)
print("Total issue strings:", sum(r["issue_count"] for r in rows))
print("Reports written to:", out_md, out_csv)

# Print per-page issue summary
print("\n--- ISSUE SUMMARY (pages with issues) ---")
for r in sorted(rows, key=lambda x: (-x["issue_count"], x["page"])):
    if r["issues"] != "PASS":
        print("%s  [%d]  %s" % (r["page"], r["issue_count"], r["issues"][:200]))
