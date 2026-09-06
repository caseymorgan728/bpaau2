# -*- coding: utf-8 -*-
import re, json
files = [
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\blog\index.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\curacao-casino-licence-check-australia-2026.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\fastest-withdrawal-casinos-australia-under-1-hour-2026.html",
    r"C:\Users\User\Documents\GitHub\Australia igaming website\public\mobile-pokies-australia-2026.html",
]
for f in files:
    txt = open(f, encoding="utf-8").read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S)
    print("====", f.split("\\")[-1], "blocks:", len(blocks))
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
        except Exception as e:
            print("  BAD block", i, ":", str(e))
            m = re.search(r"column (\d+)", str(e))
            if m:
                col = int(m.group(1)) - 1
                print("  CONTEXT:", repr(b[max(0, col-80):col+80]))
