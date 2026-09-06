import re, os
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"
PROTECTED = {
    "1xaud.com": "https://1xaud.com/register",
    "gd8au.com": "https://gd8au.com/register",
    "mrblueyau.com": "https://mrblueyau.com/register",
    "1xaceau.com": "https://1xaceau.com/register",
    "garcat8.com": "https://garcat8.com/register",
    "toystory9au.com": "https://toystory9au.com/register",
}
REL_OK = "sponsored nofollow noopener"

files=[]
for dp,dn,fn in os.walk(PUB):
    for f in fn:
        if f.endswith(".html"):
            files.append(os.path.join(dp,f))

bad=[]
total=0
for host, expected in PROTECTED.items():
    host_hits=0
    for fp in files:
        rel=os.path.relpath(fp,PUB).replace("\\","/")
        h=open(fp,encoding="utf-8").read()
        # find every anchor containing this host
        for m in re.finditer(r'<a\b[^>]*href="https?://(?:www\.)?'+re.escape(host)+r'[^"]*"[^>]*>', h):
            tag=m.group(0)
            host_hits+=1; total+=1
            href=re.search(r'href="([^"]+)"',tag).group(1)
            relattr=re.search(r'rel="([^"]*)"',tag)
            tgt=re.search(r'target="([^"]*)"',tag)
            relv=relattr.group(1) if relattr else ""
            tgtv=tgt.group(1) if tgt else ""
            issues=[]
            # href must be exactly the register url
            if href.rstrip("/") not in (expected,):
                issues.append(f"href={href}")
            if REL_OK not in relv:
                issues.append(f"rel={relv!r}")
            if tgtv!="_blank":
                issues.append(f"target={tgtv!r}")
            if issues:
                bad.append((rel,host,issues))
    print(f"{host}: {host_hits} anchor(s) across site")

print(f"\nTOTAL protected anchors: {total}")
print(f"ISSUES: {len(bad)}")
for rel,host,issues in bad:
    print(" ", rel,"|",host,"|", "; ".join(issues))
