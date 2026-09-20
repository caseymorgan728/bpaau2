import pathlib, re
d = pathlib.Path(r"C:\Users\User\Documents\GitHub\bpaau2\public")
s = (d/"pokies-tournaments-australia-2026.html").read_text(encoding="utf-8")
print("=== images referenced on tournaments page ===")
for m in re.findall(r'src="([^"]+\.(?:webp|jpg|png))"', s):
    print("  ", m)
print("=== candidate related pages: have blog-card-grid? ===")
cands = ["hot-pokies-australia-2026-popular-slots.html",
         "biggest-casino-wins-australia-pokies-2026.html",
         "progressive-jackpot-pokies-australia-2026.html",
         "vip-loyalty-programs-australia-pokies-2026.html",
         "daily-free-credit-pokies-australia-2026.html",
         "best-high-rtp-pokies-australia-2026.html"]
for c in cands:
    fp = d/c
    if fp.exists():
        t = fp.read_text(encoding="utf-8")
        print(f"  {c}: grid={'blog-card-grid' in t}, alreadyLinksTournament={'pokies-tournaments' in t}")
    else:
        print(f"  {c}: MISSING")
# list available blog banners
print("=== blog banner files ===")
bdir = d/"blog banner"
if bdir.exists():
    for f in sorted(bdir.glob("*.webp")):
        print("  ", f.name)
