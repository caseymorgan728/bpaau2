# -*- coding: utf-8 -*-
import re
files = [
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\blog\index.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\curacao-casino-licence-check-australia-2026.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\fastest-withdrawal-casinos-australia-under-1-hour-2026.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\mobile-pokies-australia-2026.html",
]
for f in files:
    txt = open(f, encoding="utf-8").read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S)
    print("====", f.split("\\")[-1])
    print(blocks[4])
    print("\n\n")
