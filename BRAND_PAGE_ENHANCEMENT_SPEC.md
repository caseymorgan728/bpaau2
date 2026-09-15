# Brand Review Page Enhancement Spec (2026-09-15)

> Single source of truth for enhancing the 6 brand hub review pages in `public/`.
> Read this file + `PRODUCT_RESEARCH.md` + the existing HTML file before editing.

## 1. NON-NEGOTIABLE CONSTRAINTS

- **Only modify files in `C:\Users\User\Documents\GitHub\bpaau2\public\`**. Never touch the old `bpaau` repo.
- **Zero JavaScript** — only `<script type="application/ld+json">` allowed. No inline JS, no event handlers.
- **Zero popups, overlays, sticky elements, side banners.**
- **Zero external fonts** — system font stack only.
- **CSS**: `/assets/theme.css?v=20260915` only. No inline `<style>` blocks.
- **18+** and **Curacao** trust signals must appear in footer and body text.
- **6 protected products**: URLs, brand names, logo paths, and offer amounts are FIXED. See §3.
- **Bottom 6-product card grid must be preserved exactly** (all 6 brands with correct links/offers/logos).
- All affiliate register links: `rel="sponsored nofollow noopener" target="_blank"`.
- All internal links must point to files that actually exist in `public/`.

## 2. TARGET OUTPUT

- File size: **25–35 KB** per page (current ~17–19 KB).
- Visible word count in `<main>`: **≥2000 words**.
- SEO audit: **100/100** — every check in §7 must pass.

## 3. PROTECTED PRODUCT DATA (DO NOT CHANGE)

| Brand | Register URL | Logo path | Protected Offers |
|---|---|---|---|
| 1XAUD | https://1xaud.com/register | /logo%20app/logo%201.png (845×242) | Sign Up Free $199; Daily Deposit Bonus 120%; Welcome Bonus 100% |
| GD8 | https://gd8au.com/register | /logo%20app/logo%202.webp (350×215) | Rollover Rebate 1.18%; Grand Jackpot Bonus $2888; Welcome Bonus 100% |
| MR BLUEY | https://mrblueyau.com/register | /logo%20app/logo%203.png (789×318) | Daily Depositor Free $18; Weekly Winlose Rebate 10%; VIP Upgrade Bonus $2888 |
| TOY STORY 9 | https://toystory9au.com/register | /logo%20app/logo%204.png (500×263) | Lucky Wheel Bonus Up To $999; Monthly Welcome Bonus 50%; Grand Jackpot Bonus $2888 |
| GARCAT8 | https://garcat8.com/register | /logo%20app/logo%205.webp (1000×366) | Daily Easy Step Free $100; Garcat8 Jackpot Bonus $1888.88; Slot Welcome Bonus 100% |
| 1XACE | https://1xaceau.com/register | /logo%20app/logo%206.png (788×313) | Sign Up Free $177.77; No Rollover & Winover 120%; Premium Jackpot $1888 |

## 4. PAGE STRUCTURE (sections in order)

Keep existing `<head>`, `<header>`, hero, and `<footer>`. Enhance `<main>` with these sections:

### 4.1 Hero (keep, may tweak H1/lede for keywords)
- H1: brand + primary keyword + Australia angle, ≤70 chars visible.
- Lede: 1 line with key offer amounts.
- CTA button to register URL with correct rel.

### 4.2 Overview / At a Glance (expand existing)
- Intro paragraph (150–200 words): brand positioning, network context, what the review covers.
- Score table: 7–8 categories with scores and a 1-line reason per row. Overall 4.6–4.8/5.

### 4.3 Brand Story & Background (NEW)
- 200–300 words. Where the brand sits in the 6-site BPA network, target market (Australia), platform type, unique theme/positioning, when it launched (if known), what makes it distinct.
- Cite real facts from PRODUCT_RESEARCH.md (e.g., "1XAUD is the flagship with a built-in 6-site switcher and four backup domains").

### 4.4 Bonuses & Promotions — Full Terms (expand existing)
- For each protected offer: 2–3 sentences explaining what it is, who qualifies, min deposit (AUD 10 network standard), wagering mechanics (Turnover vs Rollover — explain both), expiry, game restrictions (pokies/slots only), no stacking rule.
- Link to every dedicated promo page for that brand (see §5).
- Mention VIP/loyalty tiers if applicable.

### 4.5 Popular Pokies Deep Dive (expand existing)
- 5–6 games, each with **2–3 sentences**: provider, theme, RTP if known, bonus features, why Australian players like it.
- Use real game names: Gates of Olympus, 5 Dragons, Feng Huang, 3 Super Ace, Fortune Gems 3, Angel & Devil, plus brand-specific games from research (e.g., 1XACE: Super Mahjong 2 97%, 5 Lions 96.68%, Crazy Buffalo 96.89%, Gods of Asgaro 97.23%; TOY STORY 9: JILI Caishen 96.18%, Wicked Fortune, Thunderstruck II).

### 4.6 Payment Methods & Withdrawal Speed (NEW section or expand)
- Comparison table: PayID vs USDT/Crypto vs Neosurf/Cards — min deposit, min withdrawal (AUD 50), speed, fees, KYC.
- Paragraph on PayID instant deposits, OSKO withdrawals, one-time KYC, crypto options.
- Link to /payid-cashouts-australia-2026.

### 4.7 Licence, Safety & Responsible Gambling (expand)
- Specific licence details from research (e.g., 1XACE: Curaçao Gaming Authority Licence No. OJK/2025/878/6868, Bridge Technologies B.V. No. 160689; GARCAT8: OJK/2025/878/6968, Bridge Technologies B.V. No. 168679).
- For brands where licence is unconfirmed (GD8, MR BLUEY): state "Curacao-licensed network operator" without fabricating a licence number.
- 18+, responsible gambling, deposit limits, BetStop mention.
- Link to /curacao-casino-licence-check-australia-2026.

### 4.8 Rating Breakdown (NEW)
- Table: Category | Score (out of 10) | Justification (1 sentence).
- Categories: Sign-up Bonus, Daily Promotions, Game Variety, Payment Speed, Licence & Trust, Mobile Experience, Customer Support, VIP/Loyalty.
- Overall: 4.6–4.8/5.

### 4.9 What Sets [Brand] Apart (NEW comparison)
- Intro paragraph.
- Comparison table: [Brand] vs other 5 — columns: Sign-up Free, Daily Bonus, Jackpot, Unique Feature, Best For.
- 2–3 paragraphs on unique selling points from research.

### 4.10 FAQ (expand from 5 to 8–10 items)
- Use `<details class="faq-item"><summary>Question</summary><p>Answer</p></details>`.
- Questions must cover: licensing, PayID, welcome bonus terms, wagering, withdrawal speed, min deposit, mobile play, game fairness, safety, how to sign up.
- Each answer 2–4 sentences.
- **Mirror exactly in JSON-LD FAQPage** (same Q&A pairs).

### 4.11 Editor Conclusion (NEW)
- 150–200 words: final verdict, who should join, top 3 pros, top 1–2 cons, final CTA.

### 4.12 All Six Operators Product Grid (PRESERVE EXACTLY)
- Keep the existing 6-card grid unchanged. This is the cross-selling module.

### 4.13 Related Guides & Reviews (expand existing)
- Link to: all 5 other brand review pages, all core guide pages, /blog.
- Use `<ul class="related-links">`.

## 5. INTERNAL LINK MAP

### Promo pages per brand (link to ALL that exist):
- **1XAUD**: /1xaud-188-free-credit-no-deposit-australia-2026, /1xaud-daily-bonus-25-percent-australia-2026, /1xaud-pokies-unlimited-rebate-12-percent-australia-2026, /1xaud-sign-up-free-chips-1888-australia-2026, /1xaud-weekend-bonus-35-percent-australia-2026
- **GD8**: /gd8-aussie-opal-vip-888-bonus-australia-2026
- **MR BLUEY**: /mrbluey-18-daily-free-credit-australia-2026
- **1XACE**: /1xace-17777-free-sign-up-no-rollover-australia-2026, /1xace-app-bonus-25-percent-australia-2026, /1xace-no-rollover-winover-50-percent-australia-2026, /1xace-premium-jackpot-1888-australia-2026, /1xace-usdt-crypto-bonus-10-percent-australia-2026
- **GARCAT8**: /garcat8-free-365-day-bonus-australia-2026, /garcat8-188888-jackpot-bonus-australia-2026, /garcat8-slot-welcome-bonus-100-percent-australia-2026
- **TOY STORY 9**: /toystory9-lucky-wheel-999-bonus-australia-2026

### Other brand review pages (cross-link all 5):
/gd8-review, /mrbluey-review, /1xace-review, /garcat8-review, /toystory9-review, /1xaud-review

### Core guide pages:
/no-deposit-free-bonus-guide-australia-2026
/payid-cashouts-australia-2026
/curacao-casino-licence-check-australia-2026
/best-high-rtp-pokies-australia-2026
/blog

## 6. KEYWORDS (natural integration, no stuffing)

Primary keyword per page = brand + review/bonus:
- 1XAUD: "1xaud review", "1xaud free credit"
- GD8: "gd8 bonus australia", "gd8 pokies"
- MR BLUEY: "mr bluey pokies", "mr bluey review"
- 1XACE: "1xace no rollover", "1xace review"
- GARCAT8: "garcat8 daily bonus", "garcat8 review"
- TOY STORY 9: "toystory9 lucky wheel", "toystory9 review"

Long-tail keywords to weave in (naturally, in H2/H3/body/alt):
australia pokies, online pokies real money, free credit no deposit, PayID pokies,
daily bonus pokies, no rollover bonus, fast withdrawal casino australia,
Curacao licensed casino, best pokies site, pokies free spins, high RTP pokies,
instant payout casino, AUD minimum deposit, no wagering bonus, aussie pokie sites

Marketing language allowed (exaggerated but truthful on amounts):
"Top 1 Trusted", "#1 首选", "free bonus no deposit", "daily free credit",
"biggest jackpot", "exclusive bonus", "verified by Curacao", "instant PayID cashout",
"limited time", "Australia's favourite", "most generous".

## 7. SEO AUDIT CHECKLIST (must pass 100%)

Run these checks on your file before reporting done:

1. **Title**: ≤60 characters, unique across the 6 pages, contains brand keyword.
2. **Meta description**: 139–160 characters, contains keyword + "18+".
3. **H1**: exactly one, contains primary keyword.
4. **Heading hierarchy**: no skips (h1→h2→h3, never h2→h4).
5. **Canonical**: `https://bpaau.org/<slug>` (no .html, trailing slash only for root).
6. **Robots**: `index,follow,max-image-preview:large`.
7. **JSON-LD** (all must be valid JSON — verify with `json.loads`):
   - WebSite
   - Organization
   - BreadcrumbList (Home → Reviews → Brand Review)
   - Review (ratingValue 4.6–4.8, author BPAAU, datePublished 2026-09-15)
   - Product + AggregateRating (ratingValue 4.6–4.8, ratingCount realistic 150–300)
   - FAQPage (matches visible FAQ items exactly)
   - Article (headline, datePublished, dateModified, author, publisher)
8. **Images**: every `<img>` has non-empty `alt`, `width`, `height`, and `loading="lazy"` (except hero logo which is `loading="eager"`).
9. **Internal links**: every `href="/..."` target exists as a file in `public/`.
10. **Affiliate links**: every link to 1xaud.com/gd8au.com/mrblueyau.com/1xaceau.com/garcat8.com/toystory9au.com has `rel="sponsored nofollow noopener"` and `target="_blank"`.
11. **No JS**: no `<script>` except JSON-LD, no `onclick`, no inline event handlers.
12. **No external fonts**: no Google Fonts links.
13. **18+**: appears in visible text.
14. **Curacao**: appears in visible text (body or footer).
15. **Word count**: ≥2000 visible words in `<main>` (strip tags, count whitespace-separated tokens).
16. **CSS**: only `/assets/theme.css?v=20260915`.
17. **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>` used appropriately.
18. **Mobile FAQ**: `<details>` elements work without JS.

## 8. REAL FACTS FROM PRODUCT_RESEARCH.md (use these, don't fabricate)

### Network-wide facts (applicable to all 6):
- All 6 are sister sites on the same white-label platform.
- Min deposit: AUD 10. Min withdrawal: AUD 50.
- Registration: name + +61 mobile + password + SMS OTP, bank-name match required.
- Wagering: Turnover system (balance × multiplier) and Rollover system (total wagers). No bonus stacking. Free credits valid on pokies/slots only.
- Withdrawals via OSKO, Visa, Crypto with one-time KYC.
- Payments: PayID/Osko, Visa, Mastercard, Apple Pay, Google Pay, BTC, ETH, USDT.
- 18+ only.

### Brand-specific facts (cite in the relevant page):
- **1XAUD**: Flagship brand. Built-in 6-site "Switch To" widget. ~100 game providers (JILI, Pragmatic Play, Microgaming, Aristocrat, Yggdrasil, Spadegaming, Evolution, SA Gaming, Allbet, SBOBET). Four Telegram channels/bots, Facebook, WhatsApp, Linktree. Backup domains .net/.org/.vip. Mini-games: Lucky Wheel, Mystery Box, Plinko, Daily Mission. Live RTP "Game Tips" page and leaderboard. Footer says PAGCOR. Cloudflare-protected SPA on Bunny CDN.
- **GD8**: "Low Pending Rate" tagline. Sister site called out by Toy Story 9 as offering "exclusive Aussie pokies with fast payouts and VIP rewards." Deep-linked from 1XAUD switcher. Site was not directly fetchable during research — mark specific figures as per bpaau.org listing.
- **MR BLUEY**: Bluey-cartoon themed (Australian-made cartoon = local hook). Game categories: SLOT 1:1, SLOT 1:100, EVENT GAME, LIVE GAME, OTHER GAME, BONZA SCRATCHIER. Providers: BNG, JILI, MEGAH5, IMPERIUM. Live transaction feed shows AUD deposits/withdrawals. 100% welcome bonus (meta description). ScamAdviser trust score 75.
- **1XACE**: Most game-rich catalogue. RTP-tagged games: Jin Qian Wa/Pussy888 96.82%, Lucky Ox/888King 96.43%, Super Mahjong 2/JILI 97.00%, 5 Lions/Pragmatic Play 96.68%, Caishen Mega Fortune/Live22 97.05%, DJ Boom Boom/FaChai 96.00%, Fortune Meow/Rich Gaming 96.10%, Crazy Buffalo/Apollo 96.89%, Lantern of Luck/WF Gaming 96.38%, Gods of Asgaro/888King 97.23%. Live dealer: Sexy Baccarat (C02/C03/C06/C08), SA Gaming Deluxe Blackjack, Pragmatic Play Speed Baccarat 12/Mega Roulette/Baccarat 2. Crash games: Aviatrix, Spribe Dice/Goal/Mines/Mini Roulette. Curaçao Gaming Authority Licence No. OJK/2025/878/6868, operated by Bridge Technologies B.V. (No. 160689). BPA/Anjouan "Exclusive Member Channel" badge. iOS PWA + Google Play app.
- **GARCAT8**: Blue-and-gold navy theme. Categories: SLOT, CRASH, FAST. Curaçao Gaming Authority Licence No. OJK/2025/878/6968, operated by Bridge Technologies B.V. (No. 168679). PAGCOR logo displayed. Payments: PayID, Visa, Mastercard, Apple Pay, Google Pay, e-wallet, BTC, ETH, USDT, FPX. Support: Facebook, WhatsApp, Telegram. Certifications: iovation, bmm, iTech Labs, TST Verified, GoDaddy, LGMS, ThreatMetrix.
- **TOY STORY 9**: Toy Story (Disney/Pixar) character theme. Active promos: BPA Monthly Competition, ToyStory9 × BNG "Deposit AUD50 → 30 Free Spins". Promo tiles: Sign Up Free $199, Daily Up Bonus 120%, Rollover Rebate 1.10%, Weekly Rebate 9%, VIP Upgrade Bonus $2888, Daily Depositor Free AUD 18. Landing-page banners: Free Chips AUD 19.99, 365 Daily Free Chips, Social Share Free AUD 9.99, Pokies Unlimited Bonus 9%, Daily Deposit Bonus 30%/40% (no turnover). Providers: JILI, Aristocrat, Microgaming, BNG, Playson, V Power, Acewin, Slot Mania. Featured RTP: JILI Caishen 96.18%, FlyOut 93.29%, Iceland StandAlone 96.88%. Banks: Westpac, NAB, Virgin Money. PAGCOR + Gaming Curacao logos. 24/7 live chat.

## 9. WORKFLOW

1. Read the existing HTML file fully.
2. Read this spec + relevant brand section of PRODUCT_RESEARCH.md.
3. Edit the file in place (overwrite `public/<brand>-review.html`).
4. Self-audit using the checklist in §7. Fix any failures.
5. Report: file path, final size, word count, what new sections were added, any audit items that need attention.

## 10. WHAT NOT TO DO

- Do NOT change any protected offer amount, URL, logo path, or brand name.
- Do NOT add JavaScript, popups, external fonts, or inline CSS.
- Do NOT fabricate licence numbers — use only what's in §8 or say "Curacao-licensed network."
- Do NOT delete or modify the 6-card product grid at the bottom.
- Do NOT link to internal pages that don't exist in `public/`.
- Do NOT use the same title or meta description across two pages.
- Do NOT keyword-stuff — write naturally for Australian pokie players.
