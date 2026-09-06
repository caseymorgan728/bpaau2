# -*- coding: utf-8 -*-
"""Add inline-figure to 3 pillar pages missing it."""
import os

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

def insert_before(fname, marker, figure):
    path = os.path.join(PUB, fname)
    txt = open(path, encoding="utf-8").read()
    if "inline-figure" in txt:
        print(f"SKIP {fname}: already has inline-figure")
        return
    idx = txt.find(marker)
    if idx == -1:
        print(f"MARKER NOT FOUND in {fname}: {marker[:60]!r}")
        return
    txt = txt[:idx] + figure + "\n" + txt[idx:]
    open(path, "w", encoding="utf-8").write(txt)
    print(f"ADDED inline-figure to {fname}")

# 1. Curacao: after the red-flag table, before that section closes
curacao_fig = (
    '<figure class="inline-figure">\n'
    '<img alt="Curacao casino licence verification check shield and badge" decoding="async" height="360" loading="lazy" src="/assets/hero/curacao-verified.webp" width="640"/>\n'
    '<figcaption>Verify any Gaming Curacao licence in the public registry before you deposit</figcaption>\n'
    '</figure>\n'
)
# marker: the unique </table></div>\n</section> right after the table-wrap in step-by-step
insert_before(
    "curacao-casino-licence-check-australia-2026.html",
    '<div class="table-wrap"><table class="score-table"><thead><tr><th>Check</th><th>Healthy sign</th><th>Red flag</th></tr></thead><tbody><tr><td>Licence number in footer</td>',
    ""  # placeholder; we insert AFTER the table row block instead
)
# Easier: insert the figure right before the closing </section> that follows the table.
# Do a targeted replace:
path = os.path.join(PUB, "curacao-casino-licence-check-australia-2026.html")
txt = open(path, encoding="utf-8").read()
old = '<tr><td>Company name</td><td>Holder matches footer</td><td>No company named</td></tr></tbody></table></div>\n</section>'
new = '<tr><td>Company name</td><td>Holder matches footer</td><td>No company named</td></tr></tbody></table></div>\n' + curacao_fig + '</section>'
if old in txt and "inline-figure" not in txt:
    txt = txt.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(txt)
    print("ADDED curacao inline-figure")
else:
    print("curacao: marker issue (already has figure or marker not found)")

# 2. Fastest withdrawal: Big Bass Bonanza game image. Find a good insertion point.
path = os.path.join(PUB, "fastest-withdrawal-casinos-australia-under-1-hour-2026.html")
txt = open(path, encoding="utf-8").read()
if "inline-figure" not in txt:
    # insert right before the FAQ section
    marker = '<span class="section-title__label">FAQ</span>'
    fig = (
        '<figure class="inline-figure">\n'
        '<img alt="Big Bass Bonanza pokie game fast to play and fast to cash out" decoding="async" height="300" loading="lazy" src="/assets/games/big-bass-bonanza.webp" width="400"/>\n'
        '<figcaption>Big Bass Bonanza - reel in the wins, cash out in under an hour at a verified operator</figcaption>\n'
        '</figure>\n'
    )
    idx = txt.find(marker)
    # find the start of the <section> that contains FAQ marker
    sec_start = txt.rfind("<section", 0, idx)
    if sec_start != -1:
        txt = txt[:sec_start] + fig + "\n" + txt[sec_start:]
        open(path, "w", encoding="utf-8").write(txt)
        print("ADDED fastest-withdrawal inline-figure")
    else:
        print("fastest-withdrawal: no section before FAQ")
else:
    print("fastest-withdrawal: already has inline-figure")

# 3. Mobile: Starburst game image
path = os.path.join(PUB, "mobile-pokies-australia-2026.html")
txt = open(path, encoding="utf-8").read()
if "inline-figure" not in txt:
    marker = '<span class="section-title__label">FAQ</span>'
    fig = (
        '<figure class="inline-figure">\n'
        '<img alt="Starburst pokie game playing on mobile phone browser" decoding="async" height="300" loading="lazy" src="/assets/games/starburst.webp" width="400"/>\n'
        '<figcaption>Starburst plays flawlessly in any mobile browser on iPhone or Android</figcaption>\n'
        '</figure>\n'
    )
    idx = txt.find(marker)
    sec_start = txt.rfind("<section", 0, idx)
    if sec_start != -1:
        txt = txt[:sec_start] + fig + "\n" + txt[sec_start:]
        open(path, "w", encoding="utf-8").write(txt)
        print("ADDED mobile inline-figure")
    else:
        print("mobile: no section before FAQ")
else:
    print("mobile: already has inline-figure")

print("DONE")
