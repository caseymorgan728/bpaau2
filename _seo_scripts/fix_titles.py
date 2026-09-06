#!/usr/bin/env python3
"""Shorten titles to <=60 chars and fix duplicate / homepage meta issues."""
import os, re
from bs4 import BeautifulSoup

PUB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

NEW_TITLES = {
    "index.html": "Best Pokies Australia 2026 | Free Bonus & Fast Payouts",
    "ausmegaways-review.html": "AusMegaways44 Review | Free Spins AU 2026",
    "best-bonus-types-australian-pokies-2026.html": "Best Bonus Types Aussie Pokies 2026 | Chips & Spins",
    "best-high-rtp-pokies-australia-2026.html": "Best High-RTP Pokies Australia 2026 | 96%+ Slots",
    "bestrtp-review.html": "BestRTP44 Aus Review | High-RTP Pokies 2026",
    "biggest-casino-wins-australia-2026.html": "Biggest Casino Wins Australia 2026 | Verified Payouts",
    "daily-free-credits-au-returning-players.html": "Daily Free Credits AU 2026 | Reload Bonuses",
    "free-chips-australia-guide-2026.html": "Free Chips Australia 2026 | No-Deposit Guide",
    "freecredit777-review.html": "FreeCredit777 Aus Review | Daily Reload Credits",
    "high-volatility-vs-high-rtp-free-spins.html": "High Volatility vs High RTP Free Spins 2026",
    "hold-and-win-pokies-australia-2026.html": "Hold & Win Pokies Australia 2026 | RTP & Strategy",
    "hot-pokies-australia-2026-popular-slots.html": "Hot Pokies Australia 2026 | Most Played Slots",
    "how-to-read-casino-bonus-terms-australia-2026.html": "How to Read Casino Bonus Terms AU 2026",
    "methodology.html": "Testing Methodology | How We Test Pokies Sites",
    "no-deposit-free-bonus-guide-australia-2026.html": "No-Deposit Bonus Guide Australia 2026",
    "nodepspin-review.html": "NoDepSpin22 Review | 77 Free Spins AU 2026",
    "payid-cashouts-australia-2026.html": "PayID Cashouts Australia 2026 | Real Times Tested",
    "payid-withdraw-review.html": "PayIDWithdraw44 Review | Fast PayID AU 2026",
    "research.html": "Research & Data | Pokies Industry Research AU",
    "responsible-gambling.html": "Responsible Gambling | Help & Support AU 2026",
    "same-day-pokies-withdrawals-australia.html": "Same-Day Pokies Withdrawals Australia 2026",
    # Fix duplicate: fastest-withdrawal had same title as same-day
    "fastest-withdrawal-casinos-australia-under-1-hour-2026.html": "Fastest Withdrawal Casinos Australia Under 1 Hour",
}

NEW_DESCS = {
    "index.html": "Australia's independent, Gaming Curacao-verified pokies comparison for 2026. Free no-deposit bonuses, PayID fast payouts and high-RTP slots from six trusted operators. 18+.",
}

def fix(rel):
    fp = os.path.join(PUB, rel.replace("/", os.sep))
    with open(fp, "r", encoding="utf-8") as f:
        raw = f.read()
    soup = BeautifulSoup(raw, "html.parser")
    changed = False

    if rel in NEW_TITLES:
        new_title = NEW_TITLES[rel]
        if soup.title:
            soup.title.string = new_title
        # Also update og:title and twitter:title
        for tag in soup.find_all("meta", attrs={"property": "og:title"}):
            tag["content"] = new_title
        for tag in soup.find_all("meta", attrs={"name": "twitter:title"}):
            tag["content"] = new_title
        changed = True

    if rel in NEW_DESCS:
        new_desc = NEW_DESCS[rel]
        for tag in soup.find_all("meta", attrs={"name": "description"}):
            tag["content"] = new_desc
        for tag in soup.find_all("meta", attrs={"property": "og:description"}):
            tag["content"] = new_desc
        for tag in soup.find_all("meta", attrs={"name": "twitter:description"}):
            tag["content"] = new_desc
        changed = True

    if changed:
        out = str(soup)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"fixed {rel}")

for rel in list(NEW_TITLES.keys()) + list(NEW_DESCS.keys()):
    if os.path.exists(os.path.join(PUB, rel.replace("/", os.sep))):
        fix(rel)
