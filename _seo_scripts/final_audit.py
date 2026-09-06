#!/usr/bin/env python3
"""Final comprehensive SEO audit for bpaau.org."""
import os, re, json, sys, urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(r"C:\Users\User\Documents\GitHub\Australia igaming website\public")
SITE = "https://bpaau.org"

PROTECTED = {
    "1XAUD": "1xaud.com/register",
    "GD8": "gd8au.com/register",
    "MR BLUEY": "mrblueyau.com/register",
    "TOY STORY 9": "toystory9au.com/register",
    "GARCAT8": "garcat8.com/register",
    "1XACE": "1xaceau.com/register",
}

issues = []          # (severity, page, check, detail)
summary = {}
titles_seen = {}
descs_seen = {}

def log(sev, page, check, detail):
    issues.append((sev, page, check, detail))

def html_to_slug(path: Path) -> str:
    rel = path.relative_to(BASE).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("/index.html")]
    return "/" + rel[:-len(".html")]

def slug_to_canonical(slug: str) -> str:
    if slug == "/":
        return SITE + "/"
    return SITE + slug.rstrip("/")

def file_exists_for_url(url_path: str) -> bool:
    """Given an internal path like /foo or /foo/bar/, check file exists."""
    # strip query/fragment
    p = url_path.split("#", 1)[0].split("?", 1)[0]
    p = urllib.parse.unquote(p)  # decode %20
    if p.startswith("/"):
        p = p[1:]
    if p == "":
        return (BASE / "index.html").exists()
    # strip trailing slash for test
    p_norm = p.rstrip("/")
    candidates = []
    # /foo  -> foo.html, foo/index.html
    candidates.append(BASE / (p_norm + ".html"))
    candidates.append(BASE / p_norm / "index.html")
    candidates.append(BASE / p_norm)
    for c in candidates:
        if c.exists():
            return True
    return False

def word_count(soup):
    # strip script/style/noscript (on a copy so we don't mutate the live soup)
    import copy
    s2 = BeautifulSoup(str(soup), "html.parser")
    for t in s2(["script", "style", "noscript"]):
        t.decompose()
    txt = s2.get_text(" ", strip=True)
    return len([w for w in re.split(r"\s+", txt) if w])

def audit_file(path: Path):
    rel = path.relative_to(BASE).as_posix()
    slug = html_to_slug(path)
    raw = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")

    is_404 = rel == "404.html"
    is_verification = rel.startswith("google")  # google verification file

    # ---- meta robots ----
    robots = soup.find("meta", attrs={"name": "robots"})
    if not robots:
        log("ERROR", rel, "meta_robots", "missing")
    else:
        c = robots.get("content", "")
        if is_404:
            if "noindex" not in c:
                log("ERROR", rel, "meta_robots", f"404 should be noindex, got {c!r}")
        else:
            if "noindex" in c:
                log("WARN", rel, "meta_robots", f"indexable page has noindex: {c!r}")
            if "index" not in c or "follow" not in c:
                log("WARN", rel, "meta_robots", f"unexpected: {c!r}")

    # ---- canonical ----
    canon = soup.find("link", attrs={"rel": "canonical"})
    if not canon:
        log("ERROR", rel, "canonical", "missing")
    else:
        href = canon.get("href", "")
        expected = slug_to_canonical(slug)
        if href != expected:
            log("WARN", rel, "canonical", f"got {href!r} expected {expected!r}")

    # ---- title ----
    title = soup.title.get_text(strip=True) if soup.title else ""
    if not title:
        log("ERROR", rel, "title", "missing")
    else:
        n = len(title)
        if n > 60:
            log("WARN", rel, "title_len", f"{n} chars: {title!r}")
        if title in titles_seen:
            log("WARN", rel, "title_dup", f"duplicate with {titles_seen[title]}")
        titles_seen[title] = rel

    # ---- meta description ----
    desc = soup.find("meta", attrs={"name": "description"})
    if not desc:
        log("ERROR", rel, "description", "missing")
    else:
        d = desc.get("content", "").strip()
        n = len(d)
        if n < 130 or n > 165:
            log("INFO", rel, "desc_len", f"{n} chars")
        if d in descs_seen:
            log("WARN", rel, "desc_dup", f"duplicate with {descs_seen[d]}")
        descs_seen[d] = rel

    # ---- H1 ----
    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        log("ERROR", rel, "h1", f"{len(h1s)} h1 tags")

    # ---- OG / Twitter ----
    og_keys = ["og:title", "og:description", "og:type", "og:url", "og:image"]
    for k in og_keys:
        if not soup.find("meta", attrs={"property": k}):
            log("WARN", rel, "og", f"missing {k}")
    if not soup.find("meta", attrs={"name": "twitter:card"}):
        log("WARN", rel, "twitter", "missing twitter:card")

    # ---- viewport ----
    if not soup.find("meta", attrs={"name": "viewport"}):
        log("ERROR", rel, "viewport", "missing")

    # ---- lang ----
    html_tag = soup.find("html")
    if not html_tag or html_tag.get("lang") != "en-AU":
        log("WARN", rel, "lang", f"got {html_tag.get('lang') if html_tag else None!r}")

    # ---- word count ----
    wc = word_count(soup)
    if not is_404 and not is_verification:
        if wc < 800:
            log("WARN", rel, "wordcount", f"{wc} words (<800)")

    # ---- H tag hierarchy ----
    tags = [t.name for t in soup.find_all(["h1", "h2", "h3", "h4"])]
    # simple check: no H3 before H2, no H2 before H1 (after first h1)
    seen_h1 = False
    issues_h = []
    for t in tags:
        if t == "h1":
            seen_h1 = True
        elif t == "h2":
            if not seen_h1:
                issues_h.append("h2-before-h1")
        elif t == "h3":
            # need an h2 seen
            if "h2" not in tags[: tags.index(t if hasattr(t, 'name') else "")] if False else False:
                pass
    # simpler: find sequence of levels
    levels = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}
    prev = 0
    for t in tags:
        cur = levels[t]
        if prev and cur - prev > 1:
            log("INFO", rel, "heading_skip", f"{t} after {tags[tags.index(t)-1] if t in tags else ''}")
        prev = cur

    # ---- images ----
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            log("WARN", rel, "img_no_src", str(img)[:100])
            continue
        if src.startswith("data:"):
            continue
        if not img.get("alt"):
            log("WARN", rel, "img_alt", src)
        if not img.get("width") or not img.get("height"):
            log("WARN", rel, "img_dim", src)
        # lazy check: non-hero (not fetchpriority=high) should have loading=lazy
        if "fetchpriority" not in img.attrs and "eager" not in (img.get("loading") or ""):
            pass  # ok if lazy or absent
        # existence check
        if src.startswith("http"):
            continue
        local = src.split("?", 1)[0].split("#", 1)[0]
        if not file_exists_for_url(local):
            log("ERROR", rel, "img_broken", src)

    # ---- scripts (non JSON-LD) ----
    for sc in soup.find_all("script"):
        t = (sc.get("type") or "text/javascript").lower()
        if t == "application/ld+json":
            # validate JSON
            try:
                json.loads(sc.string or sc.get_text() or "")
            except Exception as e:
                log("ERROR", rel, "jsonld_parse", str(e)[:120])
        else:
            log("ERROR", rel, "script_tag", f"non-JSON-LD script: type={t!r} src={sc.get('src')!r}")

    # ---- inline styles ----
    for st in soup.find_all("style"):
        log("WARN", rel, "style_block", "inline <style> block")

    # ---- external fonts ----
    for link in soup.find_all("link"):
        href = link.get("href", "")
        if link.get("rel") and "preload" in link.get("rel") and "font" in href:
            log("WARN", rel, "external_font", href)
        if "fonts.googleapis" in href or "fonts.gstatic" in href:
            log("WARN", rel, "external_font", href)

    # ---- JSON-LD types ----
    types_seen = set()
    for sc in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(sc.string or sc.get_text() or "")
        except Exception:
            continue
        t = data.get("@type")
        if isinstance(t, list):
            for x in t:
                types_seen.add(x)
        elif t:
            types_seen.add(t)
        # also scan @graph
        if "@graph" in data:
            for node in data["@graph"]:
                tt = node.get("@type")
                if isinstance(tt, list):
                    types_seen.update(tt)
                elif tt:
                    types_seen.add(tt)

    if not is_404 and not is_verification:
        for required in ["WebSite", "Organization", "BreadcrumbList"]:
            if required not in types_seen:
                log("WARN", rel, "jsonld", f"missing {required}")

    # ---- internal links ----
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            # external — check affiliate rel
            host = urllib.parse.urlparse(href).netloc.lower()
            is_aff = any(p in href for p in PROTECTED.values()) or any(
                p in host for p in PROTECTED.values()
            )
            if is_aff:
                rel_attr = (a.get("rel") or [])
                if isinstance(rel_attr, str):
                    rel_attr = rel_attr.split()
                rel_set = set(rel_attr)
                need = {"sponsored", "nofollow", "noopener"}
                missing = need - rel_set
                if missing:
                    log("WARN", rel, "aff_rel", f"{href} missing rel={missing}")
                if a.get("target") != "_blank":
                    log("WARN", rel, "aff_target", f"{href} no target=_blank")
            continue
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("#"):
            continue
        if href.startswith("javascript:"):
            log("ERROR", rel, "js_href", href)
            continue
        # clean URL check: no .html
        if href.endswith(".html"):
            log("INFO", rel, "clean_url", f"internal link ends .html: {href}")
        # existence
        path_part = href.split("#", 1)[0].split("?", 1)[0]
        if path_part and not path_part.startswith("data:"):
            if not file_exists_for_url(path_part):
                log("ERROR", rel, "broken_link", f"{href} (from {rel})")

    # ---- FAQ details/summary ----
    details = soup.find_all("details")
    faq_in_html = len(details)

    # ---- RG banner ----
    if not is_404 and not is_verification:
        if "18+" not in raw and "18 +" not in raw:
            log("WARN", rel, "rg_banner", "no 18+ banner found")
        # duplicate rg-banner check
        rg_banners = soup.find_all("aside", class_=re.compile(r"^rg-banner$"))
        if len(rg_banners) > 1:
            log("WARN", rel, "duplicate_rg", f"{len(rg_banners)} rg-banner asides")

    # ---- skip link ----
    if not soup.find("a", class_=re.compile(r"skip")):
        log("WARN", rel, "skip_link", "no skip-to-content")

    # ---- semantic elements ----
    if not soup.find("header"):
        log("INFO", rel, "semantic", "no <header>")
    if not soup.find("main"):
        log("WARN", rel, "semantic", "no <main>")
    if not soup.find("footer"):
        log("WARN", rel, "semantic", "no <footer>")

    return {
        "file": rel,
        "slug": slug,
        "title": title,
        "title_len": len(title),
        "desc_len": len(desc.get("content", "")) if desc else 0,
        "h1": len(h1s),
        "words": wc,
        "faq_details": faq_in_html,
        "jsonld_types": sorted(types_seen),
    }

def main():
    files = sorted(BASE.rglob("*.html"))
    results = []
    for f in files:
        results.append(audit_file(f))

    # robots.txt
    robots_txt = (BASE / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots_txt:
        log("ERROR", "robots.txt", "sitemap_ref", "no Sitemap: line")
    if "Allow: /" not in robots_txt:
        log("WARN", "robots.txt", "allow", "no Allow: /")

    # sitemap.xml
    sm = (BASE / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    sm_paths = set()
    for u in sm_urls:
        if u.startswith(SITE):
            sm_paths.add(u[len(SITE):])
    # every indexable page should be in sitemap
    for r in results:
        if r["file"] == "404.html" or r["file"].startswith("google"):
            continue
        expected_slug = slug_to_canonical(r["slug"]).replace(SITE, "")
        if expected_slug not in sm_paths:
            log("WARN", r["file"], "sitemap", f"missing from sitemap: {expected_slug}")

    # CSS size
    css = BASE / "assets" / "theme.css"
    css_size = css.stat().st_size if css.exists() else -1
    if css_size > 20 * 1024:
        log("WARN", "theme.css", "css_size", f"{css_size} bytes > 20KB")

    # ---- output ----
    print(f"Audited {len(results)} HTML files")
    print(f"CSS size: {css_size} bytes ({css_size/1024:.1f} KB)")
    print(f"Sitemap URLs: {len(sm_urls)}")
    print()
    by_sev = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for sev, *_ in issues:
        by_sev[sev] = by_sev.get(sev, 0) + 1
    print(f"Issues: ERROR={by_sev['ERROR']}  WARN={by_sev['WARN']}  INFO={by_sev['INFO']}")
    print()
    for sev in ["ERROR", "WARN", "INFO"]:
        print(f"--- {sev} ---")
        for s, page, check, detail in issues:
            if s == sev:
                print(f"  [{page}] {check}: {detail}")
        print()

    # word count table
    print("--- Word counts (sorted asc) ---")
    for r in sorted(results, key=lambda x: x["words"]):
        if r["file"] in ("404.html",) or r["file"].startswith("google"):
            continue
        flag = "  <-- LOW" if r["words"] < 800 else ""
        print(f"  {r['words']:5d}w  {r['file']}{flag}")

    # titles
    print()
    print("--- Title lengths ---")
    for r in sorted(results, key=lambda x: x["title_len"]):
        flag = "  <-- LONG" if r["title_len"] > 60 else ""
        print(f"  {r['title_len']:3d}c  {r['file']}: {r['title'][:70]!r}{flag}")

    # save JSON for report
    out = {
        "files": len(results),
        "css_size": css_size,
        "sitemap_urls": len(sm_urls),
        "issues": [{"sev": s, "page": p, "check": c, "detail": d} for s, p, c, d in issues],
        "results": results,
    }
    out_path = BASE.parent / "_seo_scripts" / "audit_results.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
