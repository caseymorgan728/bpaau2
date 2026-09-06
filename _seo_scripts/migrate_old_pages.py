#!/usr/bin/env python3
"""Migrate old-template utility/blog pages to the new SEO-first template.

For each old-template page, preserves the unique content (title, meta,
main inner HTML, non-standard JSON-LD) and rewraps with the new
head / CSS-only header / footer used by index.html and the new guide pages.
"""
import os, re, json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
DOMAIN = "bpaau.org"
ORIGIN = "https://bpaau.org"

# Pages still on the old template (shell / header-bar / button nav-toggle / old footer)
OLD_PAGES = [
    "404.html",
    "about.html",
    "contact.html",
    "methodology.html",
    "press.html",
    "privacy.html",
    "research.html",
    "responsible-gambling.html",
    "terms.html",
    "blog/index.html",
    "blog/bonus-guides/index.html",
    "blog/fast-cashouts/index.html",
    "blog/promo-guides/index.html",
    "blog/top-pokies/index.html",
    "blog/winning-tips/index.html",
]

# Map old nav hrefs to new clean URLs
NAV_REWRITE = {
    "/#pokies": "/best-high-rtp-pokies-australia-2026",
    "/#bonuses": "/no-deposit-free-bonus-guide-australia-2026",
    "/#fast": "/payid-cashouts-australia-2026",
    "/freecredit777-review": "/curacao-casino-licence-check-australia-2026",
    "/blog/": "/blog",
    "/blog/top-pokies/": "/blog/top-pokies",
    "/blog/bonus-guides/": "/blog/bonus-guides",
    "/blog/fast-cashouts/": "/blog/fast-cashouts",
    "/blog/winning-tips/": "/blog/winning-tips",
    "/blog/promo-guides/": "/blog/promo-guides",
}

def clean_internal_href(href):
    if not href:
        return href
    if href.startswith(("http://", "https://", "//", "mailto:", "tel:", "javascript:")):
        return href
    # strip trailing slash on /foo/
    # rewrite old anchors
    if href in NAV_REWRITE:
        href = NAV_REWRITE[href]
    # .html extension -> clean
    if href.endswith(".html"):
        href = "/" + href[1:-5] if href.startswith("/") else href[:-5]
    # /blog/ -> /blog
    if href == "/blog/":
        href = "/blog"
    # strip trailing slash except root
    if href != "/" and href.endswith("/"):
        href = href[:-1]
    return href

def slug_for(rel_path):
    if rel_path.endswith("/index.html"):
        return "/" + rel_path[: -len("/index.html")]
    if rel_path == "index.html":
        return "/"
    if rel_path.endswith(".html"):
        return "/" + rel_path[:-5]
    return "/" + rel_path

def build_head(title, desc, robots, canonical_slug, og_image, og_type, extra_ld):
    og_title = title
    lines = []
    lines.append('<!doctype html>')
    lines.append('<html lang="en-AU">')
    lines.append('<head>')
    lines.append('  <meta charset="utf-8">')
    lines.append('  <meta name="viewport" content="width=device-width, initial-scale=1">')
    lines.append('  <meta name="theme-color" content="#0d1117">')
    lines.append(f'  <title>{title}</title>')
    lines.append(f'  <meta name="description" content="{desc}">')
    lines.append(f'  <meta name="robots" content="{robots}">')
    lines.append(f'  <link rel="canonical" href="{ORIGIN}{canonical_slug}">')
    lines.append('  <link rel="icon" type="image/png" href="/assets/favicon-32.png">')
    lines.append('  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">')
    lines.append('  <link rel="manifest" href="/site.webmanifest">')
    lines.append('  <link rel="stylesheet" href="/assets/theme.css">')
    lines.append('')
    lines.append('  <meta property="og:site_name" content="BPAAU">')
    lines.append(f'  <meta property="og:title" content="{og_title}">')
    lines.append(f'  <meta property="og:description" content="{desc}">')
    lines.append(f'  <meta property="og:type" content="{og_type}">')
    lines.append(f'  <meta property="og:url" content="{ORIGIN}{canonical_slug}">')
    lines.append(f'  <meta property="og:image" content="{og_image}">')
    lines.append('  <meta property="og:locale" content="en_AU">')
    lines.append('')
    lines.append('  <meta name="twitter:card" content="summary_large_image">')
    lines.append(f'  <meta name="twitter:title" content="{og_title}">')
    lines.append(f'  <meta name="twitter:description" content="{desc}">')
    lines.append(f'  <meta name="twitter:image" content="{og_image}">')
    lines.append('')
    # Standard JSON-LD
    lines.append(f'  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"BPAAU","url":"{ORIGIN}/","inLanguage":"en-AU"}}</script>')
    lines.append(f'  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"BPAAU","alternateName":"Best Pokies Australia","url":"{ORIGIN}/","logo":"{ORIGIN}/assets/logo.png","sameAs":["https://bpaau.com"]}}</script>')
    # BreadcrumbList derived from canonical
    if canonical_slug == "/":
        crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":f"{ORIGIN}/"}]
    else:
        parts = [p for p in canonical_slug.split("/") if p]
        crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":f"{ORIGIN}/"}]
        path = ""
        names = {"blog": "Blog", "bonus-guides": "Bonus Guides", "fast-cashouts": "Fast Cashouts",
                 "winning-tips": "Winning Tips", "promo-guides": "Promo Guides", "top-pokies": "Top Pokies"}
        for i, p in enumerate(parts, start=2):
            path += "/" + p
            name = names.get(p, p.replace("-", " ").title())
            crumbs.append({"@type":"ListItem","position":i,"name":name,"item":f"{ORIGIN}{path}"})
    lines.append('  <script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs}, ensure_ascii=False) + '</script>')
    for ld in extra_ld:
        lines.append('  <script type="application/ld+json">' + ld + '</script>')
    lines.append('</head>')
    return "\n".join(lines)

HEADER_TMPL = '''<body>
  <a class="skip-link" href="#main-content">Skip to content</a>

  <header class="site-header">
    <div class="container">
      <div class="header-inner">
        <a class="brand-logo" href="/" aria-label="BPAAU home">
          <img src="/assets/logo.png" alt="BPAAU — Best Pokies Australia" width="240" height="72" loading="eager" decoding="async">
        </a>
        <input type="checkbox" id="nav-toggle" class="nav-toggle" hidden>
        <label for="nav-toggle" class="nav-toggle-label" aria-label="Toggle navigation">
          <span></span><span></span><span></span>
        </label>
        <nav class="nav" aria-label="Primary">
          <a class="nav__link" href="/">Home</a>
          <a class="nav__link" href="/best-high-rtp-pokies-australia-2026">Best Pokies</a>
          <a class="nav__link" href="/no-deposit-free-bonus-guide-australia-2026">Free Bonus</a>
          <a class="nav__link" href="/payid-cashouts-australia-2026">Fast Payouts</a>
          <a class="nav__link" href="/curacao-casino-licence-check-australia-2026">Curacao Verified</a>
          <a class="nav__link" href="/blog">Blog</a>
          <a class="nav__link" href="/about">About</a>
        </nav>
      </div>
    </div>
  </header>'''

FOOTER_TMPL = '''  <footer class="site-footer">
    <div class="container">
      <nav class="footer-nav" aria-label="Footer">
        <a href="/">Home</a>
        <a href="/best-high-rtp-pokies-australia-2026">Best Pokies</a>
        <a href="/no-deposit-free-bonus-guide-australia-2026">Free Bonus</a>
        <a href="/payid-cashouts-australia-2026">Fast Payouts</a>
        <a href="/blog">Blog</a>
        <a href="/about">About</a>
        <a href="/methodology">Methodology</a>
        <a href="/responsible-gambling">Responsible Gambling</a>
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
        <a href="/contact">Contact</a>
      </nav>
      <p class="footer-note">18+ only. BPAAU is an independent comparison site. All listed operators hold Gaming Curacao licences. Gamble responsibly.</p>
      <p class="footer-note"><strong>Editorial Disclosure:</strong> bpaau.org is an independent information portal. Some outbound links are affiliate links — we may receive a commission. This never influences our rankings. Real-money online pokies are regulated under the Interactive Gambling Act 2001 (Cth).</p>
    </div>
  </footer>
</body>
</html>'''

RG_BANNER = '''      <aside class="rg-banner" role="note">
        <strong>18+ Only.</strong> Gambling is addictive. Gamble responsibly. Free 24/7 support:
        <a href="tel:1800858858">1800 858 858</a> &middot;
        <a href="https://www.gamblinghelponline.org.au" target="_blank" rel="noopener">gamblinghelponline.org.au</a> &middot;
        <a href="https://www.betstop.gov.au" target="_blank" rel="noopener">BetStop</a>
      </aside>'''

def migrate(rel):
    fp = os.path.join(PUB, rel.replace("/", os.sep))
    with open(fp, "r", encoding="utf-8") as f:
        raw = f.read()
    soup = BeautifulSoup(raw, "html.parser")

    # Extract head metadata
    title = soup.title.get_text(strip=True) if soup.title else "BPAAU"
    desc = soup.find("meta", attrs={"name": "description"})
    desc = desc.get("content", "") if desc else ""
    robots = soup.find("meta", attrs={"name": "robots"})
    robots = robots.get("content", "index,follow,max-image-preview:large") if robots else "index,follow,max-image-preview:large"
    og_img = soup.find("meta", attrs={"property": "og:image"})
    og_img = og_img.get("content", "https://bpaau.org/assets/hero/main-hero.webp") if og_img else "https://bpaau.org/assets/hero/main-hero.webp"
    og_type = soup.find("meta", attrs={"property": "og:type"})
    og_type = og_type.get("content", "website") if og_type else "website"

    canonical_slug = slug_for(rel)

    # Extract non-standard JSON-LD (skip WebSite, Organization, BreadcrumbList — we regenerate)
    extra_ld = []
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(s.string or s.get_text())
        except Exception:
            continue
        t = data.get("@type") if isinstance(data, dict) else None
        if t in ("WebSite", "Organization", "BreadcrumbList"):
            continue
        extra_ld.append(json.dumps(data, ensure_ascii=False))

    # Extract main content
    main = soup.find("main")
    if main is None:
        body = soup.body
        main_inner = body.decode_contents() if body else ""
    else:
        main_inner = main.decode_contents()

    # Remove the broken rg-ph-wrap block
    main_inner = re.sub(r'<div class="shell rg-ph-wrap">.*?</div>\s*', '', main_inner, flags=re.S)
    # Also remove any stray rg-ph img
    main_inner = re.sub(r'<img[^>]*class="[^"]*rg-ph[^"]*"[^>]*>', '', main_inner)
    # Remove old rg-banner (we add a fresh one in the new template)
    main_inner = re.sub(r'<aside class="rg-banner"[^>]*>.*?</aside>', '', main_inner, flags=re.S)
    # Remove the opening <div class="shell"> that directly wraps the rg-banner in old pages
    # (it's now empty after stripping the banner + rg-ph-wrap)
    main_inner = re.sub(r'<div class="shell">\s*</div>', '', main_inner, flags=re.S)

    # Rewrite internal links in main_inner
    def rewrite_href(m):
        q = m.group(1)
        return f'href="{clean_internal_href(q)}"'
    main_inner = re.sub(r'href="([^"]+)"', rewrite_href, main_inner)

    # Replace .shell with .container in main_inner (top-level wrappers)
    # We'll convert <div class="shell"> to nothing (the container is provided by main wrapper)
    # Actually, the new template wraps main content in <div class="container">. Old pages have
    # nested .shell divs. Replace class="shell" with class="container" — CSS will center them.
    main_inner = re.sub(r'class="shell"', 'class="container"', main_inner)
    main_inner = re.sub(r'class="shell rg-ph-wrap"', '', main_inner)

    # Add dimensions/loading to imgs that lack them (blog cards in old pages already have them)
    # Add loading=lazy decoding=async to imgs without it
    def fix_img(m):
        tag = m.group(0)
        if "loading=" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        if "decoding=" not in tag:
            tag = tag[:-1] + ' decoding="async">'
        return tag
    # Only fix imgs that don't already have both attrs
    def fix_img_tag(m):
        tag = m.group(0)
        if "loading=" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        if "decoding=" not in tag:
            tag = tag[:-1] + ' decoding="async">'
        return tag
    # Skip — old blog imgs already have them. We'll rely on audit to catch.

    # Build new page
    head = build_head(title, desc, robots, canonical_slug, og_img, og_type, extra_ld)
    out = []
    out.append(head)
    out.append(HEADER_TMPL)
    out.append('')
    out.append('  <main id="main-content">')
    out.append('    <div class="container">')
    out.append(RG_BANNER)
    out.append('')
    # Indent main_inner one level
    for line in main_inner.split("\n"):
        out.append("    " + line if line.strip() else "")
    out.append('')
    out.append('    </div>')
    out.append('  </main>')
    out.append(FOOTER_TMPL)

    with open(fp, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"migrated {rel}")

for rel in OLD_PAGES:
    migrate(rel)
