# -*- coding: utf-8 -*-
import urllib.request, re, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0 Safari/537.36"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8","ignore")
    except Exception as e:
        return "ERR:"+str(e), ""
st, body = fetch("https://bpaau.org/sitemap.xml")
print("sitemap", st, "loc count:", body.count("<loc>"))
for slug in sys.argv[1:]:
    st, body = fetch("https://bpaau.org/"+slug)
    m = re.search(r"<title>(.*?)</title>", body, re.S)
    print(st, slug, "|", (m.group(1)[:70] if m else ""))
