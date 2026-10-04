# -*- coding: utf-8 -*-
"""Build 7 new evidence-backed AU keyword pages for bpaau.org (week 40)."""
import pagegen as P

B = "/assets/banners/"

def offers_table(intro=None, badge="Verified free-credit offer"):
    rows = [
        ("Toy Story 9", "$199 sign-up credit", "No code &mdash; auto after mobile OTP; Lucky Wheel up to $999",
         "/toystory9-199-free-credit-sign-up-australia-2026", "/toystory9-review"),
        ("1XAUD", "$188 no-deposit credit", "No code &mdash; claim from the Promotions tab after OTP; 1,888 sign-up chips",
         "/1xaud-188-free-credit-no-deposit-australia-2026", "/1xaud-review"),
        ("Mr Bluey", "$188 no-deposit credit", "Auto after OTP; BNG free-spins offers and a 10% win/lose rebate",
         "/mrbluey-188-no-deposit-free-credit-australia-2026", "/mrbluey-review"),
        ("1XACE", "$177.77 sign-up credit", "No code after OTP; no-rollover winover and a 25% app bonus",
         "/1xace-17777-free-sign-up-no-rollover-australia-2026", "/1xace-review"),
        ("GarCat8", "Free 365-day bonus", "Daily easy-step free $100 and a $1,888.88 jackpot event",
         "/garcat8-free-365-day-bonus-australia-2026", "/garcat8-review"),
        ("GD8", "Social-share free credit", "Free credit for sharing; 1.18% rollover rebate and a $2,888 grand jackpot",
         "/gd8-social-share-free-credit-australia-2026", "/gd8-review"),
    ]
    trs = []
    for name, offer, note, promo, review in rows:
        trs.append(f"""<tr>
<td data-label="Operator"><strong>{name}</strong><br/><a href="{review}">Full review</a></td>
<td data-label="Free offer">{offer}</td>
<td data-label="Details">{note}</td>
<td data-label="Claim"><a class="btn btn--primary" href="{promo}">Claim offer</a></td>
</tr>""")
    intro_html = f"<p>{intro}</p>" if intro else ""
    return f"""{intro_html}
<div class="table-wrap">
<table class="score-table">
<thead><tr><th>Operator</th><th>Registration free credit</th><th>How it is granted</th><th>Claim</th></tr></thead>
<tbody>
{chr(10).join(trs)}
</tbody>
</table>
</div>
<p style="font-size:.9rem;color:var(--muted)">All six hold verifiable Gaming&nbsp;Curacao licences, accept Australian players and pay withdrawals through PayID. Outbound offer links are affiliate links (<code>rel=&quot;sponsored nofollow noopener&quot;</code>). 18+ T&amp;Cs apply; every offer carries its own wagering and cashout rules.</p>"""


def sec(label, h2, *body):
    return f'<section class="section">\n<div class="section-title"><span class="section-title__label">{label}</span><h2>{h2}</h2></div>\n' + "\n".join(body) + "\n</section>"


# ---------------------------------------------------------------------------
# 1. $100 NO DEPOSIT
# ---------------------------------------------------------------------------
c1 = {
 "slug": "free-100-no-deposit-bonus-australia-2026",
 "title": "$100 No Deposit Bonus Australia 2026: The Real Terms",
 "desc": "A $100 no deposit bonus for Australian pokies explained honestly: how the free $100 chip really works, wagering and max-cashout rules, scams to avoid, and the verified free-credit offers for 2026.",
 "ogimg": "https://bpaau.org/assets/banners/free-100-no-deposit-bonus-australia-2026-banner.jpg",
 "banner": B+"free-100-no-deposit-bonus-australia-2026-banner.jpg",
 "banner_alt": "Free $100 no deposit bonus for Australian pokies 2026",
 "crumbs": [("Home","/"),("Bonus Guides","/blog/bonus-guides"),("$100 No Deposit",None)],
 "active": "/no-deposit-free-bonus-guide-australia-2026",
 "h1": "$100 No Deposit Bonus in Australia &mdash; Free Pokies Credit With the Real Terms Attached (2026)",
 "lede": "A &ldquo;$100 free, no deposit&rdquo; pokie bonus is one of the most searched casino offers in Australia and one of the most misrepresented. This guide explains exactly what a $100 no-deposit chip is, why genuine versions are rare, what wagering and max-cashout rules you will actually face, and which Australian-facing operators give real registration free credit in 2026.",
 "mission": "We cross-checked the advertised &ldquo;$100 free&rdquo; offers against published bonus terms and separated real automatic credits from capped coupons and outright fakes",
 "faqs": [
  ("Is there really a $100 no deposit bonus in Australia?","A genuinely free $100 chip with no deposit exists only occasionally, and when it does it is always governed by wagering (commonly 40x&ndash;60x), a maximum withdrawal (often A$50&ndash;A$200), an expiry and KYC. Most &ldquo;$100 free&rdquo; adverts either hide these rules, bundle the $100 across several deposits, or come from unlicensed clone sites. The Australian-facing operators reviewed on BPAAU instead grant automatic registration credits of $177&ndash;$199 with published terms."),
  ("Can I keep the whole $100 if I win?","No. A no-deposit chip is bonus money, not cash, and you keep only the winnings that remain after wagering, up to the max-cashout cap. On a capped A$100 offer, winning A$2,000 on a pokie still typically allows a withdrawal of just the cap (for example A$100), with the remainder forfeited."),
  ("How much wagering does a $100 free chip require?","Market terms for a chip this size usually sit between 40x and 60x the bonus. At 50x, a $100 chip requires A$5,000 of eligible spins before anything is withdrawable. High-RTP pokies clear this with the best mathematical chance, but the house edge still works against the balance while you play."),
  ("Do I need a bonus code for the $100 offers?","The verified operators on this page require no coupon code &mdash; the free credit is granted automatically after mobile-number (OTP) verification or from the in-account Promotions tab. Be suspicious of sites demanding a code for a &ldquo;$100 free&rdquo; chip that is not mentioned in their written terms."),
  ("Why do the verified casinos give $177 to $199 instead of $100?","The six licensed brands use a larger automatic sign-up credit as their acquisition offer. It is still bonus money with turnover or winover rules and is not instantly withdrawable, but a larger automatic credit with clear, published terms generally gives a player more spins and a better chance of a withdrawable result than a small, heavily capped coupon."),
  ("Are $100 no-deposit offers legal and safe for Australians?","The Interactive Gambling Act 2001 targets the operators providing prohibited interactive gambling to Australians, not individual players, while ACMA blocks offending sites. Safety therefore depends on the operator: use only casinos with a verifiable Gaming Curacao licence, published terms and secure PayID banking, and avoid unlicensed pages promising uncapped, zero-verification $100 payouts."),
  ("How fast do no-deposit winnings pay to PayID?","After wagering is complete and KYC is approved, withdrawals to PayID settle in near-real time; the delay players feel is the casino&rsquo;s internal finance review, from minutes at the fastest brands to 24&ndash;72 hours elsewhere. A few sites require one small verifying deposit before a first cashout, and the payout can never exceed the cap."),
  ("Can I claim $100 free at several casinos?","You can claim one welcome no-deposit offer at each separately licensed operator, but only one account and one bonus per casino. Duplicate accounts opened with a second email, number or device are treated as bonus abuse and lead to confiscated balances."),
 ],
 "related": [
  ("/free-spins-no-deposit-pokies-australia-2026", B+"free-spins-no-deposit-pokies-australia-2026-banner.jpg","Bonus Guides","Free Spins No Deposit Australia 2026","Free spins instead of a cash chip, with winnings terms compared.","2026-10-04 · 7 min read · Read the guide &rarr;"),
  ("/10-payid-no-deposit-bonus-australia-2026", B+"10-payid-no-deposit-bonus-australia-2026-banner.jpg","Bonus Guides","$10 PayID No Deposit Bonus Australia","The small-chip tier with instant bank payout.","2026-10-04 · 6 min read · Read the guide &rarr;"),
  ("/free-50-pokies-no-deposit-sign-up-bonus-australia-2026","/blog%20banner/blogpost%2012.webp","Bonus Guides","Free $50 Pokies No Deposit Sign-Up Bonus","The mid-size chip tier and its real cashout terms.","2026-09-21 · 6 min read · Read the guide &rarr;"),
  ("/no-deposit-bonus-codes-australia-2026","/blog%20banner/blogpost%204.webp","Bonus Guides","No Deposit Bonus Codes Australia 2026","How coupon codes work and the verified offers that need none.","2026-09-22 · 6 min read · Read the guide &rarr;"),
 ],
}
s1 = [
 sec("The short version","What Is a &ldquo;$100 No Deposit Bonus&rdquo;?",
  '<p>A <strong>no-deposit bonus</strong> is free casino credit granted simply for opening and verifying an account &mdash; you do not have to transfer any of your own money first. A <strong>$100 no-deposit bonus</strong> advertises A$100 of that free credit, usually marketed at pokies players as a &ldquo;free $100 chip&rdquo; or &ldquo;$100 free pokies credit&rdquo;. It is the headline figure that dominates Google results for searches such as <em>&ldquo;$100 no deposit bonus 2026 real money free play&rdquo;</em> and <em>&ldquo;$100 free casino chips without deposit NSW&rdquo;</em>.</p>',
  '<p>The crucial detail almost every advert leaves out is that the A$100 is <strong>bonus money, not withdrawable cash</strong>. Before a single dollar can be paid to your bank you generally have to complete wagering, pass identity verification (KYC) and stay inside a maximum-withdrawal cap. Understanding those three conditions is the difference between a genuine free chance and a marketing trap.</p>'),
 sec("The reality","Why a True Free $100 Chip Is Rare (and Often Fake)",
  '<p>Legitimate casinos run on a mathematical edge, so handing out A$100 of unrestricted cash to every new player would be commercial suicide. When you see &ldquo;$100 free, no deposit, keep winnings&rdquo; in 2026, it is almost always one of four things:</p>',
  '<ol><li><strong>A real but heavily conditioned chip</strong> &mdash; wagering of 40x&ndash;60x, a low max-cashout cap and a short expiry. These exist but are uncommon at A$100.</li><li><strong>A bundled &ldquo;package&rdquo; figure</strong> &mdash; the $100 is spread across your first several deposits (e.g. a deposit match), which is not a no-deposit offer at all.</li><li><strong>A free-spins equivalent</strong> &mdash; the &ldquo;$100&rdquo; is the theoretical value of a batch of spins at a fixed coin value, with wagering on whatever they win.</li><li><strong>A scam clone</strong> &mdash; an unlicensed page using a familiar-sounding name and a stolen logo, designed to harvest phone numbers and card details. These dominate the cheapest ad slots.</li></ol>',
  '<p>Our <a href="/methodology">six-step audit</a> treats any offer that cannot be matched to a published licence and written terms as unverifiable. A surprising number of &ldquo;$100 free&rdquo; landing pages fail that basic test.</p>'),
 sec("Verified offers","Australian-Facing Operators With Real Registration Free Credit",
  offers_table("Rather than chase phantom $100 coupons, the most reliable free value in the Australian market in 2026 is the automatic registration credit offered by six Gaming&nbsp;Curacao-licensed brands. The headline amounts are larger than $100, require no coupon code, and each has a dedicated terms page:"),
  '<p>You can read the full background to each brand on their review pages (<a href="/toystory9-review">Toy Story 9</a>, <a href="/1xaud-review">1XAUD</a>, <a href="/mrbluey-review">Mr Bluey</a>, <a href="/1xace-review">1XACE</a>, <a href="/garcat8-review">GarCat8</a> and <a href="/gd8-review">GD8</a>), and compare the smaller chip tiers on our <a href="/10-20-25-free-chip-no-deposit-australia-2026">$10&ndash;$25 free-chip guide</a> and <a href="/free-50-pokies-no-deposit-sign-up-bonus-australia-2026">$50 sign-up page</a>.</p>'),
 sec("How it works","How to Claim a No-Deposit Pokies Bonus in Australia",
  '<ol><li><strong>Choose one licensed operator</strong> from the table and open it through the offer link (affiliate links are marked <code>sponsored nofollow</code>).</li><li><strong>Register with your real details</strong> &mdash; legal name, Australian mobile number and email. The name must later match your PayID/bank account.</li><li><strong>Verify your mobile number</strong> with the one-time PIN (OTP). The automatic credits above are released at this step or from the in-account <em>Promotions</em> tab.</li><li><strong>If a code is genuinely required</strong>, enter it exactly as published on the terms page &mdash; the six verified brands above need none.</li><li><strong>Play eligible pokies</strong> to clear wagering; note which games contribute and at what percentage.</li><li><strong>Complete KYC</strong> (ID plus proof of address) and request a PayID withdrawal once the cap and wagering are met.</li></ol>',
  '<p>The full end-to-end process, including screenshots of where bonuses appear, is on our <a href="/no-deposit-free-bonus-guide-australia-2026">no-deposit free-bonus guide</a>.</p>'),
 sec("The maths","Wagering on a $100 Chip, Worked Example",
  '<p>Wagering (also called playthrough or rollover) is the total value of eligible bets required before bonus funds become cash. It is the single number that decides whether a &ldquo;free $100&rdquo; is realistically cashable.</p>',
  '<div class="table-wrap"><table class="score-table"><thead><tr><th>Bonus</th><th>Wagering</th><th>Total spins required</th><th>Realistic at high RTP?</th></tr></thead><tbody>'
  '<tr><td>$100 chip</td><td>40x</td><td>A$4,000</td><td>Possible &mdash; needs patience and high-RTP pokies</td></tr>'
  '<tr><td>$100 chip</td><td>50x</td><td>A$5,000</td><td>Hard &mdash; most balances reach zero first</td></tr>'
  '<tr><td>$100 chip</td><td>60x+</td><td>A$6,000+</td><td>Very unlikely to retain value</td></tr>'
  '</tbody></table></div>',
  '<p>Because every spin carries a house edge, the expected value of a bonus falls as wagering rises. Choosing pokies with an RTP around 96.5%&ndash;97% (see the <a href="/best-high-rtp-pokies-australia-2026">best high-RTP pokies</a>) and avoiding restricted or low-weighting games gives the best chance of finishing with funds. Our <a href="/how-to-read-casino-bonus-terms-australia-2026">bonus-terms guide</a> shows exactly where these figures are printed.</p>'),
 sec("Cashout cap","The Max-Cashout Rule Nobody Advertises",
  '<p>No-deposit winnings are almost always capped. As a market rule of thumb, a free chip commonly allows a maximum withdrawal of roughly A$50&ndash;A$200 regardless of how much you win; offers above that are rare and usually demand a verifying deposit. Anything above the cap is forfeited at cashout.</p>',
  '<p>This is why a &ldquo;$100 free&rdquo; chip that produces a A$3,000 jackpot rarely pays A$3,000. The cap is the single most important figure to check before you play, and it must be written in the terms &mdash; if support cannot point to it, treat the offer as unsafe.</p>'),
 sec("Offer types","$100 Chip vs Free Spins vs Deposit Match",
  '<div class="table-wrap"><table class="score-table"><thead><tr><th>Offer type</th><th>What you get</th><th>Wagering applies to</th><th>Typical cap</th></tr></thead><tbody>'
  '<tr><td>$100 free chip</td><td>A$100 bonus balance</td><td>The bonus amount</td><td>A$50&ndash;A$200</td></tr>'
  '<tr><td>Free spins no deposit</td><td>10&ndash;50 spins at a fixed coin value</td><td>Spin winnings</td><td>A$50&ndash;A$150</td></tr>'
  '<tr><td>Welcome deposit match</td><td>% of your own deposit</td><td>Bonus + sometimes deposit</td><td>Often higher/uncapped, but requires funding</td></tr>'
  '<tr><td>Cashback / rebate</td><td>A share of losses returned</td><td>Often low or none</td><td>Varies</td></tr>'
  '</tbody></table></div>',
  '<p>If you specifically want no-cost spins, our <a href="/free-spins-no-deposit-pokies-australia-2026">free-spins no-deposit guide</a> covers eligible games and winnings rules; if you want the smallest, easiest-to-clear chip, see the <a href="/10-payid-no-deposit-bonus-australia-2026">$10 PayID page</a>.</p>'),
 sec("Getting paid","Turning a No-Deposit Win Into PayID Cash",
  '<p>All six verified operators settle withdrawals through <strong>PayID</strong>, the Australian fast-bank-rail service that moves funds between participating banks in near-real time, often within minutes. The practical steps are:</p>',
  '<ul><li>Finish wagering before requesting a payout &mdash; withdrawing early usually forfeits the bonus.</li><li>Complete KYC once, early, to avoid a last-minute delay.</li><li>Withdraw to a PayID (mobile number, email or ABN) held in the same name as the casino account.</li><li>Expect an internal finance review of minutes to 24&ndash;72 hours; the bank transfer itself is then fast. See <a href="/payid-cashouts-australia-2026">PayID cashout timings</a>.</li></ul>',
  '<p>Some sites require one small deposit first purely to verify the receiving account &mdash; this is standard anti-fraud practice, not a charge. For sites that streamline documents, see <a href="/payid-pokies-no-verification-australia-2026">PayID pokies with reduced verification</a>.</p>'),
 sec("Safety & law","Legality, Licensing and Scam Red Flags",
  '<p>Under the <strong>Interactive Gambling Act 2001 (Cth)</strong>, Australia prohibits the <em>provision</em> of online casino and pokie games to people in Australia by unlicensed operators; the regulator ACMA asks for and blocks offending sites. The law is aimed at operators, not at individual adults who play, which is why Australians use offshore, licensed brands. Our <a href="/online-pokies-legality-australia-2026">legality guide</a> sets this out in full.</p>',
  '<p>Because the sector is offshore, licence checks matter. Every operator on this page holds a verifiable <a href="/curacao-casino-licence-check-australia-2026">Gaming&nbsp;Curacao licence</a>. Treat the following as red flags on any &ldquo;$100 free&rdquo; page: no visible licence number; no written bonus terms; promises of uncapped or guaranteed profit; pressure to deposit before you can &ldquo;release&rdquo; free winnings; a domain that copies a famous brand with a strange suffix; or requests to send crypto or vouchers to an individual.</p>'),
 sec("Play it smart","Tips to Actually Cash Out a Free Chip",
  '<ul><li><strong>Read the cap and wagering first</strong> &mdash; two numbers tell you if the offer is worth playing.</li><li><strong>Stick to eligible, high-RTP pokies</strong> and avoid table games if they contribute 0%.</li><li><strong>Use small, consistent stakes</strong>; max-betting a bonus balance usually ends it quickly.</li><li><strong>Verify your identity early</strong> and use your own PayID details.</li><li><strong>Track the expiry</strong> &mdash; unused free credit and unfinished wagering disappear when it lapses.</li><li><strong>Never open duplicate accounts</strong> to chase the bonus again.</li><li><strong>Treat it as entertainment</strong>, not income &mdash; and use <a href="/responsible-gambling">responsible-gambling tools</a> (1800&nbsp;858&nbsp;858, BetStop) if play stops being fun.</li></ul>'),
]

# ---------------------------------------------------------------------------
# 2. FREE SPINS NO DEPOSIT
# ---------------------------------------------------------------------------
c2 = {
 "slug": "free-spins-no-deposit-pokies-australia-2026",
 "title": "Free Spins No Deposit Australia 2026: Keep Winnings",
 "desc": "Free spins no deposit for Australian pokies in 2026: which casinos give registration free spins, the eligible games (Wolf Treasure, Big Bass, Gates of Olympus), wagering on winnings, caps and PayID cashout.",
 "ogimg": "https://bpaau.org/assets/banners/free-spins-no-deposit-pokies-australia-2026-banner.jpg",
 "banner": B+"free-spins-no-deposit-pokies-australia-2026-banner.jpg",
 "banner_alt": "Free spins with no deposit on Australian pokies 2026",
 "crumbs": [("Home","/"),("Bonus Guides","/blog/bonus-guides"),("Free Spins No Deposit",None)],
 "active": "/no-deposit-free-bonus-guide-australia-2026",
 "h1": "Free Spins No Deposit in Australia &mdash; Keep Pokie Winnings the Honest Way (2026)",
 "lede": "Free spins with no deposit are the most popular registration bonus for Australian pokie players because they let you spin real reels without funding an account. This guide covers which casinos actually give them in 2026, the pokies they work on, how wagering attaches to what you win, the cashout caps, and how to move winnings to PayID.",
 "mission": "We verified which Australian-facing brands grant free or free-credit spins on registration and documented the wagering, eligible-game and cashout terms attached to each",
 "faqs": [
  ("What are free spins with no deposit?","They are spins on a nominated pokie, paid for by the casino rather than your balance, granted simply for registering (and usually verifying your mobile number). You make no deposit, but anything the spins win is treated as bonus money subject to wagering and a max-cashout cap."),
  ("Which online casinos give free spins on sign-up in Australia?","The six Gaming Curacao-licensed operators reviewed on BPAAU grant registration free credit that can be used on pokies, and several run dedicated free-spins offers &mdash; notably Mr Bluey&rsquo;s BNG free-spins bonus and GD8&rsquo;s social-share free credit. The table on this page links to each offer&rsquo;s terms. 18+ T&amp;Cs apply."),
  ("What pokies can I use no-deposit free spins on?","Operators nominate the eligible game, commonly a popular, mobile-friendly title such as Wolf Treasure, Big Bass Bonanza, Sweet Bonanza or Gates of Olympus. The eligible slot, coin value and number of spins are fixed in the offer terms; you cannot usually swap them to another game."),
  ("Do free-spins winnings have wagering requirements?","Almost always. Wagering applies to the total amount the spins win (for example, 40x winnings), not to the spins themselves. A batch that wins A$20 at 40x then requires A$800 of eligible play before the balance is cashable, up to the max-cashout cap."),
  ("How much can I withdraw from no-deposit free spins?","Caps commonly sit between A$50 and A$150 for a registration spin batch, occasionally A$200. Winnings above the cap are forfeited. The exact figure is printed in the offer terms and is the first thing to check before you play."),
  ("Are free spins really free?","There is no purchase required to receive them, which is what &ldquo;free&rdquo; means, but they are not unconditional cash &mdash; wagering, KYC, a cap and an expiry always apply. Offers marketed as no-wagering remove the playthrough step but still keep the cap and identity verification."),
  ("Can I win real money and withdraw via PayID?","Yes. Once wagering is complete and KYC approved, winnings within the cap can be withdrawn to PayID and typically reach an Australian bank within minutes of the casino&rsquo;s finance approval. A few sites require one small verifying deposit before the first payout."),
  ("Can I claim free spins at more than one casino?","Yes &mdash; one welcome offer per casino, but you can register separately at each licensed operator. Never create a second account at the same site, as duplicate accounts are treated as bonus abuse and void winnings."),
 ],
 "related": [
  ("/free-100-no-deposit-bonus-australia-2026", B+"free-100-no-deposit-bonus-australia-2026-banner.jpg","Bonus Guides","$100 No Deposit Bonus Australia 2026","The larger cash-chip tier and its real terms.","2026-10-04 · 7 min read · Read the guide &rarr;"),
  ("/mrbluey-bng-free-spins-bonus-australia-2026","/blog%20banner/blogpost%202.webp","Promo Guides","Mr Bluey BNG Free Spins Bonus","A dedicated free-spins offer with claim steps.","2026-09-12 · 5 min read · Read the guide &rarr;"),
  ("/wolf-treasure-pokies-australia-2026", "/assets/banners/wolf-treasure-pokies-australia-2026-banner.jpg","Top Pokies","Wolf Treasure Pokies Australia","The pokie most AU free-spins offers use.","2026-09-21 · 7 min read · Read the guide &rarr;"),
  ("/no-wagering-bonuses-australia-2026","/blog%20banner/blogpost%203.webp","Bonus Guides","No-Wagering Bonuses Australia","Offers that remove the playthrough step.","2026-08-10 · 5 min read · Read the guide &rarr;"),
 ],
}
s2 = [
 sec("The short version","What Are No-Deposit Free Spins?",
  '<p><strong>Free spins</strong> are individual bets on a pokie that the casino pays for instead of you. When they are granted <strong>with no deposit</strong>, you receive them just for opening and verifying an account &mdash; no card, no bank transfer, no crypto. Reels spin at a fixed coin value on a nominated slot, and the money they land goes into a bonus balance.</p>',
  '<p>For Australian players this is the lowest-risk way to try a real-money casino: you can feel the mobile lobby, test a specific pokie and, if the math works out, convert winnings to <a href="/payid-cashouts-australia-2026">PayID cash</a>. The catch is always in the terms &mdash; wagering on the winnings, a cap, KYC and an expiry.</p>'),
 sec("Where to get them","Verified Australian-Facing Free-Spins &amp; Free-Credit Offers",
  offers_table("These six licensed brands give registration free credit that plays on pokies, with dedicated free-spins offers at Mr Bluey and GD8. Each row links to the exact offer and its terms:"),
  '<p>For spins tied to a specific provider, the <a href="/mrbluey-bng-free-spins-bonus-australia-2026">Mr Bluey BNG free-spins bonus</a> is the most direct. If you would rather have flexible credit you can spend on any pokie, the automatic sign-up credits from Toy Story 9, 1XAUD and 1XACE are the better fit.</p>'),
 sec("Eligible games","Which Pokies Do Free Spins Work On?",
  '<p>Casinos attach no-deposit spins to games that are lightweight on mobile, popular with Australians and cheap for the operator to provide. The recurring choices are:</p>',
  '<ul><li><strong><a href="/wolf-treasure-pokies-australia-2026">Wolf Treasure</a></strong> &mdash; the outback IGTech pokie with the golden-moon Money Respin and three jackpots; the single most common free-spins game in the AU market.</li><li><strong><a href="/big-bass-bonanza-pokies-australia-2026">Big Bass Bonanza</a></strong> &mdash; Pragmatic Play&rsquo;s fishing pokie with a retriggable free-spins round and multiplier wilds (RTP about 96.7%).</li><li><strong><a href="/sweet-bonanza-pokies-australia-2026">Sweet Bonanza</a></strong> &mdash; the tumble-wins candy pokie whose free-spins round carries 2x&ndash;100x multiplier bombs.</li><li><strong><a href="/gate-of-olympus-pokies-australia-2026">Gates of Olympus</a></strong> &mdash; the high-volatility multiplier pokie from Pragmatic Play.</li><li>Australian-Asian favourites such as <a href="/5-dragons-pokies-australia-2026">5 Dragons</a> and <a href="/thunderstruck-2-pokies-australia-2026">Thunderstruck II</a> on selected offers.</li></ul>',
  '<p>The eligible slot, number of spins and fixed coin value are set in the terms &mdash; you cannot normally move spins to a different game. Browse trending titles on the <a href="/hot-pokies-australia-2026-popular-slots">hot pokies list</a>.</p>'),
 sec("The mechanics","How Free Spins Actually Work",
  '<ol><li><strong>Trigger/grant</strong> &mdash; after OTP verification the spins (or free credit) appear in your account or the nominated game.</li><li><strong>Fixed value</strong> &mdash; each spin is worth a set amount (commonly A$0.10&ndash;A$0.40); you cannot change the stake.</li><li><strong>Winnings accrue as bonus money</strong> &mdash; including anything won inside in-game free-spins features.</li><li><strong>Wagering applies to winnings</strong> &mdash; e.g. A$20 won at 40x means A$800 of eligible play.</li><li><strong>Cap and expiry</strong> &mdash; only winnings up to the cap survive, and unfinished wagering lapses after the stated days.</li></ol>',
  '<p>Some offers are described as <strong>no-wagering</strong> or <strong>no-rollover</strong> (for example 1XACE&rsquo;s no-rollover winover and Toy Story 9&rsquo;s daily no-rollover bonus). These remove step 4 but retain KYC and often a cap &mdash; compare them on the <a href="/no-wagering-bonuses-australia-2026">no-wagering bonuses page</a>.</p>'),
 sec("Free spins vs credit","Which Should You Choose?",
  '<div class="table-wrap"><table class="score-table"><thead><tr><th></th><th>No-deposit free spins</th><th>No-deposit free credit</th></tr></thead><tbody>'
  '<tr><td>Game choice</td><td>One nominated pokie</td><td>Often many eligible pokies</td></tr>'
  '<tr><td>Stake</td><td>Fixed, low</td><td>You choose within max-bet rules</td></tr>'
  '<tr><td>Wagering base</td><td>Spin winnings</td><td>The credit amount</td></tr>'
  '<tr><td>Best for</td><td>Trying a specific game</td><td>Exploring the lobby and picking high-RTP slots</td></tr>'
  '</tbody></table></div>',
  '<p>If your goal is to evaluate a single popular pokie, spins are ideal; if you want control over stake and game, take the credit and play the <a href="/best-high-rtp-pokies-australia-2026">highest-RTP pokies</a>.</p>'),
 sec("The maths","Wagering on Free-Spins Winnings",
  '<p>Suppose 30 spins at A$0.20 win a combined A$24, with 40x wagering on winnings. You would need A$960 of eligible bets before the A$24 (and any further winnings up to the cap) becomes cashable. Because the house edge erodes the balance during playthrough, clearing wagering is never guaranteed &mdash; it is a chance, not an entitlement.</p>',
  '<p>Improve the odds by playing only eligible pokies with high RTP, avoiding gamble features that can void bonuses, and keeping stakes steady. Our <a href="/how-to-read-casino-bonus-terms-australia-2026">terms-reading guide</a> lists every clause that can void a payout.</p>'),
 sec("Getting paid","Withdrawing Free-Spins Winnings via PayID",
  '<p>After wagering and KYC, request a withdrawal to a PayID in your own name. PayID moves money between Australian banks in near-real time once the casino approves it; the realistic end-to-end wait is dominated by the operator&rsquo;s finance review (minutes to 24&ndash;72 hours). Same-day operators are compared on the <a href="/same-day-pokies-withdrawals-australia">same-day withdrawals page</a>, and the sub-one-hour tier on the <a href="/fastest-withdrawal-casinos-australia-under-1-hour-2026">fastest-payout ranking</a>.</p>'),
 sec("Safety","Scams and Red Flags on &ldquo;Free Spins&rdquo; Ads",
  '<p>Free spins are a common bait for clone sites. Avoid pages that promise hundreds of &ldquo;instantly withdrawable&rdquo; spins with no terms, have no visible Gaming&nbsp;Curacao licence, use a misspelled version of a known brand, or demand a deposit &ldquo;to verify&rdquo; before releasing no-deposit winnings. Stick to the <a href="/curacao-casino-licence-check-australia-2026">licence-verified operators</a> and confirm the offer on the casino&rsquo;s own promotions page.</p>'),
 sec("Play it smart","Maximising a Free-Spins Bonus",
  '<ul><li>Note the eligible game, spin value, wagering and cap before you start.</li><li>Use the spins promptly &mdash; most expire within days.</li><li>Clear wagering on high-RTP eligible pokies with steady stakes.</li><li>Verify your ID and PayID name early.</li><li>Do not chase losses or open duplicate accounts.</li><li>Remember the pokie is a game of chance &mdash; use <a href="/responsible-gambling">responsible-gambling tools</a> and 1800&nbsp;858&nbsp;858 if needed.</li></ul>'),
]

# ---------------------------------------------------------------------------
# 3. $10 PAYID NO DEPOSIT
# ---------------------------------------------------------------------------
c3 = {
 "slug": "10-payid-no-deposit-bonus-australia-2026",
 "title": "$10 PayID No Deposit Bonus Australia 2026: Free Chip",
 "desc": "The $10 PayID no-deposit bonus for Australian pokies: whether a free $10 chip exists, how PayID withdrawals work, wagering and caps on small chips, and the verified automatic free-credit casinos for 2026.",
 "ogimg": "https://bpaau.org/assets/banners/10-payid-no-deposit-bonus-australia-2026-banner.jpg",
 "banner": B+"10-payid-no-deposit-bonus-australia-2026-banner.jpg",
 "banner_alt": "$10 PayID no deposit bonus for Australian pokies 2026",
 "crumbs": [("Home","/"),("Bonus Guides","/blog/bonus-guides"),("$10 PayID No Deposit",None)],
 "active": "/no-deposit-free-bonus-guide-australia-2026",
 "h1": "$10 PayID No Deposit Bonus in Australia &mdash; The Small Free Chip With Fast Bank Payout (2026)",
 "lede": "The &ldquo;$10 PayID no deposit bonus&rdquo; is one of the most frequently asked questions on Australian pokies forums: a small free chip you can claim without funding an account, with winnings paid straight to your bank through PayID. Here is what actually exists in 2026, how PayID fits in, and the realistic wagering and cashout terms.",
 "mission": "We answered the recurring &ldquo;which casinos offer a $10 PayID no-deposit bonus&rdquo; question by separating genuine small chips from marketing language and documenting the PayID payout path",
 "faqs": [
  ("What is a $10 PayID no deposit bonus?","It is a small free chip of about A$10 granted on registration with no deposit, where the casino supports PayID for the eventual withdrawal. PayID is the Australian fast-bank payout rail &mdash; it is how winnings reach your bank, not how the bonus itself is handed out, which is normally automatic after mobile OTP verification."),
  ("Do Australian online casinos actually give a free $10 chip?","Small free chips appear occasionally as short promotions, but the established Australian-facing licensed brands more often grant larger automatic registration credits ($177&ndash;$199) rather than $10 coupons. A free $10 chip always carries wagering and a cap; the six verified operators on this page give more free value with no coupon code."),
  ("Do I need a bonus code for a $10 PayID chip?","The verified operators require no code &mdash; credit is released after OTP verification or from the Promotions tab. Treat any site demanding a code for a tiny chip that is not in its written terms with caution."),
  ("What wagering does a $10 chip carry?","Typically 30x&ndash;50x the bonus. On a $10 chip at 40x that is A$400 of eligible spins &mdash; much easier to clear than a $100 chip, which is the appeal of small free chips."),
  ("How much can I cash out from a $10 free chip?","Small-chip caps commonly range from A$50 to A$100. You forfeit anything above the cap. The cap and any requirement for one small verifying deposit are stated in the offer terms."),
  ("How fast does PayID pay no-deposit winnings?","Once wagering is complete and KYC is approved, the PayID transfer itself settles in near-real time (often minutes). The wait is the casino&rsquo;s internal review, from minutes at the fastest sites to 24&ndash;72 hours elsewhere."),
  ("Is PayID safe for Australian pokie withdrawals?","Yes. PayID is an Australian banking-industry service that sends payments between participating banks using a mobile number, email or ABN instead of a BSB and account number. Use a PayID held in the same name as your casino account; mismatched names are rejected for anti-fraud reasons."),
  ("Is claiming a no-deposit chip legal in Australia?","The Interactive Gambling Act 2001 regulates operators rather than individual adult players, while ACMA blocks sites that breach it. Play only at operators with a verifiable Gaming Curacao licence, published terms and secure PayID banking."),
 ],
 "related": [
  ("/free-100-no-deposit-bonus-australia-2026", B+"free-100-no-deposit-bonus-australia-2026-banner.jpg","Bonus Guides","$100 No Deposit Bonus Australia 2026","The large-chip tier and why genuine versions are rare.","2026-10-04 · 7 min read · Read the guide &rarr;"),
  ("/10-20-25-free-chip-no-deposit-australia-2026","/blog%20banner/blogpost%202.webp","Bonus Guides","$10/$20/$25 Free Chips Australia","Small-chip tiers with wagering and caps compared.","2026-09-23 · 6 min read · Read the guide &rarr;"),
  ("/payid-pokies-australia-2026","/blog%20banner/blogpost%203.webp","Fast Cashouts","PayID Pokies Australia 2026","How PayID deposits and withdrawals work at pokies sites.","2026-08-15 · 6 min read · Read the guide &rarr;"),
  ("/payid-pokies-no-verification-australia-2026","/blog%20banner/blogpost%204.webp","Fast Cashouts","PayID Pokies With Reduced Verification","Sites that streamline documents before payout.","2026-09-20 · 6 min read · Read the guide &rarr;"),
 ],
}
s3 = [
 sec("The short version","What Does &ldquo;$10 PayID No Deposit&rdquo; Mean?",
  '<p>The phrase combines two separate ideas. A <strong>$10 no-deposit bonus</strong> is a small free chip granted for registering an account, with no deposit required. <strong>PayID</strong> is the Australian fast-payment service used to move any eventual winnings into your bank. So a &ldquo;$10 PayID no-deposit bonus&rdquo; is simply a tiny free chip at a casino that pays out through PayID.</p>',
  '<p>It is important to separate the two: PayID is not how you receive the A$10 (that happens automatically after mobile verification), and PayID does not make the bonus &ldquo;instant cash&rdquo;. Wagering, KYC and a cap still apply before a withdrawal.</p>'),
 sec("Does it exist","Is There a Real Free $10 Chip in 2026?",
  '<p>Small A$10&ndash;A$25 free chips appear as short-lived promotions, and we track the tiers on our dedicated <a href="/10-20-25-free-chip-no-deposit-australia-2026">$10/$20/$25 free-chip page</a>. However, the established Australian-facing licensed brands have largely moved to <strong>larger automatic registration credits</strong>, because a tiny coupon attracts bonus-hunters and costs support time. The verified 2026 offers therefore give more free value up front:</p>',
  offers_table("These automatic credits require no coupon code and are released after mobile OTP verification (or from the Promotions tab), with PayID supported for withdrawal:"),
  '<p>If you specifically want the smallest, simplest chip to learn the process, the A$10&ndash;A$25 tier guide explains where small promotions appear and how they compare.</p>'),
 sec("PayID explained","How PayID Works for Australian Pokie Payouts",
  '<p>PayID is run by Australian banks through the New Payments Platform. Instead of quoting a BSB and account number, you link a mobile number, email address or ABN to a bank account; a casino withdrawal sent to your PayID is routed to that account. Transfers between participating banks typically settle in near-real time, 24/7.</p>',
  '<ul><li><strong>Deposits</strong> are instant, so funds appear in your casino balance within minutes.</li><li><strong>Withdrawals</strong> are fast once the casino approves them &mdash; the bank leg is usually minutes; the operator&rsquo;s review is the variable part.</li><li><strong>Names must match</strong>: the casino account and the PayID owner should be the same person.</li></ul>',
  '<p>Full setup and timing details are on the <a href="/payid-pokies-australia-2026">PayID pokies guide</a>, and same-day operators are ranked on the <a href="/same-day-pokies-withdrawals-australia">same-day withdrawals page</a>.</p>'),
 sec("The terms","Wagering and Cashout on a $10 Chip",
  '<p>Small chips are the most realistically clearable no-deposit offers because the wagering total is low. At 40x, a A$10 chip needs A$400 of eligible spins, versus A$4,000&ndash;A$5,000 for a A$100 chip. The trade-off is a lower cap.</p>',
  '<div class="table-wrap"><table class="score-table"><thead><tr><th>Chip</th><th>Typical wagering</th><th>Playthrough total</th><th>Common max cashout</th></tr></thead><tbody>'
  '<tr><td>$10</td><td>40x</td><td>A$400</td><td>A$50&ndash;A$100</td></tr>'
  '<tr><td>$20</td><td>40x</td><td>A$800</td><td>A$50&ndash;A$100</td></tr>'
  '<tr><td>$25</td><td>40x</td><td>A$1,000</td><td>A$100&ndash;A$200</td></tr>'
  '</tbody></table></div>'),
 sec("Claim steps","How to Claim and Cash Out",
  '<ol><li>Register at one verified operator using your real name and Australian mobile number.</li><li>Enter the OTP to verify; the free credit is released automatically.</li><li>Play eligible high-RTP pokies to clear wagering.</li><li>Complete KYC (ID and proof of address).</li><li>Register your PayID in your banking app if you have not already.</li><li>Request withdrawal to your PayID; allow minutes to 72 hours for approval, then a near-instant bank transfer.</li></ol>'),
 sec("Verification","KYC and the &ldquo;Verifying Deposit&rdquo;",
  '<p>Australian-facing casinos are required to know their customers. Before a first no-deposit payout you will usually verify identity and address. A small number of operators also require one small deposit to confirm the receiving PayID &mdash; this is refundable and anti-fraud, not a hidden charge. Sites that promise genuinely zero checks on a real-money payout are generally unsafe; see the nuance on the <a href="/payid-pokies-no-verification-australia-2026">reduced-verification page</a>.</p>'),
 sec("PayID safety","PayID Fees, Limits and Safety for Pokie Payouts",
  '<p>Australian players choose PayID for pokies because it is fast, familiar and free at most banks. Key facts:</p>',
  '<ul><li><strong>Cost:</strong> banks generally do not charge for receiving a PayID payment; any casino-side withdrawal fee should be stated before you confirm.</li><li><strong>Speed:</strong> once the casino approves the payout, the transfer usually settles in near-real time, including evenings and weekends, unlike traditional bank transfers that can wait for business hours.</li><li><strong>Privacy:</strong> you share a PayID (mobile/email) rather than your BSB and account number with the casino.</li><li><strong>Name matching:</strong> payments display the recipient account name before confirmation, which reduces misdirected transfers &mdash; and is why your casino and PayID names must match.</li><li><strong>Limits:</strong> casinos set minimum and maximum withdrawal amounts; a small free-chip win near the cap is rarely an issue, but large jackpot payouts may be split or require additional checks.</li></ul>',
  '<p>Always enable your bank&rsquo;s transaction notifications so you can see exactly when a payout lands. For the operators with the quickest internal approval, see the <a href="/fastest-withdrawal-casinos-australia-under-1-hour-2026">fastest-withdrawal ranking</a> and the broader <a href="/payid-cashouts-australia-2026">PayID cashout guide</a>.</p>'),
 sec("Safety","Red Flags on &ldquo;$10 PayID Free&rdquo; Ads",
  '<p>Avoid listings with no licence number, no written terms, &ldquo;guaranteed&rdquo; profit language, or requests to send PayID money to an individual to &ldquo;activate&rdquo; a bonus. Confirm every offer on the casino&rsquo;s own promotions page and only use <a href="/curacao-casino-licence-check-australia-2026">licence-verified operators</a>. The legal background is summarised in our <a href="/online-pokies-legality-australia-2026">legality guide</a>.</p>'),
 sec("Play it smart","Making the Small Chip Count",
  '<ul><li>Prefer the smallest wagering and the highest stated cap.</li><li>Clear it on eligible pokies around 96.5%+ RTP.</li><li>Keep stakes small and steady rather than max-betting.</li><li>Verify ID and PayID early to avoid a payout wait.</li><li>Treat any cashout as a bonus, not an income, and gamble responsibly (1800&nbsp;858&nbsp;858, <a href="/responsible-gambling">tools here</a>).</li></ul>'),
]

PAGES = [(c1,s1),(c2,s2),(c3,s3)]
if __name__ == "__main__":
    for cfg, sections in PAGES:
        P.write_page(cfg, sections)
    print("batch A (3 money pages) built")
