# -*- coding: utf-8 -*-
"""
Comprehensive canonical/SEO audit for bpaau.org (bpaau2/public).

Checks per HTML file:
  1. Canonical tag present? Expected clean self-referential URL?
  2. Canonical pointing to a different page / .html / http:// / trailing slash issues
  3. Duplicate canonicals (two files -> same canonical)
  4. robots meta: 404.html must be noindex; everything else must be indexable
  5. og:url and twitter:url match canonical
  6. sitemap.xml: every URL matches a page's canonical; no redirected/noindex URLs; https only
  7. redirects.json: targets resolve to real pages; no canonical loops
"""
import os
import re
import sys
import json
from collections import defaultdict

PUBLIC = r"C:\Users\User\Documents\GitHub\bpaau2\public"
ROOT = r"C:\Users\User\Documents\GitHub\bpaau2"
BASE = "https://bpaau.org"

# Files that are not regular HTML content pages
SKIP = {"google6c4a857337176f53.html"}  # Google verification file (plain text)

def expected_canonical(rel_path):
    """Compute the canonical a page SHOULD have from its file path."""
    rel = rel_path.replace("\\", "/")
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        # blog/bonus-guides/index.html -> https://bpaau.org/blog/bonus-guides (no trailing slash)
        return BASE + "/" + rel[:-len("index.html")].rstrip("/")
    if rel.endswith(".html"):
        return BASE + "/" + rel[:-5]
    return None

def find_tag(html, name, attr="href"):
    """Find first tag by name (canonical/meta) and return dict of attrs."""
    # canonical link
    for m in re.finditer(r'<link\b[^>]*>', html, re.IGNORECASE):
        tag = m.group(0)
        if re.search(r'rel\s*=\s*["\']?canonical["\']?', tag, re.IGNORECASE):
            am = re.search(attr + r'\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
            if am:
                return am.group(1)
            am = re.search(attr + r"\s*=\s*'([^']*)'", tag, re.IGNORECASE)
            if am:
                return am.group(1)
            return None
    return None

def find_meta(html, prop):
    """Return content of meta[property=prop] or meta[name=prop], else None."""
    for m in re.finditer(r'<meta\b[^>]*>', html, re.IGNORECASE):
        tag = m.group(0)
        if re.search(r'(?:property|name)\s*=\s*["\']?' + re.escape(prop) + r'["\']?', tag, re.IGNORECASE):
            cm = re.search(r'content\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
            if cm:
                return cm.group(1)
            cm = re.search(r"content\s*=\s*'([^']*)'", tag, re.IGNORECASE)
            if cm:
                return cm.group(1)
            return None
    return None

def find_robots(html):
    return find_meta(html, "robots")

def norm_url(u):
    """Normalise a URL for comparison: strip trailing slash except root."""
    u = u.strip()
    if u == BASE + "/":
        return u
    return u.rstrip("/")

def main():
    findings = []          # list of (level, file, message)
    pages = []             # list of dicts per page
    canonical_owners = defaultdict(list)

    # ---- collect HTML files ----
    for root, dirs, files in os.walk(PUBLIC):
        for fn in sorted(files):
            if not fn.lower().endswith(".html"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, PUBLIC)
            if rel.replace("\\", "/") in SKIP:
                continue
            pages.append({
                "rel": rel.replace("\\", "/"),
                "full": full,
            })

    total = len(pages)
    print(f"Auditing {total} HTML files (excluding verification files)\n")

    for p in pages:
        rel = p["rel"]
        with open(p["full"], "r", encoding="utf-8", errors="replace") as fh:
            html = fh.read()

        canon = find_tag(html, "canonical")
        robots = find_robots(html)
        ogurl = find_meta(html, "og:url")
        twurl = find_meta(html, "twitter:url")
        expected = expected_canonical(rel)

        rec = {
            "file": rel,
            "canonical": canon,
            "expected": expected,
            "robots": robots,
            "og:url": ogurl,
            "twitter:url": twurl,
            "ok": True,
        }

        # --- canonical presence / correctness ---
        if canon is None:
            findings.append(("ERROR", rel, "NO canonical tag"))
            rec["ok"] = False
        else:
            canonical_owners[canon].append(rel)
            if canon != expected:
                findings.append(("ERROR", rel, f"canonical MISMATCH: got '{canon}', expected '{expected}'"))
                rec["ok"] = False
            if canon.endswith(".html"):
                findings.append(("ERROR", rel, f"canonical contains .html: '{canon}'"))
                rec["ok"] = False
            if canon.startswith("http://"):
                findings.append(("ERROR", rel, f"canonical uses http:// : '{canon}'"))
                rec["ok"] = False
            if not canon.startswith("https://bpaau.org"):
                findings.append(("ERROR", rel, f"canonical wrong host: '{canon}'"))
                rec["ok"] = False
            if canon != BASE + "/" and canon.endswith("/"):
                findings.append(("WARN", rel, f"canonical has trailing slash: '{canon}'"))
                rec["ok"] = False
            # canonical points elsewhere?
            norm_c = norm_url(canon)
            norm_e = norm_url(expected) if expected else None
            if norm_e and norm_c != norm_e:
                findings.append(("ERROR", rel, f"canonical points to DIFFERENT page: '{canon}' (self would be '{expected}')"))
                rec["ok"] = False

        # --- robots ---
        if rel == "404.html":
            if robots is None or "noindex" not in robots.lower():
                findings.append(("ERROR", rel, f"404.html missing noindex (robots='{robots}')"))
                rec["ok"] = False
        else:
            if robots is not None and "noindex" in robots.lower():
                findings.append(("ERROR", rel, f"non-404 page has noindex (robots='{robots}')"))
                rec["ok"] = False

        # --- og:url / twitter:url ---
        for tag, val in (("og:url", ogurl), ("twitter:url", twurl)):
            if val is not None:
                if val != canon:
                    findings.append(("ERROR", rel, f"{tag} MISMATCH: '{val}' vs canonical '{canon}'"))
                    rec["ok"] = False
            # missing twitter:url is informational only (Twitter falls back to og:url)
            if val is None and tag == "twitter:url":
                rec["twitter:url"] = "(missing)"
                if rel != "404.html":
                    findings.append(("INFO", rel, "twitter:url missing (informational only)"))

        pages[pages.index(p)] = rec

    # --- duplicate canonicals ---
    dup = {c: owners for c, owners in canonical_owners.items() if len(owners) > 1}
    if dup:
        for c, owners in sorted(dup.items()):
            findings.append(("ERROR", "MULTIPLE", f"duplicate canonical '{c}' owned by {owners}"))
            for o in owners:
                for rec in pages:
                    if rec["file"] == o:
                        rec["ok"] = False

    # --- sitemap check ---
    sm_path = os.path.join(PUBLIC, "sitemap.xml")
    sm_urls = []
    if os.path.exists(sm_path):
        with open(sm_path, "r", encoding="utf-8") as fh:
            sm = fh.read()
        sm_urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm)
        print(f"Sitemap: {len(sm_urls)} URLs\n")
        sm_set = set()
        for u in sm_urls:
            if u in sm_set:
                findings.append(("ERROR", "sitemap.xml", f"duplicate URL in sitemap: {u}"))
            sm_set.add(u)
            if not u.startswith("https://bpaau.org"):
                findings.append(("ERROR", "sitemap.xml", f"non-https/bpaau URL in sitemap: {u}"))
            if u != BASE + "/" and u.endswith("/"):
                findings.append(("ERROR", "sitemap.xml", f"trailing slash in sitemap URL: {u}"))
            if u.endswith(".html"):
                findings.append(("ERROR", "sitemap.xml", f".html URL in sitemap: {u}"))

    # sitemap URLs must match a page canonical 1:1
    page_canons = {rec["canonical"] for rec in pages if rec["canonical"]}
    for u in sm_urls:
        if u not in page_canons:
            # is it a redirect target instead?
            findings.append(("ERROR", "sitemap.xml", f"sitemap URL has no matching page canonical: {u}"))
    for c in sorted(page_canons):
        if c not in sm_set:
            # 404 is intentionally noindex -> excluded from sitemap
            if c == BASE + "/404":
                continue
            findings.append(("WARN", "sitemap", f"page canonical not in sitemap: {c}"))

    # --- redirects.json check ---
    red_path = os.path.join(ROOT, "redirects.json")
    try:
        with open(red_path, "r", encoding="utf-8") as fh:
            red = json.load(fh)
        redmap = red.get("redirects", {})
        for src, dst in sorted(redmap.items()):
            if src == dst:
                findings.append(("ERROR", "redirects.json", f"self-redirect loop: {src} -> {dst}"))
            if dst in redmap:
                findings.append(("ERROR", "redirects.json", f"redirect chain (should be direct): {src} -> {dst} which itself redirects"))
            dst_html = os.path.join(PUBLIC, dst.lstrip("/") + ".html")
            dst_idx = os.path.join(PUBLIC, dst.lstrip("/"), "index.html")
            if not (os.path.exists(dst_html) or os.path.exists(dst_idx)):
                findings.append(("ERROR", "redirects.json", f"redirect target missing file: {dst} (from {src})"))
            # check no canonical loop: the target page's canonical should be dst
            if os.path.exists(dst_html):
                with open(dst_html, "r", encoding="utf-8", errors="replace") as fh:
                    tgt_canon = find_tag(fh.read(), "canonical")
                if tgt_canon and norm_url(tgt_canon) != norm_url(BASE + dst):
                    findings.append(("ERROR", "redirects.json", f"redirect target {dst} canonical '{tgt_canon}' != '{BASE+dst}'"))
    except Exception as e:
        findings.append(("ERROR", "redirects.json", f"could not parse: {e}"))

    # --- report ---
    print("=" * 100)
    print("CANONICAL MAP")
    print("=" * 100)
    for rec in sorted(pages, key=lambda r: r["file"]):
        print(f"{rec['file']:55s} -> {rec['canonical'] or 'MISSING':45s} {'OK' if rec['ok'] else '** ISSUE **'}")

    print("\n" + "=" * 100)
    print("FINDINGS")
    print("=" * 100)
    if findings:
        # sort errors first
        findings.sort(key=lambda f: (0 if f[0] == "ERROR" else (1 if f[0] == "WARN" else 2), f[1], f[2]))
        for level, loc, msg in findings:
            print(f"[{level:5s}] {loc:60s} {msg}")
    else:
        print("No issues found.")

    errs = [f for f in findings if f[0] == "ERROR"]
    warns = [f for f in findings if f[0] == "WARN"]
    infos = [f for f in findings if f[0] == "INFO"]
    print(f"\nSUMMARY: {total} pages audited | {len(errs)} errors | {len(warns)} warnings | {len(infos)} info")
    print(f"Sitemap URLs: {len(sm_urls)} | Page canonicals: {len(page_canons)}")

    # write machine-readable report
    out = {
        "total_pages": total,
        "sitemap_urls": len(sm_urls),
        "errors": [{"level": l, "file": f, "msg": m} for l, f, m in findings],
        "pages": pages,
        "canonical_map": {r["file"]: r["canonical"] for r in pages},
    }
    with open(os.path.join(ROOT, "_seo_scripts", "canonical_audit_report.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Report written to _seo_scripts/canonical_audit_report.json")

    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main())
