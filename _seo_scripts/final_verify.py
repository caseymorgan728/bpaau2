import os, re, glob
ROOT = "public"
files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
files = [f for f in files if "google" not in f]

PROTECTED = ["1xaud.com/register","gd8au.com/register","mrblueyau.com/register",
             "toystory9au.com/register","garcat8.com/register","1xaceau.com/register"]
issues = {"viewport-fit":0,"id=top":0,"backdrop":0,"cta":0,"btt":0,"18banner":0,"cta-not-1xaud":0}
cta_link_ok = 0
prod_ok = 0
for f in files:
    raw = open(f, encoding="utf-8").read()
    if "viewport-fit=cover" not in raw: issues["viewport-fit"]+=1
    if 'id="top"' not in raw: issues["id=top"]+=1
    if "nav-backdrop" not in raw: issues["backdrop"]+=1
    if "mobile-cta" not in raw: issues["cta"]+=1
    if "back-to-top" not in raw: issues["btt"]+=1
    if "18+" not in raw and "18 plus" not in raw.lower(): issues["18banner"]+=1
    # CTA must point to 1XAUD with correct rel
    if 'class="mobile-cta"' in raw:
        m = re.search(r'class="mobile-cta">.*?</div>', raw, re.S)
        seg = m.group(0) if m else ""
        if "1xaud.com/register" in seg and 'rel="sponsored nofollow noopener"' in seg and 'target="_blank"' in seg:
            cta_link_ok += 1
        else:
            issues["cta-not-1xaud"] += 1
    # all 6 protected links present on pages that have a product grid
    if "product-grid" in raw:
        if all(p in raw for p in PROTECTED):
            prod_ok += 1
        else:
            print("  !! missing protected link in", f)

print("Pages checked:", len(files))
print("Remaining issues:", {k:v for k,v in issues.items() if v})
print("Mobile CTA correctly wired to 1XAUD:", cta_link_ok, "/", len(files))
print("Pages with product-grid where all 6 protected links intact:", prod_ok)
print("OK" if all(v==0 for v in issues.values()) and cta_link_ok==len(files) else "CHECK ABOVE")
