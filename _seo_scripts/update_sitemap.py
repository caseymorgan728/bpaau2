#!/usr/bin/env python3
"""Insert 10 new URLs into sitemap.xml after same-day-pokies-withdrawals-australia block."""
import io

path = r"C:\Users\User\Documents\GitHub\Australia igaming website\public\sitemap.xml"
with io.open(path, "r", encoding="utf-8", newline="") as f:
    text = f.read()

# Detect line ending
nl = "\r\n" if "\r\n" in text else "\n"

new_urls = [
    "online-pokies-legality-australia-2026",
    "curacao-casino-licence-check-australia-2026",
    "how-to-play-online-pokies-beginners-australia-2026",
    "no-wagering-bonuses-australia-2026",
    "cashback-bonus-pokies-australia-2026",
    "mobile-pokies-australia-2026",
    "best-payment-methods-pokies-australia-2026",
    "fastest-withdrawal-casinos-australia-under-1-hour-2026",
    "progressive-jackpot-pokies-australia-2026",
    "vip-loyalty-programs-pokies-australia-2026",
]

block_lines = []
for slug in new_urls:
    block_lines.append("  <url>")
    block_lines.append("    <loc>https://bpaau.org/%s</loc>" % slug)
    block_lines.append("    <lastmod>2026-09-06</lastmod>")
    block_lines.append("    <changefreq>weekly</changefreq>")
    block_lines.append("    <priority>0.7</priority>")
    block_lines.append("  </url>")
block = nl.join(block_lines)

anchor = "    <loc>https://bpaau.org/same-day-pokies-withdrawals-australia</loc>"
# find the closing </url> after anchor
idx = text.index(anchor)
end_url = text.index("</url>", idx) + len("</url>")
# Insert block after the closing </url>
new_text = text[:end_url] + nl + block + text[end_url:]

# Also update lastmod for /blog and the two modified category pages
new_text = new_text.replace(
    "    <loc>https://bpaau.org/blog</loc>" + nl + "    <lastmod>2026-08-31</lastmod>",
    "    <loc>https://bpaau.org/blog</loc>" + nl + "    <lastmod>2026-09-06</lastmod>",
)
new_text = new_text.replace(
    "    <loc>https://bpaau.org/blog/bonus-guides</loc>" + nl + "    <lastmod>2026-08-31</lastmod>",
    "    <loc>https://bpaau.org/blog/bonus-guides</loc>" + nl + "    <lastmod>2026-09-06</lastmod>",
)
new_text = new_text.replace(
    "    <loc>https://bpaau.org/blog/promo-guides</loc>" + nl + "    <lastmod>2026-08-31</lastmod>",
    "    <loc>https://bpaau.org/blog/promo-guides</loc>" + nl + "    <lastmod>2026-09-06</lastmod>",
)

with io.open(path, "w", encoding="utf-8", newline="") as f:
    f.write(new_text)

print("Sitemap updated. URL count:", new_text.count("<loc>"))
