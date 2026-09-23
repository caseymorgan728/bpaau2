# -*- coding: utf-8 -*-
import json, sys, urllib.request, os, io

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
BAN = os.path.join(BASE, "assets", "banners")
os.makedirs(BAN, exist_ok=True)

def jpeg_size(b):
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF:
            i += 1; continue
        m = b[i+1]
        if m in (0xC0,0xC1,0xC2,0xC3):
            h = (b[i+5] << 8) | b[i+6]
            w = (b[i+7] << 8) | b[i+8]
            return w, h
        ln = (b[i+2] << 8) | b[i+3]
        i += 2 + ln
    return 3138, 1336

items = json.load(io.open(sys.argv[1], encoding="utf-8"))
for it in items:
    slug, url, alt = it["slug"], it["url"], it["alt"]
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    sig = data[:12]
    if sig[:4] == b"RIFF" and sig[8:12] == b"WEBP": ext = "webp"
    elif sig[:3] == b"\xff\xd8\xff": ext = "jpg"
    elif sig[:8] == b"\x89PNG\r\n\x1a\n": ext = "png"
    else: ext = "jpg"
    w, h = jpeg_size(data) if ext == "jpg" else (3138, 1336)
    bname = slug + "-banner." + ext
    with open(os.path.join(BAN, bname), "wb") as f:
        f.write(data)
    hp = os.path.join(BASE, slug + ".html")
    s = io.open(hp, encoding="utf-8").read()
    if 'class="page-banner"' in s:
        print("skip (exists):", slug)
        continue
    fig = ('<figure class="page-banner"><img src="/assets/banners/%s" alt="%s" '
           'width="%d" height="%d" loading="eager" decoding="async" fetchpriority="high"/></figure>\n'
           % (bname, alt, w, h))
    i = s.find("<h1>")
    if i < 0:
        print("NO H1:", slug); continue
    s = s[:i] + fig + s[i:]
    io.open(hp, "w", encoding="utf-8").write(s)
    print("wired:", slug, w, h, len(data))
