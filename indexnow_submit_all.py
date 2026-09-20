import json
import urllib.request
import re

sitemap_path = r"C:\Users\User\Documents\GitHub\bpaau2\public\sitemap.xml"
key = "2a26c0db7a064e869c594ce3c5ae14f0"

with open(sitemap_path, "r", encoding="utf-8") as f:
    content = f.read()

urls = [m.group(1) for m in re.finditer(r"<loc>(.*?)</loc>", content)]
print("URLs in sitemap:", len(urls))

# Batch in chunks of 1000
chunks = [urls[i : i + 1000] for i in range(0, len(urls), 1000)]
for chunk in chunks:
    payload = json.dumps(
        {"host": "bpaau.org", "key": key, "urlList": chunk}
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print("HTTP", resp.status, "for chunk of", len(chunk))
    except urllib.error.HTTPError as e:
        print("HTTPError", e.code, e.read().decode(errors="ignore")[:200], "chunk", len(chunk))
    except Exception as e:
        print("Error:", e)
