# -*- coding: utf-8 -*-
import urllib.request, os
url = "https://aka.doubaocdn.com/s/hS9w3MeNJU"
d = r"C:\Users\User\Documents\GitHub\bpaau2\public\assets\banners"
os.makedirs(d, exist_ok=True)
req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
data = urllib.request.urlopen(req, timeout=60).read()
# detect format
sig = data[:12]
if sig[:4] == b"RIFF" and sig[8:12] == b"WEBP":
    ext = "webp"
elif sig[:3] == b"\xff\xd8\xff":
    ext = "jpg"
elif sig[:8] == b"\x89PNG\r\n\x1a\n":
    ext = "png"
else:
    ext = "webp"
p = os.path.join(d, "small-free-chip-banner." + ext)
with open(p, "wb") as f:
    f.write(data)
print("saved", p, len(data), "bytes, ext", ext)
