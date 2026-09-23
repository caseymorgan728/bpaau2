# -*- coding: utf-8 -*-
import io
p = r"C:\Users\User\Documents\GitHub\bpaau2\public\10-20-25-free-chip-no-deposit-australia-2026.html"
s = io.open(p, encoding="utf-8").read()
if 'class="page-banner"' in s:
    print("banner already present")
else:
    fig = ('<figure class="page-banner"><img src="/assets/banners/small-free-chip-banner.jpg" '
           'alt="$10, $20 and $25 no-deposit free chip for Australian pokies 2026" '
           'width="3138" height="1336" loading="eager" decoding="async" fetchpriority="high"/></figure>\n')
    i = s.find("<h1>")
    if i < 0:
        raise SystemExit("no h1")
    s = s[:i] + fig + s[i:]
    io.open(p, "w", encoding="utf-8").write(s)
    print("banner inserted before h1")
