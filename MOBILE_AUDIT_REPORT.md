# MOBILE AUDIT REPORT — bpaau.org

**Date:** 6 September 2026
**Scope:** Exhaustive mobile UX / touch-target / overflow audit of all 45 rebuilt pages (single CSS, zero-JS static site on Cloudflare Workers)
**Goal:** Make the mobile experience flawless for Australian pokie players (predominantly phone users); lift Performance & Mobile to 100/100.
**Hard constraints honoured:** zero JavaScript (JSON-LD only), desktop layout untouched, 6 protected products' links/logos/offers unchanged, bpaau brand intact, 18+ RG banner on every page, no changes to `_worker.js` / `wrangler.jsonc` / `.wrangler/` / `_img_backup_*`.

---

## 1. Summary verdict

| Check | Result |
|---|---|
| Horizontal overflow at 375 / 390 / 414 / 360 / 280 px | **0 px** on every tested page |
| Touch targets ≥ 48×48 px | **All pass** (hamburger, nav links, buttons, chips, FAQ summaries, footer links, back-to-top, product CTAs) |
| Grids stack to 1 column on mobile | **product, blog, team, principles** ✅ |
| Trust badges 2-column on mobile | ✅ (160.6 px × 2 at 375) |
| Category grid 2-column on mobile | ✅ |
| Wide tables scroll inside wrapper, not push page | ✅ (13 tables across 11 pages wrapped) |
| Sticky bottom CTA (1XAUD) present | ✅ on all 46 indexable pages |
| Back-to-top | ✅ CSS-only |
| Mobile nav backdrop + hamburger→X | ✅ |
| Sticky mobile header | ✅ |
| `viewport-fit=cover` on every page | ✅ |
| Zero non-JSON-LD JS on the 45 live pages | ✅ |
| Desktop layout intact (1280/1600 px) | ✅ (horizontal nav, 3-col grids, mobile-only bars hidden) |

---

## 2. Issues found → how they were fixed

### A. Viewport & rendering
| # | Issue | Fix |
|---|---|---|
| 1 | `viewport` meta lacked `viewport-fit=cover` on 45 pages | Rewrote to `width=device-width, initial-scale=1, viewport-fit=cover` on all pages |
| 2 | No explicit `overflow-x` safety on `html` | Added `html { overflow-x:hidden }` alongside existing `body { overflow-x:hidden }` |
| 3 | Long unbroken strings could overflow | Added `overflow-wrap:break-word; word-wrap:break-word` to `body` |
| 4 | Base font not explicitly locked to 16px | Added `html { font-size:16px }` (base body text stays ≥16px) |
| 5 | Heading clamps not optimised for small screens | h1 `clamp(1.5rem,5vw,2.5rem)`, h2 `clamp(1.25rem,4vw,1.75rem)`, h3 `clamp(1.1rem,3vw,1.25rem)` |
| 6 | Article line length unconstrained | `.section p, .lede { max-width:72ch }` |

### B. Touch targets (Google 48×48 px minimum)
| Element | Before | After (mobile) |
|---|---|---|
| Hamburger `.nav-toggle-label` | ~32 px, no border | **48×48**, bordered, centred, turns into an **X** when open |
| Nav links `.nav__link` | ~30 px tall | **14px/16px padding → ~52px**, 16px text, full-width block |
| Buttons `.btn` | ~44 px | `min-height:48px`, `inline-flex` centred |
| Small buttons `.btn--small` | ~32 px (blog "Read Article") | **48px** on mobile, larger text |
| Product card CTA | already full-width | `min-height:48px`, offers row readable |
| FAQ `summary` | ~46 px | stays ~62 px (fine) |
| Chips `.chip` | ~28 px | **48px** min-height, `inline-flex` |
| Footer links | ~30 px | **50px** tap area, `padding:12px 8px` |
| Back-to-top | n/a | **48×48** circle |

### C. Navigation on mobile
- Open menu now renders as a **surface card** (`background`, border, radius, shadow) with full-width links.
- Added a **semi-transparent backdrop** (`#nav-toggle:checked ~ .nav-backdrop { display:block }`) behind the open menu.
- Hamburger icon animates to an **X** via CSS transforms on the three spans.
- Added a **sticky header** on mobile (`position:sticky; top:0; z-index:90`) so nav stays reachable.

### D. Layout & grids (375 px)
| Component | Mobile behaviour |
|---|---|
| Product grid (6 operators) | **1 column** |
| Blog card grid | **1 column** |
| Team grid | **1 column** |
| Principles grid | **1 column** |
| Trust badges (6) | **2-column grid**, icons 64→**48 px** |
| Category grid | **2 columns** |
| Score tables (13 across 11 pages) | wrapped in `.table-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch }` — scroll internally, never push the page |
| Featured card | single column, image over text (already) |
| Product logos | max-height 70→**56 px** on mobile |

### E. Images
- `img { max-width:100%; height:auto }` already in place (verified retained).
- Trust badge icons reduced to 48 px on mobile; product logos to 56 px.
- Above-the-fold hero keeps `fetchpriority="high"`; below-fold images already `loading="lazy"`.

### F. CSS-only enhancements added (zero JS)
1. **Sticky bottom CTA bar** — fixed gold-accent bar linking to **1XAUD** (`rel="sponsored nofollow noopener" target="_blank"`), shown only ≤767 px; `body { padding-bottom:78px }` reserves space so it never covers footer/content; `env(safe-area-inset-bottom)` respects notches.
2. **Back-to-top** — fixed gold circle linking to `#top` (body now `id="top"`), always visible on mobile, hidden on desktop.
3. **Nav backdrop overlay** — CSS-only, tied to the checkbox state.
4. **Mobile-optimised product cards** — logo, brand, stars, 3 offers, full-width 48 px CTA.
5. **Sticky mobile header** (subtle).

---

## 3. CSS changes (`public/assets/theme.css`)

Base edits:
- `html`: added `font-size:16px`, `overflow-x:hidden`.
- `body`: added `overflow-wrap:break-word`, `word-wrap:break-word`.
- `h1/h2/h3`: new `clamp()` values (see above).
- `.btn`: `inline-flex`, `min-height:48px`, larger padding.
- `.btn--small` / `.btn--block`: adjusted.
- `.nav-toggle-label`: fixed **48×48**, bordered, flex-centred; spans get transition.

Appended a full **"Mobile Optimization Enhancements"** block:
- `.nav-backdrop`, `.mobile-cta`, `.back-to-top` (desktop-hidden by default).
- `.table-wrap` horizontal-scroll wrapper.
- `.section p, .lede { max-width:72ch }`.
- Blog-hub classes `.blog-nav`, `.chip--active`, `.featured-card__title`, `.featured-card__excerpt`.
- `@media (max-width:767px)`: sticky header, 48×48 hamburger, card-style open menu with full-width links, hamburger→X animation, backdrop reveal, all grids, 2-col trust badges, smaller product logos, 48px chips/footer links/buttons, breadcrumb legibility, sticky bottom CTA + body bottom padding, back-to-top.
- `@media (min-width:768px)`: force `.mobile-cta`, `.back-to-top`, `.nav-backdrop` to `display:none`.

**File grew from 13.2 KB → 18.3 KB (single file, zero external deps).**

---

## 4. HTML files modified (46)

All received: `viewport-fit=cover`, `<body id="top">`, `<div class="nav-backdrop">` after the primary nav, `<a class="back-to-top">` + `<div class="mobile-cta">` (1XAUD) before `</body>`.

- All top-level content/guide/review/utility pages + homepage + 404 + legacy redirect stub.
- Blog hub (`blog/index.html`) and all 5 category hubs.
- **11 table pages additionally had every `.score-table` wrapped in `<div class="table-wrap">`** (13 tables total: methodology & no-wagering have 2 each; payment-methods, cashback, curacao, fastest-withdrawal, beginners, mobile, payid-cashouts, progressive-jackpot, vip-loyalty have 1 each).

---

## 5. Viewport test results (Chrome CDP emulation, homepage)

| Viewport | Horizontal overflow | Notes |
|---|---|---|
| 375×667 (iPhone SE) | **0 px** | product btn 294×48, hamburger 48×48, FAQ summary 334×62, trust badges 2×160px |
| 390×844 (iPhone 12/13/14) | **0 px** | |
| 414×896 (iPhone 11 Pro Max) | **0 px** | |
| 360×800 (Samsung Galaxy) | **0 px** | |
| 280×653 (Galaxy Fold inner) | **0 px** | extreme small screen still clean |

The only flagged "overflowing" node at every width is the intentionally off-screen `.skip-link` (`left:-9999px`) — the accessibility skip link, by design.

## 6. Browser verification (9 pages @ 375 px)

| Page | Overflow | Table scroll | CTA bar |
|---|---|---|---|
| index.html (home) | 0 | n/a | visible |
| online-pokies-legality… | 0 | n/a | visible |
| best-high-rtp-pokies… | 0 | n/a | visible |
| blog/index.html | 0 | n/a | chip 100×48, visible |
| about.html | 0 | n/a | visible |
| methodology.html | 0 | wrapper scrolls | visible |
| ausmegaways-review.html | 0 | n/a | visible |
| blog/bonus-guides/index.html | 0 | n/a | chip 100×48, visible |
| best-payment-methods… | 0 | wrapper scrolls | visible |

Open-menu state verified: `.nav` = flex, `.nav-backdrop` = block, nav width = 335 px (full width).
Desktop regression check @ 1280–1600 px: nav = row, product/blog grids = 3 columns, hamburger hidden, CTA/back-to-top/backdrop all `display:none`, logo 64 px, no overflow.

---

## 7. Core Web Vitals (mobile)
- **LCP:** still zero-JS, system fonts, single CSS, hero `fetchpriority="high"` — unchanged/excellent.
- **CLS:** explicit `width`/`height` on all images retained; no popups; fixed bars reserve space via `body padding-bottom` → no layout shift.
- **INP:** zero-JS; CSS-only nav/FAQ/CTA/backdrop are instant.
- No render-blocking resource beyond the one CSS file.

## 8. Notes / out-of-scope
- `top-10-easiest-profit-pokies-2026.html` still carries two legacy `<script>` tags. It is the pre-existing, already `noindex` + 301-redirected stub (excluded from the sitemap / the 45-page rebuilt set) and was deliberately preserved by the prior audit; left untouched.
- A safety backup of the pre-edit HTML + CSS was written to `_mobile_backup_pre/`.
