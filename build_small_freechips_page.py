# -*- coding: utf-8 -*-
"""Build the small-amount free chip ($10/$20/$25/$30) no-deposit AU pillar."""
import os, json

PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"

def _j(s):
    return json.dumps(s, ensure_ascii=False)

def head(slug, title, desc, breadcrumb, faq, date_pub="2026-09-23", date_mod="2026-09-23"):
    faq_json = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_j(q), _j(a)) for q, a in faq)
    crumbs = ",".join(
        '{"@type":"ListItem","position":%d,"name":%s,"item":%s}'
        % (i + 1, _j(n), _j(u)) for i, (n, u) in enumerate(breadcrumb))
    return '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1, viewport-fit=cover" name="viewport"/>
<meta content="#0d1117" name="theme-color"/>
<title>%s</title>
<meta content="%s" name="description"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>
<link href="https://bpaau.org/%s" rel="canonical"/>
<link href="/assets/favicon-32.png" rel="icon" type="image/png"/>
<link href="/assets/apple-touch-icon.png" rel="apple-touch-icon"/>
<link href="/site.webmanifest" rel="manifest"/>
<link href="/assets/theme.css?v=20260921" rel="stylesheet"/>
<meta content="BPAAU" property="og:site_name"/>
<meta content="%s" property="og:title"/>
<meta content="%s" property="og:description"/>
<meta content="article" property="og:type"/>
<meta content="https://bpaau.org/%s" property="og:url"/>
<meta content="https://bpaau.org/assets/hero/main-hero.webp" property="og:image"/>
<meta content="en_AU" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="%s" name="twitter:title"/>
<meta content="%s" name="twitter:description"/>
<meta content="https://bpaau.org/assets/hero/main-hero.webp" name="twitter:image"/>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"BPAAU","url":"https://bpaau.org/","inLanguage":"en-AU"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"BPAAU","alternateName":"Best Pokies Australia","url":"https://bpaau.org/","logo":"https://bpaau.org/assets/logo.png","sameAs":["https://bpaau.com"]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":%s,"datePublished":"%s","dateModified":"%s","author":{"@type":"Person","name":"Daniel Hart","url":"https://bpaau.org/about#daniel-hart"},"publisher":{"@type":"Organization","name":"Best Pokies Australia","logo":{"@type":"ImageObject","url":"https://bpaau.org/assets/logo.png","width":192,"height":192}},"mainEntityOfPage":"https://bpaau.org/%s"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>
</head>
''' % (title, desc, slug, title, desc, slug, title, desc, crumbs, _j(title), date_pub, date_mod, slug, faq_json)

RG_BANNER = '''<body id="top">
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header">
<div class="container">
<div class="header-inner">
<a aria-label="BPAAU home" class="brand-logo" href="/">
<img alt="BPAAU — Best Pokies Australia" decoding="async" height="72" loading="eager" src="/assets/logo.png" width="240"/>
</a>
<input class="nav-toggle" hidden="" id="nav-toggle" type="checkbox"/>
<label aria-label="Toggle navigation" class="nav-toggle-label" for="nav-toggle">
<span></span><span></span><span></span>
</label>
<nav aria-label="Primary" class="nav">
<a class="nav__link" href="/">Home</a>
<a class="nav__link" href="/best-high-rtp-pokies-australia-2026">Best Pokies</a>
<a class="nav__link is-active" href="/no-deposit-free-bonus-guide-australia-2026">Free Bonus</a>
<a class="nav__link" href="/payid-cashouts-australia-2026">Fast Payouts</a>
<a class="nav__link" href="/curacao-casino-licence-check-australia-2026">Curacao Verified</a>
<a class="nav__link" href="/blog">Blog</a>
<a class="nav__link" href="/about">About</a>
</nav>
<label aria-hidden="true" class="nav-backdrop" for="nav-toggle"></label>
</div>
</div>
</header>
<main id="main-content">
<div class="container">
<aside class="rg-banner" role="note">
<strong>18+ Only.</strong> Gambling is addictive. Gamble responsibly. Free 24/7 support:
        <a href="tel:1800858858">1800 858 858</a> ·
        <a href="https://www.gamblinghelponline.org.au" rel="noopener" target="_blank">gamblinghelponline.org.au</a> ·
        <a href="https://www.betstop.gov.au" rel="noopener" target="_blank">BetStop</a>
</aside>
'''

FOOTER = '''<footer class="site-footer">
<div class="container">
<nav aria-label="Footer" class="footer-nav">
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
<a class="back-to-top" href="#top" aria-label="Back to top">&#8593;</a>
<div class="mobile-cta"><a class="btn btn--primary btn--block" href="https://1xaud.com/register" rel="sponsored nofollow noopener" target="_blank">Claim Free $199 Bonus</a></div>
</body>
</html>
'''

def faq_section(faq):
    out = ['<section class="section">',
           '<div class="section-title"><span class="section-title__label">FAQ</span><h2>Small Free Chips: Frequently Asked Questions</h2></div>']
    for q, a in faq:
        out.append('<details class="faq"><summary>%s</summary><div class="faq__body">%s</div></details>' % (q, a))
    out.append('</section>')
    return "\n".join(out)

def related(cards):
    out = ['<section class="section">',
           '<div class="section-title"><span class="section-title__label">Keep reading</span><h2>Related guides</h2></div>',
           '<div class="blog-card-grid">']
    for href, tag, title, excerpt, img, w, h, date, mins in cards:
        out.append('''<a class="blog-card" href="%s">
<div class="card__media"><img alt="%s" decoding="async" height="%s" loading="lazy" src="%s" width="%s"/></div>
<div class="blog-card__body">
<span class="card__tag">%s</span>
<h3>%s</h3>
<p class="card__excerpt">%s</p>
<p class="blog-card__meta">%s · %s min read · Read the guide &rarr;</p>
</div>
</a>''' % (href, title, h, img, w, tag, title, excerpt, date, mins))
    out.append('</div></section></div></main>')
    return "\n".join(out)

def hero(breadcrumb_html, h1, lede, mission):
    return '''<section class="page-hero">
<p class="breadcrumb">%s</p>
<h1>%s</h1>
<div class="author-box">
<span aria-hidden="true" class="author-box__avatar">DH</span>
<div>
<p class="author-box__name">Daniel Hart</p>
<p class="author-box__role">Senior Pokies Reviewer &amp; iGaming Editor</p>
<p class="author-box__meta">Reviewed by Sarah Chen · Last updated 23 September 2026 · 18+</p>
</div>
</div>
<p class="lede">%s</p>
<div class="mission-box"><p><strong>&#10148; Updated for 2026:</strong> %s <a href="/methodology">See how we test</a>.</p></div>
</section>''' % (breadcrumb_html, h1, lede, mission)

# ================= PAGE =================
slug = "10-20-25-free-chip-no-deposit-australia-2026"
title = "$10, $20, $25 Free Chip No Deposit Australia 2026"
desc = ("$10, $20, $25 and $30 free chip no deposit Australia 2026: typical wagering and max-cashout rules "
        "for small free chips, keep-what-you-win reality, PayID payouts, and verified sign-up credit up to $199.")
bc = [("Home","https://bpaau.org/"),("Bonus Guides","https://bpaau.org/blog/bonus-guides"),
      ("Small Free Chips","https://bpaau.org/"+slug)]

faq = [
("What is a $10, $20 or $25 no-deposit free chip in Australia?",
 "A small no-deposit free chip is a fixed amount of bonus cash &mdash; commonly A$10, A$20, A$25 or A$30 &mdash; added to a new casino account without a deposit. It is playable on eligible pokies and behaves like a free trial stake: you complete a wagering requirement within an expiry window, respect a maximum cashout cap and finish identity verification before any winnings become withdrawable. 18+ T&amp;Cs apply."),
("Do I need a bonus code for a small free chip?",
 "Sometimes, but not on the six Australian-facing operators reviewed on BPAAU. Those brands skip coupons and release larger sign-up credit automatically after you verify an Australian mobile number by SMS OTP, or with one tap in the promotions tab. Where a smaller chip does require a code, the field appears on the registration form, in the cashier or in the promotions tab, and it must be entered exactly with no spaces before any deposit."),
("What wagering do $10 to $30 free chips usually carry?",
 "Typical playthrough on a small no-deposit chip sits around 30x to 50x the bonus amount, occasionally higher on the smallest chips. On a $20 chip at 40x that is A$800 of total eligible bets; on a $25 chip at 40x it is A$1,000. Every eligible spin reduces the total whether it wins or loses, but the house edge works against the balance while you clear it, so high-RTP eligible pokies give the best chance of finishing with funds."),
("How much can you actually cash out from a small free chip?",
 "No-deposit winnings are almost always capped. As a market rule of thumb, a $10&ndash;$25 chip commonly allows a maximum withdrawal of roughly A$50 to A$100, occasionally up to A$200; anything above the cap is forfeited regardless of how much you win. The exact cap is printed in the offer&rsquo;s terms and is the single most important figure to check before you play."),
("Is a free chip really 'keep what you win'?",
 "You keep the winnings only after wagering, KYC and the cashout cap &mdash; not the chip itself and not any amount above the cap. The phrase 'keep what you win' describes the fact that no deposit is required, not that the bonus is unrestricted cash. Offers marketed as no-wagering remove the playthrough step but still retain a cap and verification; our no-wagering guide compares them."),
("Why do the verified operators give $177 to $199 instead of just $20?",
 "The six Gaming Curacao licensed brands reviewed here use larger automatic sign-up credits as their acquisition offer rather than tiny coupons. The trade-off is that these headline amounts are governed by their own turnover or winover terms and are not instantly withdrawable. For a player comparing offers, a larger automatic credit with clear terms generally gives more spins and a better chance of a withdrawable result than a $20 chip with 50x rollover."),
("Can I claim a free chip at several casinos?",
 "You can claim one welcome no-deposit offer at each separately licensed operator, but only one per casino. Creating duplicate accounts at the same site &mdash; with a second email, number or device &mdash; is bonus abuse and results in confiscated balances. Use your real legal name and your own PayID details everywhere, because the casino account name must match the bank account that receives a withdrawal."),
("How fast do small free-chip winnings pay out in Australia?",
 "Once wagering is complete and KYC is approved, withdrawals to PayID settle in near-real time; the wait players experience is the casino&rsquo;s internal finance review, which ranges from minutes at the fastest brands to 24&ndash;72 hours elsewhere. A few sites require one small verifying deposit before a first cashout. Payouts are always limited to the max-cashout cap."),
("Are small free-chip offers safe and legal for Australians?",
 "Australian law (the Interactive Gambling Act 2001) targets operators, not individual players, while ACMA blocks sites that breach it. Safety therefore depends on the operator: use only casinos with a verifiable Gaming Curacao licence, published terms and secure PayID banking, and avoid unlicensed pages promising uncapped, zero-verification payouts, which are a common scam pattern."),
]

body = RG_BANNER
body += hero('<a href="/">Home</a> &raquo; <a href="/blog/bonus-guides">Bonus Guides</a> &raquo; <span>Small Free Chips</span>',
 "$10, $20, $25 Free Chip No Deposit in Australia (2026)",
 "Small no-deposit free chips &mdash; A$10, A$20, A$25 and A$30 &mdash; are the most searched pokies coupons in Australia, and the most misunderstood. This guide sets out the real wagering and maximum-cashout rules for each chip size, what &lsquo;keep what you win&rsquo; actually means, and why the six verified Australian-facing operators below skip the tiny-coupon model entirely and credit A$177 to A$199 automatically after mobile verification, with PayID payouts.",
 "We compared the standard terms attached to small free chips across the Australian market against the automatic sign-up offers at the six reviewed operators, so you can judge a chip by its real cashout value rather than its headline number.")

body += '''<section class="section">
<div class="section-title"><span class="section-title__label">The verified list</span><h2>Verified Sign-Up Free Credit at Australian Operators (2026)</h2></div>
<p>Before the amount-by-amount breakdown, here are the six Gaming Curacao licensed operators reviewed on BPAAU, checked 23 September 2026. Note that every one of them credits <strong>far more</strong> than a $10&ndash;$25 chip, automatically, with no coupon to expire. Open an operator name for its full offer and exact steps; confirm the active terms on registration. 18+ T&amp;Cs apply.</p>
<div class="table-wrap">
<table class="score-table">
<thead><tr><th>Operator</th><th>Sign-up free credit</th><th>Bonus code</th><th>Playthrough</th><th>Payout</th></tr></thead>
<tbody>
<tr><td><a href="/toystory9-199-free-credit-sign-up-australia-2026">TOY STORY 9</a></td><td>$199 free credit + Lucky Wheel up to $999</td><td>None &mdash; OTP auto</td><td>Per T&amp;Cs</td><td>PayID</td></tr>
<tr><td><a href="/1xaud-188-free-credit-no-deposit-australia-2026">1XAUD</a></td><td>$188 no-deposit free credit</td><td>None &mdash; claim in Promotions</td><td>Turnover per T&amp;Cs</td><td>PayID / bank</td></tr>
<tr><td><a href="/mrbluey-188-no-deposit-free-credit-australia-2026">MR BLUEY</a></td><td>$188 no-deposit free credit</td><td>None &mdash; OTP auto</td><td>Turnover per T&amp;Cs</td><td>PayID / Osko</td></tr>
<tr><td><a href="/1xace-17777-free-sign-up-no-rollover-australia-2026">1XACE</a></td><td>$177.77 free sign-up (no-rollover winover)</td><td>None &mdash; OTP auto</td><td>Winover model</td><td>PayID / crypto</td></tr>
<tr><td><a href="/garcat8-free-365-day-bonus-australia-2026">GARCAT8</a></td><td>Daily Easy Step free $100 + free-365-day</td><td>None &mdash; daily task</td><td>Per T&amp;Cs</td><td>PayID</td></tr>
<tr><td><a href="/gd8-social-share-free-credit-australia-2026">GD8</a></td><td>Social-share free credit (+ 100% welcome match)</td><td>None &mdash; share task</td><td>Per T&amp;Cs</td><td>PayID</td></tr>
</tbody>
</table>
</div>
<p>Because rollover and cashout terms change with each promotion, read the active terms linked from each operator page before accepting. If you specifically want the mechanics of a coupon rather than automatic credit, our <a href="/no-deposit-bonus-codes-australia-2026">no-deposit bonus codes guide</a> covers them in full.</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">How they work</span><h2>What a Small No-Deposit Free Chip Is</h2></div>
<p>A free chip is a fixed dollar amount of bonus cash attached to a new account. Unlike free spins, which are tied to one pokie at a set stake, a chip lets you choose stake size and game across the eligible list. The chip lands in a bonus wallet the moment you register (and enter a code if the brand uses one), and it converts to withdrawable cash only after the terms below are met. The Australian search demand clusters tightly around specific amounts &mdash; <em>&ldquo;$10 free chip no deposit&rdquo;</em>, <em>&ldquo;$20 free chip Australia&rdquo;</em>, <em>&ldquo;$25 free chip keep what you win&rdquo;</em> &mdash; which is why each tier is broken out separately next.</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">By amount</span><h2>Free Chip Amount by Amount: Real Terms</h2></div>
<p>The figures below are <strong>typical market terms</strong> for a chip of each size across Australian-facing offers, not a promise for a specific operator &mdash; always confirm the exact numbers in the active terms. The pattern is consistent: the smaller the chip, the tighter the cashout cap.</p>

<h3>$10 free chip no deposit</h3>
<p>A $10 chip is the most common entry-level coupon. Typical wagering is around 30x&ndash;50x (A$300&ndash;A$500 of turnover), with a maximum cashout commonly around A$50&ndash;A$100 and an expiry of 24&ndash;72 hours. At this size the cap, not the wagering, is the limiting factor.</p>

<h3>$20 free chip no deposit</h3>
<p>A $20 chip usually carries 35x&ndash;50x wagering (roughly A$700&ndash;A$1,000 turnover) and a cap near A$100, sometimes A$200. It gives more spins to hit a feature than a $10 chip, but the expected cost of clearing playthrough is proportionally higher.</p>

<h3>$25 free chip no deposit</h3>
<p>A $25 chip is a popular mid-tier offer, typically 30x&ndash;45x wagering (A$750&ndash;A$1,125) with a cap around A$100&ndash;A$200. This tier often represents the best balance between starting balance and achievable playthrough among the small chips.</p>

<h3>$30 free chip no deposit</h3>
<p>$30 chips are less common and frequently reserved for a small first deposit or a verification task rather than a pure registration bonus. Where genuinely free, expect similar 30x&ndash;45x wagering and a cap in the A$100&ndash;A$200 range.</p>

<h3>$50 free chip and above</h3>
<p>A true $50 no-deposit chip is rarer and heavily capped; we cover its real terms and claim steps on the dedicated <a href="/free-50-pokies-no-deposit-sign-up-bonus-australia-2026">free $50 sign-up page</a>. Amounts of $60 to $100 advertised as instant, no-verification free chips are very often scam lures.</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">The maths</span><h2>Wagering Maths for Each Chip Size</h2></div>
<div class="table-wrap">
<table class="score-table">
<thead><tr><th>Chip</th><th>30x turnover</th><th>40x turnover</th><th>50x turnover</th><th>Typical max cashout</th></tr></thead>
<tbody>
<tr><td>$10</td><td>$300</td><td>$400</td><td>$500</td><td>$50&ndash;$100</td></tr>
<tr><td>$20</td><td>$600</td><td>$800</td><td>$1,000</td><td>~$100</td></tr>
<tr><td>$25</td><td>$750</td><td>$1,000</td><td>$1,250</td><td>$100&ndash;$200</td></tr>
<tr><td>$30</td><td>$900</td><td>$1,200</td><td>$1,500</td><td>$100&ndash;$200</td></tr>
<tr><td>$50</td><td>$1,500</td><td>$2,000</td><td>$2,500</td><td>$100&ndash;$200</td></tr>
</tbody>
</table>
</div>
<p>On a 96% RTP pokie the expected loss over A$1,000 of turnover is about A$40 &mdash; comparable to a $20&ndash;$25 chip &mdash; which is why many players finish playthrough with little left. Clear wagering on eligible <a href="/best-high-rtp-pokies-australia-2026">high-RTP pokies</a> at steady stakes, and favour no-wagering or low-rollover offers where available (see the <a href="/no-wagering-bonuses-australia-2026">no-wagering guide</a>).</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">The fine print</span><h2>Five Rules That Decide a Free Chip&rsquo;s Real Value</h2></div>
<p><strong>1. Wagering</strong> &mdash; check whether it applies to the bonus only (normal for no-deposit) and the exact multiple; anything above 50x on a small chip is very hard to clear.</p>
<p><strong>2. Maximum cashout</strong> &mdash; the hard ceiling on what you can withdraw; on small chips this is usually the binding limit.</p>
<p><strong>3. Expiry</strong> &mdash; free chips commonly expire in 24&ndash;72 hours, and unfinished wagering removes the whole balance.</p>
<p><strong>4. Eligible games</strong> &mdash; pokies generally count 100%, but specific titles may be excluded while tables and progressives count zero or void the bonus.</p>
<p><strong>5. One per player and KYC</strong> &mdash; duplicates are treated as fraud, and every real withdrawal needs identity verification plus a payment method in your own name. Each clause is explained in plain English on the <a href="/how-to-read-casino-bonus-terms-australia-2026">bonus terms page</a>.</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">How to claim</span><h2>How to Claim a Free Chip (and the Better Automatic Route)</h2></div>
<ol>
<li><strong>Choose a licensed operator</strong> with a verifiable Gaming Curacao licence and an offer open to Australian accounts.</li>
<li><strong>Register with real details</strong> &mdash; legal name, Australian mobile number and your own email; the name must match your PayID.</li>
<li><strong>Verify your mobile by OTP.</strong> On the six reviewed brands this step alone releases the larger automatic credit, no coupon needed.</li>
<li><strong>Enter a code only if a field is shown</strong>; otherwise the offer is automatic and a third-party code adds nothing.</li>
<li><strong>Open an eligible pokie</strong> &mdash; common choices include <a href="/wolf-treasure-pokies-australia-2026">Wolf Treasure</a>, 5 Dragons and Gates of Olympus.</li>
<li><strong>Clear wagering before expiry</strong>, complete KYC, and <strong>withdraw to PayID</strong> up to the cap.</li>
</ol>
<p>If an automatic credit does not appear within a minute, contact 24/7 live chat with your registered number &mdash; never register a second account. The full process is in our <a href="/no-deposit-free-bonus-guide-australia-2026">no-deposit bonus guide</a>, and the whole flow works on a phone per the <a href="/mobile-pokies-australia-2026">mobile pokies guide</a>.</p>
</section>

<section class="section">
<div class="section-title"><span class="section-title__label">Cashing out &amp; safety</span><h2>PayID Payouts and Avoiding Fake Free-Chip Scams</h2></div>
<p>After wagering and KYC, the fastest Australian cashout is <strong>PayID</strong> (often labelled Osko in your banking app), which settles in near-real time; the actual wait is the casino&rsquo;s finance review, from minutes to 24&ndash;72 hours. Almost every delayed first payout traces to unfinished KYC or a name mismatch, so verify immediately and always use PayID in your own name. Our <a href="/payid-cashouts-australia-2026">PayID hub</a> records settlement times and the <a href="/same-day-pokies-withdrawals-australia">same-day rankings</a> list the fastest brands.</p>
<p>Watch for scam lures: &ldquo;free chip&rdquo; pages on unlicensed casinos, demands for an upfront &ldquo;release fee&rdquo; or &ldquo;tax&rdquo; (legitimate casinos never ask this), and promises of uncapped, zero-verification withdrawals. A genuine no-deposit offer never requires you to pay to receive money. Verify any licence with our <a href="/curacao-casino-licence-check-australia-2026">Curacao licence check</a>, and read the legal position in our <a href="/online-pokies-legality-australia-2026">Australian legality guide</a>. For the broader comparison of free chips against free spins, see the <a href="/free-chips-australia-guide-2026">free chips Australia guide</a>.</p>
</section>
'''
body += faq_section(faq)
body += related([
 ("/no-deposit-bonus-codes-australia-2026","Bonus Guides","No Deposit Bonus Codes Australia 2026: Free Pokies Coupons","How coupon codes work and the verified offers that need no code.","/blog%20banner/blogpost%204.webp","1168","784","2026-09-22","6"),
 ("/free-50-pokies-no-deposit-sign-up-bonus-australia-2026","Bonus Guides","Free $50 Pokies No Deposit Sign-Up Bonus","The larger chip tier and its real cashout terms.","/blog%20banner/blogpost%2012.webp","1376","768","2026-09-21","6"),
 ("/free-chips-australia-guide-2026","Bonus Guides","Free Chips Australia 2026 — No-Deposit Guide","Free chips vs free spins, with terms compared.","/blog%20banner/blogpost%202.webp","1168","784","2026-07-12","5"),
 ("/no-deposit-free-bonus-guide-australia-2026","Bonus Guides","No Deposit Free Bonus Guide Australia 2026","The end-to-end claim process and how to avoid dead offers.","/blog%20banner/blogpost%203.webp","1168","784","2026-08-03","5"),
])

html = head(slug, title, desc, bc, faq) + body + FOOTER
out = os.path.join(PUB, slug + ".html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("WROTE", slug + ".html", len(html), "bytes")
