"""Check internal inbound links to each of the 10 new pages."""
import os, re
from bs4 import BeautifulSoup

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

NEW_PAGES = [
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

# Collect all inbound links
inbound = {slug: [] for slug in NEW_PAGES}
all_pages = []
for dirpath, dirnames, filenames in os.walk(PUB):
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, PUB).replace("\\", "/")
        c = open(full, encoding="utf-8").read()
        all_pages.append(rel)
        for slug in NEW_PAGES:
            if f"/{slug}" in c:
                inbound[slug].append(rel)

for slug in NEW_PAGES:
    print(f"\n/{slug}")
    for src in inbound[slug]:
        print(f"  <- {src}")
    print(f"  Total inbound: {len(inbound[slug])}")
