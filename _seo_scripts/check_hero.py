"""Check hero/above-the-fold images on all content pages for fetchpriority/loading."""
import os, re, glob

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

issues = []
for dirpath, dirnames, filenames in os.walk(PUB):
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, PUB).replace("\\", "/")
        c = open(full, encoding="utf-8").read()
        # Find all imgs
        imgs = re.findall(r"<img[^>]*>", c)
        if not imgs:
            continue
        first = imgs[0]
        # Check if it's a hero (large banner)
        src = re.search(r'src="([^"]+)"', first)
        loading = re.search(r'loading="([^"]+)"', first)
        fp = re.search(r'fetchpriority="([^"]+)"', first)
        is_hero = src and ("banner" in (src.group(1).lower()) or "blogpost" in (src.group(1).lower()) or "banners" in (src.group(1).lower()))
        if is_hero:
            load_val = loading.group(1) if loading else "none"
            fp_val = fp.group(1) if fp else "none"
            if load_val not in ("eager", "auto"):
                issues.append(f"{rel}: hero img loading={load_val} (should be eager/auto)")
            if fp_val != "high":
                issues.append(f"{rel}: hero img fetchpriority={fp_val} (should be high)")

for i in issues:
    print(i)
print(f"\nTotal hero image issues: {len(issues)}")
