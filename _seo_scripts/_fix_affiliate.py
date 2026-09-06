import os
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"
old = 'href="https://1xaud.com/"'
new = 'href="https://1xaud.com/register"'
for fn in ["best-high-rtp-pokies-australia-2026.html","top-10-easiest-profit-pokies-2026.html"]:
    p = os.path.join(PUB, fn)
    s = open(p, encoding="utf-8").read()
    n = s.count(old)
    s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    print(f"{fn}: fixed {n} anchors")
