import re, os, glob
from collections import Counter

base = r"C:\Users\User\Documents\GitHub\bpaau2\public"
files = sorted(glob.glob(os.path.join(base, "*.html")))
titles = {}
for f in files:
    name = os.path.basename(f)
    with open(f, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = m.group(1).strip() if m else "NO TITLE"
    titles[name] = t

# find duplicates
counts = Counter(titles.values())
print("=== DUPLICATE TITLES ===")
for t, c in counts.items():
    if c > 1:
        print(f"[{c}x] {t}")
        for n, tt in titles.items():
            if tt == t:
                print("   ", n)

print()
print("=== ALL TITLES (length check) ===")
for n, t in sorted(titles.items()):
    flag = "OVER60" if len(t) > 60 else ""
    print(f"{len(t):3d} {flag:7s} {n[:70]:70s} -> {t[:90]}")
