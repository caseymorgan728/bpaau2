import re, os

base = r"C:\Users\User\Documents\GitHub\bpaau2\public"
files = [
    "mobile-pokies-australia-2026.html",
    "progressive-jackpot-pokies-australia-2026.html",
    "best-payment-methods-pokies-australia-2026.html",
    "vip-loyalty-programs-pokies-australia-2026.html",
]
for f in files:
    with open(os.path.join(base, f), encoding="utf-8") as fh:
        html = fh.read()
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    body_words = re.sub(r"<[^>]+>", " ", html)
    body_words = len([w for w in re.split(r"\s+", body_words) if w.strip()])
    print(f)
    print("  H1:", h1[0].strip()[:80] if h1 else "NONE")
    print("  BODY_WORDS:", body_words)
    # check key terms presence
    key = {
        "mobile-pokies-australia-2026.html": "mobile",
        "progressive-jackpot-pokies-australia-2026.html": "jackpot",
        "best-payment-methods-pokies-australia-2026.html": "PayID",
        "vip-loyalty-programs-pokies-australia-2026.html": "VIP",
    }[f]
    print("  HAS_KEY('" + key + "'):", key.lower() in html.lower())
