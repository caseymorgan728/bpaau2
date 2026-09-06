import os, re
from collections import defaultdict
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"
files=[]
for dp,dn,fn in os.walk(PUB):
    for f in fn:
        if f.endswith(".html") and f!="google6c4a857337176f53.html":
            files.append(os.path.relpath(os.path.join(dp,f),PUB).replace("\\","/"))

def slug_of(rel):
    if rel=="index.html": return "/"
    if rel.endswith("index.html"):
        return "/"+rel[:-len("index.html")].strip("/")
    return "/"+rel[:-5]  # strip .html

# map target slug -> set of source files linking to it
inlinks=defaultdict(set)
for rel in files:
    h=open(os.path.join(PUB,rel),encoding="utf-8").read()
    for m in re.finditer(r'href="([^"]+)"',h):
        u=m.group(1)
        if u.startswith("https://bpaau.org"):
            path=u.replace("https://bpaau.org","")
        elif u.startswith("/"):
            path=u.split("#")[0].split("?")[0]
        else:
            continue
        if path=="" : path="/"
        inlinks[path].add(rel)

new_pages = [
 "online-pokies-legality-australia-2026","curacao-casino-licence-check-australia-2026",
 "how-to-play-online-pokies-beginners-australia-2026","no-wagering-bonuses-australia-2026",
 "cashback-bonus-pokies-australia-2026","mobile-pokies-australia-2026",
 "best-payment-methods-pokies-australia-2026","fastest-withdrawal-casinos-australia-under-1-hour-2026",
 "progressive-jackpot-pokies-australia-2026","vip-loyalty-programs-pokies-australia-2026",
 "best-high-rtp-pokies-australia-2026",
]
print("Inbound internal links to newer pages:")
for pg in new_pages:
    srcs=inlinks.get("/"+pg,set())
    flag="OK" if len(srcs)>=3 else "LOW"
    print(f"  [{flag}] /{pg}: {len(srcs)} inlinks")
