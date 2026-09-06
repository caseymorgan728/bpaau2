#!/usr/bin/env python3
"""Add standalone Organization JSON-LD to pages missing top-level Organization."""
import io, os

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"
ORG = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization",'
       '"name":"BPAAU","url":"https://bpaau.org/","logo":"https://bpaau.org/assets/logo.png"}</script>')

for fn in ["methodology.html", "research.html", "press.html"]:
    p = os.path.join(PUB, fn)
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        c = f.read()
    # Check if standalone BPAAU Organization already present
    needle = '"@type":"Organization","name":"BPAAU","url":"https://bpaau.org/","logo"'
    if needle in c:
        print(fn + ": already has standalone Org")
        continue
    marker = '<link rel="stylesheet" href="/assets/theme.css"/>'
    if marker in c:
        c = c.replace(marker, ORG + marker, 1)
    else:
        c = c.replace("</head>", ORG + "</head>", 1)
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(c)
    print(fn + ": Org added")
