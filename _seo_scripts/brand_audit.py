#!/usr/bin/env python3
"""
Brand Review Pages SEO Audit — bpaau2
Checks the 6 enhanced brand review pages against the 100/100 checklist.
Outputs: SEO_AUDIT_BRAND_PAGES.md
"""
import os, re, json, sys
from bs4 import BeautifulSoup

ROOT = r"C:\Users\User\Documents\GitHub\bpaau2"
PUB = os.path.join(ROOT, "public")

PAGES = [
    "1xaud-review.html",
    "gd8-review.html",
    "mrbluey-review.html",
    "1xace-review.html",
    "garcat8-review.html",
    "toystory9-review.html",
]

AFFILIATE_DOMAINS = [
    "1xaud.com", "gd8au.com", "mrblueyau.com",
    "toystory9au.com", "garcat8.com", "1xaceau.com",
]

# Build valid routes
valid_routes = set()
asset_files = set()
for dirpath, dirnames, filenames in os.walk(PUB):
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = "/" + os.path.relpath(full, PUB).replace("\\", "/")
        if fn.endswith(".html"):
            slug = rel[:-5] if not rel.endswith("/index.html") else "/" + rel[:-len("index.html")]
            if rel == "/index.html":
                slug = "/"
            valid_routes.add(slug)
        else:
            asset_files.add(rel)

def audit_page(filename):
    path = os.path.join(PUB, filename)
    slug = "/" + filename[:-5]
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    checks = {}
    issues = []
    
    # 1. Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    checks["title_present"] = bool(title)
    checks["title_length_ok"] = 0 < len(title) <= 60
    if not title:
        issues.append("TITLE_MISSING")
    elif len(title) > 60:
        issues.append(f"TITLE_LONG({len(title)})")
    
    # 2. Meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag.get("content", "").strip() if desc_tag else ""
    checks["desc_present"] = bool(desc)
    checks["desc_length_ok"] = 139 <= len(desc) <= 160
    if not desc:
        issues.append("DESC_MISSING")
    elif len(desc) < 139:
        issues.append(f"DESC_SHORT({len(desc)})")
    elif len(desc) > 160:
        issues.append(f"DESC_LONG({len(desc)})")
    
    # 3. H1
    h1s = soup.find_all("h1")
    checks["h1_exactly_one"] = len(h1s) == 1
    if len(h1s) == 0:
        issues.append("H1_MISSING")
    elif len(h1s) > 1:
        issues.append(f"H1_MULTI({len(h1s)})")
    
    # 4. Heading hierarchy
    headings = [int(h.name[1]) for h in soup.find_all(["h1","h2","h3","h4","h5","h6"])]
    prev = 0
    hierarchy_ok = True
    for lv in headings:
        if prev and lv > prev + 1:
            hierarchy_ok = False
            issues.append(f"H_SKIP({prev}->{lv})")
            break
        prev = lv
    checks["heading_hierarchy"] = hierarchy_ok
    
    # 5. Canonical
    canon = soup.find("link", attrs={"rel": "canonical"})
    expected_canon = f"https://bpaau.org{slug}"
    canon_ok = canon and canon.get("href", "") == expected_canon
    checks["canonical_ok"] = canon_ok
    if not canon:
        issues.append("CANONICAL_MISSING")
    elif canon.get("href", "") != expected_canon:
        issues.append(f"CANONICAL_MISMATCH({canon.get('href','')})")
    
    # 6. Robots
    robots = soup.find("meta", attrs={"name": "robots"})
    robots_ok = robots and "index" in robots.get("content","").lower() and "follow" in robots.get("content","").lower()
    checks["robots_ok"] = robots_ok
    if not robots_ok:
        issues.append("ROBOTS_BAD")
    
    # 7. JSON-LD
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    ld_types = []
    json_valid = True
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
        except Exception as e:
            json_valid = False
            issues.append(f"JSONLD_INVALID: {e}")
    
    checks["jsonld_valid"] = json_valid
    for required_type in ["WebSite", "Organization", "BreadcrumbList", "Review", "Product", "FAQPage", "Article"]:
        has = any(t == required_type for t in ld_types)
        # AggregateRating is inside Product, check separately
        checks[f"ld_{required_type.lower()}"] = has
        if not has:
            issues.append(f"LD_NO_{required_type.upper()}")
    
    # Check AggregateRating inside Product
    has_agg_rating = False
    for sc in scripts:
        try:
            data = json.loads(sc.string or "{}")
            if isinstance(data, dict) and data.get("@type") == "Product":
                if "aggregateRating" in data:
                    has_agg_rating = True
        except:
            pass
    checks["ld_aggregaterating"] = has_agg_rating
    if not has_agg_rating:
        issues.append("LD_NO_AGGREGATERATING")
    
    # 8. Images
    imgs = soup.find_all("img")
    missing_alt = [i for i in imgs if not i.get("alt") or not i.get("alt","").strip()]
    missing_dim = [i for i in imgs if not i.get("width") or not i.get("height")]
    checks["img_all_alt"] = len(missing_alt) == 0
    checks["img_all_dimensions"] = len(missing_dim) == 0
    if missing_alt:
        issues.append(f"IMG_NO_ALT({len(missing_alt)})")
    if missing_dim:
        issues.append(f"IMG_NO_DIM({len(missing_dim)})")
    
    # 9. Internal links
    links = soup.find_all("a", href=True)
    broken = []
    for a in links:
        href = a["href"].strip()
        if not href.startswith("/"):
            continue
        link_path = href.split("#")[0].split("?")[0]
        if link_path == "":
            continue
        if link_path in valid_routes or link_path in asset_files:
            continue
        candidate = PUB + link_path.replace("/", os.sep)
        if os.path.isfile(candidate) or os.path.isfile(candidate + ".html"):
            continue
        if os.path.isfile(os.path.join(PUB, link_path.lstrip("/").replace("/", os.sep), "index.html")):
            continue
        broken.append(href)
    checks["internal_links_valid"] = len(broken) == 0
    if broken:
        issues.append(f"BROKEN_LINK({len(broken)}:{','.join(broken[:3])})")
    
    # 10. Affiliate links
    bad_aff = []
    for a in links:
        href = a.get("href", "")
        if not any(d in href for d in AFFILIATE_DOMAINS):
            continue
        rel_val = a.get("rel")
        rel_attr = " ".join(rel_val).lower() if isinstance(rel_val, list) else (rel_val or "").lower()
        target = (a.get("target") or "").lower()
        if "sponsored" not in rel_attr or "nofollow" not in rel_attr or "noopener" not in rel_attr:
            bad_aff.append(f"{href}|rel={rel_attr}")
        if target != "_blank":
            bad_aff.append(f"{href}|target={target}")
    checks["affiliate_rel_ok"] = len(bad_aff) == 0
    if bad_aff:
        issues.append(f"AFF_BAD_REL({len(bad_aff)})")
    
    # 11. No JS (except JSON-LD)
    all_scripts = soup.find_all("script")
    non_jsonld = [s for s in all_scripts if s.get("type") != "application/ld+json"]
    checks["no_js"] = len(non_jsonld) == 0
    if non_jsonld:
        issues.append(f"JS_FOUND({len(non_jsonld)})")
    
    # 12. No external fonts
    has_google_fonts = "fonts.googleapis.com" in html or "fonts.gstatic.com" in html
    checks["no_external_fonts"] = not has_google_fonts
    if has_google_fonts:
        issues.append("EXTERNAL_FONTS")
    
    # 13. 18+
    text = soup.get_text(" ", strip=True)
    checks["has_18plus"] = "18+" in text or "18 +" in text
    if not checks["has_18plus"]:
        issues.append("NO_18PLUS")
    
    # 14. Curacao
    checks["has_curacao"] = "curacao" in text.lower() or "curaçao" in text.lower()
    if not checks["has_curacao"]:
        issues.append("NO_CURACAO")
    
    # 15. Word count
    main = soup.find("main")
    if main:
        for t in main.find_all(["script", "style", "nav"]):
            t.decompose()
        words = len(main.get_text(" ", strip=True).split())
    else:
        words = 0
    checks["word_count_2000plus"] = words >= 2000
    if words < 2000:
        issues.append(f"THIN_CONTENT({words})")
    
    # 16. CSS version
    css_link = soup.find("link", attrs={"rel": "stylesheet"})
    css_ok = css_link and "theme.css?v=20260915" in css_link.get("href", "")
    checks["css_version_ok"] = css_ok
    if not css_ok:
        issues.append("CSS_VERSION_WRONG")
    
    # 17. File size
    file_size = os.path.getsize(path)
    checks["size_25k_plus"] = file_size >= 25000
    if file_size < 25000:
        issues.append(f"FILE_TOO_SMALL({file_size})")
    
    # 18. Product grid preserved (6 cards)
    product_cards = soup.find_all("article", class_="product-card")
    checks["product_grid_6cards"] = len(product_cards) == 6
    if len(product_cards) != 6:
        issues.append(f"PRODUCT_GRID_COUNT({len(product_cards)})")
    
    # 19. FAQ count >= 8
    faq_items = soup.find_all("details", class_="faq-item")
    checks["faq_8plus"] = len(faq_items) >= 8
    if len(faq_items) < 8:
        issues.append(f"FAQ_TOO_FEW({len(faq_items)})")
    
    # 20. Viewport
    vp = soup.find("meta", attrs={"name": "viewport"})
    checks["viewport_present"] = bool(vp)
    
    # 21. OG tags
    og_ok = all(soup.find("meta", attrs={"property": p}) for p in ["og:title", "og:description", "og:image"])
    checks["og_tags_ok"] = og_ok
    
    # Score
    total_checks = len(checks)
    passed = sum(1 for v in checks.values() if v)
    score = round(passed / total_checks * 100)
    
    return {
        "filename": filename,
        "slug": slug,
        "title": title,
        "title_len": len(title),
        "desc_len": len(desc),
        "words": words,
        "file_size": file_size,
        "h1_count": len(h1s),
        "faq_count": len(faq_items),
        "product_cards": len(product_cards),
        "checks": checks,
        "passed": passed,
        "total_checks": total_checks,
        "score": score,
        "issues": issues,
    }

# Run audit
results = []
for page in PAGES:
    results.append(audit_page(page))

# Write report
out_path = os.path.join(ROOT, "SEO_AUDIT_BRAND_PAGES.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# SEO Audit Report — Brand Review Pages\n\n")
    f.write(f"**Audit date:** 2026-09-15\n")
    f.write(f"**Pages audited:** {len(PAGES)}\n")
    f.write(f"**Checks per page:** {results[0]['total_checks'] if results else 0}\n\n")
    
    # Summary table
    f.write("## Summary\n\n")
    f.write("| Page | Size | Words | H1 | FAQ | Cards | Score | Status |\n")
    f.write("|---|---|---|---|---|---|---|---|\n")
    for r in results:
        status = "✅ PASS" if r["score"] == 100 else f"⚠️ {r['score']}/100"
        f.write(f"| `{r['filename']}` | {r['file_size']:,}B | {r['words']} | {r['h1_count']} | {r['faq_count']} | {r['product_cards']} | **{r['score']}/100** | {status} |\n")
    
    # Per-page details
    f.write("\n## Per-Page Details\n\n")
    for r in results:
        f.write(f"### {r['filename']} — {r['score']}/100\n\n")
        f.write(f"- **Title** ({r['title_len']} chars): {r['title']}\n")
        f.write(f"- **Meta desc** ({r['desc_len']} chars)\n")
        f.write(f"- **Words:** {r['words']} | **File size:** {r['file_size']:,} bytes\n")
        f.write(f"- **H1 count:** {r['h1_count']} | **FAQ items:** {r['faq_count']} | **Product cards:** {r['product_cards']}\n\n")
        
        f.write("| Check | Result |\n|---|---|\n")
        for check_name, passed in r["checks"].items():
            status = "✅" if passed else "❌"
            f.write(f"| {check_name} | {status} |\n")
        
        if r["issues"]:
            f.write(f"\n**Issues:** {'; '.join(r['issues'])}\n")
        else:
            f.write("\n**No issues — perfect score.**\n")
        f.write("\n---\n\n")

# Print summary
print("=" * 60)
print("BRAND PAGE SEO AUDIT RESULTS")
print("=" * 60)
all_pass = True
for r in results:
    status = "PASS" if r["score"] == 100 else "FAIL"
    if r["score"] < 100:
        all_pass = False
    print(f"{r['filename']:30s} {r['score']:3d}/100  words={r['words']:5d}  size={r['file_size']:7d}  [{status}]")
    if r["issues"]:
        for iss in r["issues"]:
            print(f"  - {iss}")
print("=" * 60)
print(f"Report written to: {out_path}")
print(f"Overall: {'ALL PASS 100/100' if all_pass else 'SOME PAGES NEED FIXES'}")
