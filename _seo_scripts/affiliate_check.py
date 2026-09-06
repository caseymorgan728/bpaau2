"""Verify 6 protected product affiliate links + rel attrs."""
import re, urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(r"C:\Users\User\Documents\GitHub\Australia igaming website\public")

PROTECTED = {
    "1XAUD": "1xaud.com/register",
    "GD8": "gd8au.com/register",
    "MR BLUEY": "mrblueyau.com/register",
    "TOY STORY 9": "toystory9au.com/register",
    "GARCAT8": "garcat8.com/register",
    "1XACE": "1xaceau.com/register",
}

# Find every external a href that contains one of the protected product hosts
host_to_name = {
    "1xaud.com": "1XAUD",
    "gd8au.com": "GD8",
    "mrblueyau.com": "MR BLUEY",
    "toystory9au.com": "TOY STORY 9",
    "garcat8.com": "GARCAT8",
    "1xaceau.com": "1XACE",
}

results = {name: {"present": 0, "correct": 0, "rel_ok": 0, "target_ok": 0, "links": []} for name in PROTECTED}
broken_internal = []
all_internal = 0
all_external = 0
all_imgs = 0
broken_imgs = []

def file_exists_for_url(url_path):
    p = url_path.split("#", 1)[0].split("?", 1)[0]
    p = urllib.parse.unquote(p)
    if p.startswith("/"):
        p = p[1:]
    if p == "":
        return (BASE / "index.html").exists()
    p_norm = p.rstrip("/")
    for c in [BASE / (p_norm + ".html"), BASE / p_norm / "index.html", BASE / p_norm]:
        if c.exists():
            return True
    return False

for f in sorted(BASE.rglob("*.html")):
    rel = f.relative_to(BASE).as_posix()
    soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            all_external += 1
            host = urllib.parse.urlparse(href).netloc.lower()
            for prod_host, prod_name in host_to_name.items():
                if prod_host in host:
                    results[prod_name]["present"] += 1
                    if PROTECTED[prod_name] in href:
                        results[prod_name]["correct"] += 1
                    else:
                        results[prod_name]["links"].append((rel, href))
                    rel_attr = a.get("rel") or []
                    if isinstance(rel_attr, str):
                        rel_attr = rel_attr.split()
                    rel_set = set(rel_attr)
                    if {"sponsored", "nofollow", "noopener"}.issubset(rel_set):
                        results[prod_name]["rel_ok"] += 1
                    else:
                        results[prod_name]["links"].append((rel, f"rel={rel_set}"))
                    if a.get("target") == "_blank":
                        results[prod_name]["target_ok"] += 1
                    else:
                        results[prod_name]["links"].append((rel, f"no target=_blank: {href}"))
        elif href.startswith(("/", "./", "../")) and not href.startswith(("mailto:", "tel:", "#", "data:", "javascript:")):
            all_internal += 1
            if not file_exists_for_url(href):
                broken_internal.append((rel, href))

    for img in soup.find_all("img"):
        all_imgs += 1
        src = img.get("src", "")
        if src.startswith(("http", "data:")):
            continue
        if not file_exists_for_url(src):
            broken_imgs.append((rel, src))

print("=" * 70)
print("PROTECTED PRODUCT AFFILIATE LINK VERIFICATION")
print("=" * 70)
for name, data in results.items():
    status = "OK" if (data["present"] > 0 and data["correct"] == data["present"] and data["rel_ok"] == data["present"] and data["target_ok"] == data["present"]) else "ISSUE"
    print(f"\n{name}: [{status}]")
    print(f"  occurrences: {data['present']}, correct URL: {data['correct']}, rel ok: {data['rel_ok']}, target ok: {data['target_ok']}")
    for r, d in data["links"]:
        print(f"    !! {r}: {d}")

print("\n" + "=" * 70)
print(f"INTERNAL LINKS: {all_internal} checked, {len(broken_internal)} broken")
print("=" * 70)
for r, h in broken_internal[:30]:
    print(f"  !! {r}: {h}")

print("\n" + "=" * 70)
print(f"IMAGES: {all_imgs} checked, {len(broken_imgs)} broken")
print("=" * 70)
for r, s in broken_imgs[:30]:
    print(f"  !! {r}: {s}")

print(f"\nTotal external links: {all_external}")
