import re
p = r"C:\Users\User\Documents\GitHub\Australia igaming website\public\press.html"
c = open(p, encoding="utf-8").read()
imgs = re.findall(r"<img[^>]*>", c)
for i, img in enumerate(imgs):
    src = re.search(r'src="([^"]+)"', img)
    loading = re.search(r'loading="([^"]+)"', img)
    alt = re.search(r'alt="([^"]*)"', img)
    print(i, src.group(1) if src else "?", "| loading=", loading.group(1) if loading else "NONE", "| alt=", (alt.group(1)[:40] if alt else "NONE"))
