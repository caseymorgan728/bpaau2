import re, os

base = r"C:\Users\User\Documents\GitHub\bpaau2\public"

fixes = {
    "mobile-pokies-australia-2026.html": ("Mobile Pokies Australia 2026 | Play on Any Device", "Mobile pokies Australia 2026: no real-money App Store or Play Store apps, play in secure browser on iPhone and Android. Fast PayID deposits and withdrawals."),
    "progressive-jackpot-pokies-australia-2026.html": ("Progressive Jackpot Pokies Australia 2026 | Huge Pools", "Progressive jackpot pokies Australia 2026. How jackpots work, the big four (Mega Moolah, Divine Fortune), must-drop timers and operator pools compared."),
    "best-payment-methods-pokies-australia-2026.html": ("Best Payment Methods Pokies AU 2026 | PayID & Crypto", "Best deposit methods for pokies Australia 2026. PayID, Osko, POLi, Neosurf, BTC and USDT compared - fees, speed, AU bank acceptance and limits."),
    "vip-loyalty-programs-pokies-australia-2026.html": ("VIP Loyalty Programs Pokies Australia 2026 | Rewards", "VIP loyalty program online pokies Australia 2026. How comp points and tiers work, six operators compared, and whether playing for comps is worth it."),
}

for fname, (title, desc) in fixes.items():
    p = os.path.join(base, fname)
    with open(p, encoding="utf-8") as fh:
        html = fh.read()
    new_html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, flags=re.S)
    if re.search(r'name="description" content="', new_html):
        new_html = re.sub(r'name="description" content=".*?"', f'name="description" content="{desc}"', new_html, count=1)
    else:
        new_html = re.sub(r'(<meta charset="utf-8">)', r'\1\n    <meta name="description" content="%s">' % desc, new_html, count=1)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(new_html)
    # verify
    with open(p, encoding="utf-8") as fh:
        v = fh.read()
    m = re.search(r"<title>(.*?)</title>", v, re.S)
    md = re.search(r'name="description" content="(.*?)"', v, re.S)
    print(fname)
    print("  T:", m.group(1).strip())
    print("  D:", (md.group(1).strip()[:80] + "...") if md else "MISSING")
    print("  LEN:", len(m.group(1).strip()))
