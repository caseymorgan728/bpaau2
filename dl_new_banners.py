# -*- coding: utf-8 -*-
import io, os, urllib.request, struct

BANNERS = [
    ("free-100-no-deposit-bonus-australia-2026", "https://aka.doubaocdn.com/s/4T8bxISN1C"),
    ("free-spins-no-deposit-pokies-australia-2026", "https://aka.doubaocdn.com/s/DKWygrpQ7O"),
    ("10-payid-no-deposit-bonus-australia-2026", "https://aka.doubaocdn.com/s/VDnq25VIlw"),
    ("lightning-link-online-australia-legal", "https://aka.doubaocdn.com/s/ZDVsnrJwtP"),
    ("dragon-link-online-pokies-australia-legal", "https://aka.doubaocdn.com/s/1UdJcTE7FR"),
    ("big-bass-bonanza-pokies-australia-2026", "https://aka.doubaocdn.com/s/l3Dn2DJVWF"),
    ("sweet-bonanza-pokies-australia-2026", "https://aka.doubaocdn.com/s/gWmSUYK4Eh"),
]

OUT = os.path.join("public", "assets", "banners")

def jpeg_size(b):
    i = 2
    while i < len(b):
        if b[i] != 0xFF:
            i += 1; continue
        m = b[i+1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3):
            h = struct.unpack(">H", b[i+5:i+7])[0]
            w = struct.unpack(">H", b[i+7:i+9])[0]
            return w, h
        seg = struct.unpack(">H", b[i+2:i+4])[0]
        i += 2 + seg
    return None, None

hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
for slug, url in BANNERS:
    req = urllib.request.Request(url, headers=hdr)
    b = urllib.request.urlopen(req, timeout=60).read()
    assert b[:3] == b"\xff\xd8\xff", (slug, b[:8])
    w, h = jpeg_size(b)
    fp = os.path.join(OUT, slug + "-banner.jpg")
    with io.open(fp, "wb") as f:
        f.write(b)
    print(f"{slug:55s} {w}x{h} {len(b)//1024}KB")
print("done")
