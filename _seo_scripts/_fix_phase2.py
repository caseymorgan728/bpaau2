import os
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

# Map of broken OG image URL -> replacement (real existing images)
og_fixes = {
    "about.html": {
        "https://bpaau.org/assets/banners/about.jpg": "https://bpaau.org/assets/sections/about-editorial-team.webp",
    },
    "methodology.html": {
        "https://bpaau.org/assets/banners/methodology.jpg": "https://bpaau.org/assets/sections/methodology-research.webp",
    },
    "press.html": {
        "https://bpaau.org/assets/banners/press.jpg": "https://bpaau.org/assets/hero/main-hero.webp",
    },
    "research.html": {
        "https://bpaau.org/assets/banners/research.jpg": "https://bpaau.org/assets/sections/methodology-research.webp",
    },
}

changes = []
for fn, mapping in og_fixes.items():
    p = os.path.join(PUB, fn)
    s = open(p, encoding="utf-8").read()
    for old, new in mapping.items():
        n = s.count(old)
        s = s.replace(old, new)
        changes.append(f"{fn}: og:image {old} -> {new}  ({n} occurrences)")
    open(p, "w", encoding="utf-8").write(s)

# Fix green chilli typo
p = os.path.join(PUB, "best-high-rtp-pokies-australia-2026.html")
s = open(p, encoding="utf-8").read()
old = "assets/blog%20logo/green%20chilli.jpg"
new = "assets/blog%20logo/green%20chili.jpg"
n = s.count(old)
s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
changes.append(f"best-high-rtp...html: {old} -> {new} ({n} occurrences)")

for c in changes:
    print(c)
print("TOTAL FILES TOUCHED:", len(set(c.split(':')[0] for c in changes)))
