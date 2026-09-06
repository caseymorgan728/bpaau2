import os, re, json
from bs4 import BeautifulSoup
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

files=[]
for dp,dn,fn in os.walk(PUB):
    for f in fn:
        if f.endswith(".html") and f not in ("google6c4a857337176f53.html",):
            files.append(os.path.relpath(os.path.join(dp,f),PUB).replace("\\","/"))
files.sort()

imgs_no_dim=0; imgs_total=0; hero_no_fp=[]
no_breadcrumb=[]; no_title=[]; no_desc=[]
review_pages = ["freecredit777-review.html","megawin33-review.html","lockrespin-review.html",
                "ausmegaways-review.html","nodepspin-review.html","bestrtp-review.html","payid-withdraw-review.html"]
review_missing=[]
org_sameas=[]
font_swap=set()
lazy_missing=[]

for rel in files:
    h=open(os.path.join(PUB,rel),encoding="utf-8").read()
    soup=BeautifulSoup(h,"html.parser")
    # images
    for img in soup.find_all("img"):
        imgs_total+=1
        if not img.get("width") or not img.get("height"):
            imgs_no_dim+=1
    # breadcrumb JSON-LD
    has_bc = False
    has_review = False; has_agg = False; has_org=False
    for sc in soup.find_all("script",attrs={"type":"application/ld+json"}):
        try: data=json.loads(sc.string or "{}")
        except: continue
        items = data if isinstance(data,list) else [data]
        for it in items:
            t = it.get("@type")
            if t=="BreadcrumbList": has_bc=True
            if t=="Review": has_review=True
            if t=="AggregateRating": has_agg=True
            if t=="Organization":
                has_org=True
                if it.get("sameAs"): org_sameas.append(rel)
    if not has_bc: no_breadcrumb.append(rel)
    if rel in review_pages and not (has_review and has_agg):
        review_missing.append(rel)
    # font-display
    if "display=swap" in h or "display=swap" in h:
        font_swap.add(rel)

print("HTML pages:", len(files))
print("Total <img>:", imgs_total, "| missing width/height:", imgs_no_dim)
print("Pages WITHOUT BreadcrumbList:", len(no_breadcrumb))
for r in no_breadcrumb: print("   -", r)
print("Review pages missing Review/AggregateRating:", review_missing)
print("Pages with Organization+sameAs:", len(org_sameas))
print("Pages mentioning display=swap:", len(font_swap))
# google fonts link check
sample=open(os.path.join(PUB,"index.html"),encoding="utf-8").read()
print("\nGoogle fonts links:")
for m in re.finditer(r'href="(https://fonts\.googleapis[^"]+)"', sample):
    print("  ", m.group(1))
