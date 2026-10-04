# -*- coding: utf-8 -*-
"""Shared page chrome for BPAAU static pages (matches theme.css template)."""
import json, io, os

DATE = "2026-10-04"
DATE_HUMAN = "4 October 2026"

NAV = [
    ("/", "Home"),
    ("/best-high-rtp-pokies-australia-2026", "Best Pokies"),
    ("/no-deposit-free-bonus-guide-australia-2026", "Free Bonus"),
    ("/payid-cashouts-australia-2026", "Fast Payouts"),
    ("/curacao-casino-licence-check-australia-2026", "Curacao Verified"),
    ("/blog", "Blog"),
    ("/about", "About"),
]

FOOTER = [
    ("/", "Home"),
    ("/best-high-rtp-pokies-australia-2026", "Best Pokies"),
    ("/no-deposit-free-bonus-guide-australia-2026", "Free Bonus"),
    ("/payid-cashouts-australia-2026", "Fast Payouts"),
    ("/blog", "Blog"),
    ("/about", "About"),
    ("/methodology", "Methodology"),
    ("/responsible-gambling", "Responsible Gambling"),
    ("/privacy", "Privacy"),
    ("/terms", "Terms"),
    ("/contact", "Contact"),
]


def head(cfg):
    slug = cfg["slug"]
    url = "https://bpaau.org/" + slug
    title = cfg["title"]
    desc = cfg["desc"]
    ogimg = cfg.get("ogimg", "https://bpaau.org/assets/hero/main-hero.webp")
    crumbs = cfg["crumbs"]  # list of (name, url or None)
    breadcrumb = [{"@type": "ListItem", "position": i + 1,
                   "name": n, **({"item": u} if u else {})}
                  for i, (n, u) in enumerate(crumbs)]
    article = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": cfg["h1"],
        "datePublished": DATE, "dateModified": DATE,
        "author": {"@type": "Person", "name": "Daniel Hart",
                   "url": "https://bpaau.org/about#daniel-hart"},
        "publisher": {"@type": "Organization", "name": "Best Pokies Australia",
                      "logo": {"@type": "ImageObject",
                               "url": "https://bpaau.org/assets/logo.png",
                               "width": 192, "height": 192}},
        "mainEntityOfPage": url,
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in cfg["faqs"]]}
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "BPAAU",
         "url": "https://bpaau.org/", "inLanguage": "en-AU"},
        {"@context": "https://schema.org", "@type": "Organization", "name": "BPAAU",
         "alternateName": "Best Pokies Australia", "url": "https://bpaau.org/",
         "logo": "https://bpaau.org/assets/logo.png", "sameAs": ["https://bpaau.com"]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": breadcrumb},
        article, faq,
    ]
    scripts = "\n".join(
        '<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>"
        for x in ld)
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1, viewport-fit=cover" name="viewport"/>
<meta content="#0d1117" name="theme-color"/>
<title>{title}</title>
<meta content="{desc}" name="description"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>
<link href="{url}" rel="canonical"/>
<link href="/assets/favicon-32.png" rel="icon" type="image/png"/>
<link href="/assets/apple-touch-icon.png" rel="apple-touch-icon"/>
<link href="/site.webmanifest" rel="manifest"/>
<link href="/assets/theme.css?v=20261004" rel="stylesheet"/>
<meta content="BPAAU" property="og:site_name"/>
<meta content="{title}" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<meta content="article" property="og:type"/>
<meta content="{url}" property="og:url"/>
<meta content="{ogimg}" property="og:image"/>
<meta content="en_AU" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{desc}" name="twitter:description"/>
<meta content="{ogimg}" name="twitter:image"/>
{scripts}
</head>"""


def body_open(cfg):
    active = cfg.get("active", "/")
    navlinks = "\n".join(
        f'<a class="nav__link{" is-active" if href == active else ""}" href="{href}">{name}</a>'
        for href, name in NAV)
    crumbs = " &raquo; ".join(
        (f'<a href="{u}">{n}</a>' if u else f"<span>{n}</span>")
        for n, u in cfg["crumbs"])
    return f"""<body id="top">
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header">
<div class="container">
<div class="header-inner">
<a aria-label="BPAAU home" class="brand-logo" href="/">
<img alt="BPAAU &mdash; Best Pokies Australia" decoding="async" height="72" loading="eager" src="/assets/logo.png" width="240"/>
</a>
<input class="nav-toggle" hidden="" id="nav-toggle" type="checkbox"/>
<label aria-label="Toggle navigation" class="nav-toggle-label" for="nav-toggle">
<span></span><span></span><span></span>
</label>
<nav aria-label="Primary" class="nav">
{navlinks}
</nav>
<label aria-hidden="true" class="nav-backdrop" for="nav-toggle"></label>
</div>
</div>
</header>
<main id="main-content">
<div class="container">
<aside class="rg-banner" role="note">
<strong>18+ Only.</strong> Gambling is addictive. Gamble responsibly. Free 24/7 support:
        <a href="tel:1800858858">1800 858 858</a> &middot;
        <a href="https://www.gamblinghelponline.org.au" rel="noopener" target="_blank">gamblinghelponline.org.au</a> &middot;
        <a href="https://www.betstop.gov.au" rel="noopener" target="_blank">BetStop</a>
</aside>
<section class="page-hero">
<p class="breadcrumb">{crumbs}</p>
<figure class="page-banner"><img src="{cfg['banner']}" alt="{cfg['banner_alt']}" width="3138" height="1336" loading="eager" decoding="async" fetchpriority="high"/></figure>
<h1>{cfg['h1']}</h1>
<div class="author-box">
<span aria-hidden="true" class="author-box__avatar">DH</span>
<div>
<p class="author-box__name">Daniel Hart</p>
<p class="author-box__role">Senior Pokies Reviewer &amp; iGaming Editor</p>
<p class="author-box__meta">Reviewed by Sarah Chen &middot; Last updated {DATE_HUMAN} &middot; 18+</p>
</div>
</div>
<p class="lede">{cfg['lede']}</p>
<div class="mission-box"><p><strong>&#10148; Updated for 2026:</strong> {cfg['mission']} <a href="/methodology">See how we test</a>.</p></div>
</section>"""


def body_close(cfg):
    # visible FAQ
    faq_html = ""
    if cfg["faqs"]:
        items = "\n".join(
            f'<details class="faq"><summary>{q}</summary><div class="faq__body">{a}</div></details>'
            for q, a in cfg["faqs"])
        faq_html = f"""<section class="section">
<div class="section-title"><span class="section-title__label">FAQ</span><h2>{cfg.get('faq_title','Frequently Asked Questions')}</h2></div>
{items}
</section>"""
    cards = ""
    if cfg.get("related"):
        c = []
        for href, img, tag, h3, ex, meta in cfg["related"]:
            c.append(f"""<a class="blog-card" href="{href}">
<div class="card__media"><img alt="{h3}" decoding="async" height="784" loading="lazy" src="{img}" width="1168"/></div>
<div class="blog-card__body">
<span class="card__tag">{tag}</span>
<h3>{h3}</h3>
<p class="card__excerpt">{ex}</p>
<p class="blog-card__meta">{meta}</p>
</div>
</a>""")
        cards = f"""<section class="section">
<div class="section-title"><span class="section-title__label">Keep reading</span><h2>Related guides</h2></div>
<div class="blog-card-grid">
{chr(10).join(c)}
</div></section>"""
    footlinks = "\n".join(f'<a href="{h}">{n}</a>' for h, n in FOOTER)
    return f"""{faq_html}{cards}</div></main><footer class="site-footer">
<div class="container">
<nav aria-label="Footer" class="footer-nav">
{footlinks}
</nav>
<p class="footer-note">18+ only. BPAAU is an independent comparison site. All listed operators hold Gaming Curacao licences. Gamble responsibly.</p>
<p class="footer-note"><strong>Editorial Disclosure:</strong> bpaau.org is an independent information portal. Some outbound links are affiliate links &mdash; we may receive a commission. This never influences our rankings. Real-money online pokies are regulated under the Interactive Gambling Act 2001 (Cth).</p>
</div>
</footer>
<a class="back-to-top" href="#top" aria-label="Back to top">&#8593;</a>
<div class="mobile-cta"><a class="btn btn--primary btn--block" href="https://1xaud.com/register" rel="sponsored nofollow noopener" target="_blank">Claim Free $199 Bonus</a></div>
</body>
</html>
"""


def write_page(cfg, sections):
    html = head(cfg) + "\n" + body_open(cfg) + "\n" + "\n".join(sections) + "\n" + body_close(cfg)
    fp = os.path.join("public", cfg["slug"] + ".html")
    with io.open(fp, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    words = len(__import__("re").sub(r"<[^>]+>", " ", html).split())
    print(f"{cfg['slug']:55s} {words:5d} words  {len(html)//1024:4d}KB")
    return fp
