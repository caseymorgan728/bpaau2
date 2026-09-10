import re, os

base = r"C:\Users\User\Documents\GitHub\bpaau2\public"
files = [
    "index.html",
    "best-high-rtp-pokies-australia-2026.html",
    "hold-and-win-pokies-australia-2026.html",
    "daily-free-credits-au-returning-players.html",
    "cashback-bonus-pokies-australia-2026.html",
    "payid-cashouts-australia-2026.html",
    "hot-pokies-australia-2026-popular-slots.html",
    "best-bonus-types-australian-pokies-2026.html",
    "mobile-pokies-australia-2026.html",
    "best-payment-methods-pokies-australia-2026.html",
    "progressive-jackpot-pokies-australia-2026.html",
    "vip-loyalty-programs-pokies-australia-2026.html",
]
for f in files:
    p = os.path.join(base, f)
    try:
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        md = re.search(r'name="description" content="(.*?)"', html, re.S)
        print(f)
        print("  T:", (m.group(1).strip()[:120] if m else "NO TITLE"))
        print("  D:", (md.group(1).strip()[:140] if md else "NO DESC"))
    except Exception as e:
        print(f, "ERR", e)
