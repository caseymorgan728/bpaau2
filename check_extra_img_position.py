# -*- coding: utf-8 -*-
import os, io, re, glob

BASE = r"C:\Users\User\Documents\GitHub\bpaau2\public"
files = ["about.html","best-payment-methods-pokies-australia-2026.html","cashback-bonus-pokies-australia-2026.html",
"curacao-casino-licence-check-australia-2026.html","fastest-withdrawal-casinos-australia-under-1-hour-2026.html",
"how-to-play-online-pokies-beginners-australia-2026.html","methodology.html","mobile-pokies-australia-2026.html",
"no-wagering-bonuses-australia-2026.html","online-pokies-legality-australia-2026.html",
"progressive-jackpot-pokies-australia-2026.html","vip-loyalty-programs-pokies-australia-2026.html"]

fig_pat = re.compile(r'<figure class="page-banner">.*?</figure>', re.S)
for f in files:
    s = io.open(os.path.join(BASE, f), encoding="utf-8", errors="replace").read()
    m = re.search(r'<section class="page-hero">(.*?)</section>', s, re.S)
    body = fig_pat.sub("", m.group(1))
    h1 = re.search(r"<h1[\s>]", body)
    lede = body.find('class="lede"')
    img = re.search(r"<img\b", body)
    src = re.search(r'<img[^>]*src="([^"]*)"', body)
    after = img.start() > (lede if lede > -1 else (h1.start() if h1 else -1))
    print(("BODY-OK " if after else "HEADER-ZONE! "), f, "->", src.group(1).split("/")[-1])
