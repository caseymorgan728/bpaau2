# BPAAU Template Specification (2026 Rebuild)

> **For all agents rebuilding remaining pages.** This spec is the single source of truth for the new SEO-first, performance-first design system. Copy the `public/index.html` skeleton, swap the page-specific `<title>`, meta, canonical, breadcrumb JSON-LD and `<main>` content. **Do not add JavaScript, popups, side banners, external fonts, or inline `<style>` blocks.**

---

## 1. Hard constraints (non-negotiable)

- **6 protected products** must always keep exact affiliate links, logos and offers (see §6). Product links use `rel="sponsored nofollow noopener" target="_blank"`.
- **bpaau.org brand** stays. Static HTML + Cloudflare Workers only — no build framework.
- **Zero JavaScript** on every page. The only `<script>` tags allowed are JSON-LD (`type="application/ld+json"`). FAQ = native `<details>`/`<summary>`. Mobile nav = CSS checkbox hack (no JS).
- **Zero popups, overlays, side banners, sticky elements.** No `#fk-popout-overlay`, no `#promo-side-banner`, no sticky header.
- **Zero external fonts.** Use the system font stack defined in `:root`. Never add `<link rel="preconnect">` to fonts.googleapis.com or fonts.gstatic.com.
- **18+ responsible gambling** banner appears on every page (use the `.rg-banner` snippet in §4).
- **Curacao licence** trust signal throughout.
- Keep existing images in `assets/badges/`, `assets/hero/`, `assets/categories/`, `assets/sections/`, `logo app/`, `banners home/`, `blog banner/`.
- Do **not** delete `_img_backup_*`, `.wrangler/`, `.gitignore`, `DumpStack.log`. Do **not** modify `_worker.js` or `wrangler.jsonc`.

---

## 2. Files you build on

| File | Purpose |
|---|---|
| `public/assets/theme.css` | The complete design system. Single file, no imports. Use every class from §5. Do not inline page-specific CSS into `<style>` blocks — add new classes here only if unavoidable. |
| `public/index.html` | Reference implementation. Copy its `<head>`, `<header>`, RG banner and `<footer>` verbatim into every page; change only the page-specific bits. |
| `TEMPLATE_SPEC.md` | This document. |

---

## 3. Master template (copy this skeleton)

```html
<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0d1117">
  <title>PAGE TITLE | BPAAU</title>
  <meta name="description" content="139–160 char unique description with keyword + 18+ note.">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="https://bpaau.org/SLUG">
  <link rel="icon" type="image/png" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/theme.css">

  <meta property="og:site_name" content="BPAAU">
  <meta property="og:title" content="PAGE TITLE">
  <meta property="og:description" content="Same as meta description.">
  <meta property="og:type" content="website">           <!-- use "article" for blog posts -->
  <meta property="og:url" content="https://bpaau.org/SLUG">
  <meta property="og:image" content="https://bpaau.org/assets/hero/main-hero.webp">
  <meta property="og:locale" content="en_AU">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="PAGE TITLE">
  <meta name="twitter:description" content="Same as meta description.">
  <meta name="twitter:image" content="https://bpaau.org/assets/hero/main-hero.webp">

  <!-- JSON-LD: WebSite + Organization + BreadcrumbList on EVERY page; add Article/FAQPage where relevant -->
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"BPAAU","url":"https://bpaau.org/","inLanguage":"en-AU"}</script>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"BPAAU","alternateName":"Best Pokies Australia","url":"https://bpaau.org/","logo":"https://bpaau.org/assets/logo.png","sameAs":["https://bpaau.com"]}</script>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://bpaau.org/"},{"@type":"ListItem","position":2,"name":"Category","item":"https://bpaau.org/blog/CATEGORY"},{"@type":"ListItem","position":3,"name":"Page Title","item":"https://bpaau.org/SLUG"}]}</script>
</head>
<body>
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
  </header>

  <main id="main-content">
    <div class="container">
      <aside class="rg-banner" role="note">
        <strong>18+ Only.</strong> Gambling is addictive. Gamble responsibly. Free 24/7 support:
        <a href="tel:1800858858">1800 858 858</a> ·
        <a href="https://www.gamblinghelponline.org.au" target="_blank" rel="noopener">gamblinghelponline.org.au</a> ·
        <a href="https://www.betstop.gov.au" target="_blank" rel="noopener">BetStop</a>
      </aside>

      <!-- ========== PAGE-SPECIFIC CONTENT HERE ========== -->

    </div>
  </main>

  <footer class="site-footer">
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
</html>
```

> **Important:** the `<input id="nav-toggle">`, `<label>` and `<nav class="nav">` must be siblings inside `.header-inner`, in that exact order, so the CSS selector `#nav-toggle:checked ~ .nav` works. Do not wrap them in extra divs.

---

## 4. Page anatomy (what goes in `<main>`)

Every content page uses these building blocks in order:

1. **`.page-hero`** — `<h1>` (exactly one per page), `.breadcrumb`, `.author-box`, `.lede`.
   - Breadcrumb uses `»` text separators and muted color.
   - Author box: `<span class="author-box__avatar">DH</span>` + name/role/meta.
2. **`.section`** blocks. Each starts with `.section-title` (small uppercase `.section-title__label` + `<h2>`).
3. **Content** — paragraphs, `<ul>`/`<ol>`, `.callout`, `.mission-box`, `.score-table`, `.method-steps`, `.principles-grid` as needed.
4. **Product grid** (transactional pages) — `.product-grid` with 6 `.product-card`s (see §6).
5. **FAQ** — native `<details class="faq">` blocks (see §5.14).
6. CTA row — `.cta-row` with `.btn.btn--primary` links.

---

## 5. CSS class reference (all defined in `assets/theme.css`)

### Layout & base
- `.container` — max-width 1100px, centered, 20px side padding.
- `.skip-link` / `.skip-link:focus` — accessibility skip-to-content.
- `.text-center`, `.mt-0` — utilities.

### Header / nav
- `.site-header`, `.header-inner`, `.brand-logo`, `.brand-logo img`
- `.nav-toggle` (checkbox, hidden), `.nav-toggle-label` (hamburger, hidden ≥768px), `.nav`, `.nav__link`
- Active link: add `.is-active` to the current page's `.nav__link`.

### Trust / RG
- `.rg-banner` — green responsible-gambling notice (use verbatim).
- `.trust-badges`, `.trust-badge`, `.trust-badge img`, `.trust-badge p`

### Hero / article
- `.page-hero`, `.breadcrumb`, `.author-box`, `.author-box__avatar`, `.author-box__name`, `.author-box__role`, `.author-box__meta`, `.lede`
- `.hero-banner` — full-width rounded image.

### Sections
- `.section`, `.section-title`, `.section-title__label`

### Cards
- `.card`, `.card__media`, `.card__tag`, `.card__title`, `.card__excerpt`
- `.blog-card`, `.blog-card__body`, `.blog-card__meta`
- `.featured-card`, `.featured-card__media`, `.featured-card__body`
- `.category-grid`, `.category-card`
- `.team-grid`, `.team-card`, `.team-card__head`, `.team-avatar`
- `.principles-grid`, `.principle-card`

### Buttons
- `.btn`, `.btn--primary` (gold), `.btn--small`, `.btn--block`, `.cta-row`

### Products
- `.product-grid`, `.product-card`, `.product-card__logo`, `.product-card__logo img`, `.product-card__brand`, `.product-card__stars`, `.product-card__offers`, `.product-card__offers li`

### Tables
- `.score-table`, `.score-table th`, `.score-table td`

### FAQ (zero-JS accordion)
```html
<details class="faq">
  <summary>Question text?</summary>
  <div class="faq__body"><p>Answer text.</p></div>
</details>
```

### Callouts / boxes
- `.callout`, `.callout--green`, `.mission-box`
- `.chip`, `.chip:hover`
- `.method-steps`, `.method-steps li`, `.method-steps li::before` (auto-numbered)

### Footer
- `.site-footer`, `.footer-nav`, `.footer-nav a`, `.footer-note`

---

## 6. The 6 protected products (use EXACT data)

Use this `.product-grid` markup on every transactional/comparison page. Do not change logos, offers or links.

```html
<div class="product-grid">
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%201.png" alt="1XAUD logo" width="845" height="242" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">1XAUD</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Sign Up Free $199</li>
      <li>Daily Deposit Bonus 120%</li>
      <li>Welcome Bonus 100%</li>
    </ul>
    <a class="btn btn--primary" href="https://1xaud.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
  <!-- GD8 -->
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%202.webp" alt="GD8 logo" width="350" height="215" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">GD8</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Rollover Rebate 1.18%</li>
      <li>Grand Jackpot Bonus $2888</li>
      <li>Welcome Bonus 100%</li>
    </ul>
    <a class="btn btn--primary" href="https://gd8au.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
  <!-- MR BLUEY -->
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%203.png" alt="MR BLUEY logo" width="789" height="318" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">MR BLUEY</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Daily Depositor Free $18</li>
      <li>Weekly Winlose Rebate 10%</li>
      <li>VIP Upgrade Bonus $2888</li>
    </ul>
    <a class="btn btn--primary" href="https://mrblueyau.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
  <!-- TOY STORY 9 -->
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%204.png" alt="TOY STORY 9 logo" width="500" height="263" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">TOY STORY 9</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Lucky Wheel Bonus Up To $999</li>
      <li>Monthly Welcome Bonus 50%</li>
      <li>Grand Jackpot Bonus $2888</li>
    </ul>
    <a class="btn btn--primary" href="https://toystory9au.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
  <!-- GARCAT8 -->
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%205.webp" alt="GARCAT8 logo" width="1000" height="366" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">GARCAT8</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Daily Easy Step Free $100</li>
      <li>Garcat8 Jackpot Bonus $1888.88</li>
      <li>Slot Welcome Bonus 100%</li>
    </ul>
    <a class="btn btn--primary" href="https://garcat8.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
  <!-- 1XACE -->
  <article class="product-card">
    <div class="product-card__logo"><img src="/logo%20app/logo%206.png" alt="1XACE logo" width="788" height="313" loading="lazy" decoding="async"></div>
    <p class="product-card__brand">1XACE</p>
    <div class="product-card__stars" role="img" aria-label="Rated 5 out of 5">★★★★★</div>
    <ul class="product-card__offers">
      <li>Sign Up Free $177.77</li>
      <li>No Rollover &amp; Winover 120%</li>
      <li>Premium Jackpot $1888</li>
    </ul>
    <a class="btn btn--primary" href="https://1xaceau.com/register" target="_blank" rel="sponsored nofollow noopener">Claim Bonus</a>
  </article>
</div>
```

---

## 7. Color tokens (defined in `:root` of theme.css)

| Token | Value | Use |
|---|---|---|
| `--bg` | `#0d1117` | Page background |
| `--surface` | `#161b22` | Cards / sections |
| `--surface-2` | `#1c2230` | Offer list rows, inner boxes |
| `--border` | `#30363d` | Borders |
| `--text` | `#e6edf3` | Primary text |
| `--muted` | `#8b949e` | Secondary text |
| `--gold` | `#d4af37` | Primary CTA, links, highlights |
| `--gold-hover` | `#e6c44a` | Gold hover |
| `--green` | `#3fb950` | "verified", 18+ badges, RG banner |

---

## 8. Responsive behavior (already handled by CSS)

- **< 768px (mobile):** hamburger nav (checkbox), single-column cards, product grid 1–2 per row.
- **768–1023px (tablet):** horizontal nav, featured-card becomes 2-column.
- **≥ 1024px (desktop):** full nav, product/blog grids auto-fit 3+ per row.

Product and blog grids use `repeat(auto-fit, minmax(..., 1fr))` — you do **not** need per-page media queries.

---

## 9. SEO checklist for every new/rebuilt page

- [ ] One `<h1>` only; H2/H3 hierarchy follows.
- Title ≤ 60 chars; meta description 139–160 chars; keyword-first.
- Self-referencing `<link rel="canonical">` (clean URL, no `.html`).
- JSON-LD: WebSite + Organization + BreadcrumbList on every page; add `Article` for blog posts and `FAQPage` when a `<details class="faq">` block is present.
- Every `<img>` has descriptive `alt`, explicit `width`/`height`, `loading="lazy"` (except above-the-fold hero which uses `loading="eager"` and/or `fetchpriority="high"`), `decoding="async"`.
- `og:image` / `twitter:image` point to a file that actually exists under `/assets/`.
- Internal links use clean URLs (no `.html` extension).
- Affiliate links carry `rel="sponsored nofollow noopener" target="_blank"`.
- 18+ RG banner present.
- No `<script>` other than JSON-LD. No inline `<style>`. No Google Fonts.

---

## 10. Image asset quick reference

- Logo: `/assets/logo.png` (use `width="240" height="72"` in header).
- Favicon: `/assets/favicon-32.png`, `/assets/favicon.png`. Apple touch: `/assets/apple-touch-icon.png`.
- Trust badges (WebP): `/assets/badges/{curacao-licensed,responsible-18plus,payid-fast-payout,top1-trusted,audited-reviews,secure-encrypted}.webp`.
- Hero images (WebP): `/assets/hero/{main-hero,free-bonus-no-deposit,payid-fast-withdrawals,curacao-verified}.webp`.
- Category thumbnails (WebP): `/assets/categories/{winning-tips,top-pokies,promo-guides,fast-cashouts,bonus-guides}.webp`.
- Product logos: `/logo%20app/logo%201.png` … `logo%20app/logo%206.png` (note the URL-encoded spaces).

---

*End of spec. When in doubt, copy `public/index.html` and replace the page-specific region between the RG banner and the footer.*
