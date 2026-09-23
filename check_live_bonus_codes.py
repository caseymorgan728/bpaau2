# -*- coding: utf-8 -*-
import urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0 Safari/537.36"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "ignore")
            return r.status, body
    except Exception as e:
        return "ERR:" + str(e), ""

for url in [
    "https://bpaau.org/no-deposit-bonus-codes-australia-2026",
    "https://bpaau.org/sitemap.xml",
]:
    st, body = fetch(url)
    extra = ""
    if st == 200:
        import re
        m = re.search(r"<title>(.*?)</title>", body, re.S)
        extra = (m.group(1) if m else "")[:70]
        if "sitemap" in url:
            extra = "loc count=%d, new url present=%s" % (
                body.count("<loc>"), "no-deposit-bonus-codes" in body)
    print(st, url, "|", extra)
