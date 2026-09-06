# -*- coding: utf-8 -*-
import re, os, html, json

pages = [
 "best-high-rtp-pokies-australia-2026.html",
 "free-chips-australia-guide-2026.html",
 "payid-cashouts-australia-2026.html",
 "no-deposit-free-bonus-guide-australia-2026.html",
 "hold-and-win-pokies-australia-2026.html",
 "hot-pokies-australia-2026-popular-slots.html",
 "best-bonus-types-australian-pokies-2026.html",
 "daily-free-credits-au-returning-players.html",
 "biggest-casino-wins-australia-2026.html",
 "how-to-read-casino-bonus-terms-australia-2026.html",
 "high-volatility-vs-high-rtp-free-spins.html",
 "same-day-pokies-withdrawals-australia.html",
]
def strip(s):
    s=re.sub(r"<[^>]+>"," ",s); return html.unescape(s)

issues=0
for p in pages:
    s=open(os.path.join("public",p),encoding="utf-8").read()
    # meta
    dm=re.search(r'<meta content="([^"]*)" name="description"/>',s)
    dlen=len(dm.group(1)) if dm else 0
    # body words
    bm=re.search(r"<main[^>]*>(.*?)</main>",s,re.S)
    bw=len(strip(bm.group(1)).split()) if bm else 0
    # visible FAQs
    details=re.findall(r'<details class="faq">(.*?)</details>',s,re.S)
    thin=[]
    for d in details:
        b=re.search(r'<div class="faq__body">(.*?)</div>',d,re.S)
        w=len(strip(b.group(1)).split()) if b else 0
        if w<50: thin.append(w)
    # JSON-LD
    json_ok=True; faq_q=0; faq_ans_words=[]
    for jm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try:
            obj=json.loads(jm.group(1))
        except Exception as e:
            json_ok=False; continue
        if obj.get("@type")=="FAQPage":
            for ent in obj.get("mainEntity",[]):
                faq_q+=1
                t=ent.get("acceptedAnswer",{}).get("text","")
                faq_ans_words.append(len(t.split()))
    thin_json=[w for w in faq_ans_words if w<50]
    # products
    prods=len(re.findall(r'<article class="product-card">',s))
    # script count
    scripts=len(re.findall(r"<script",s))
    flags=[]
    if thin: flags.append(f"VIS_THIN{thin}")
    if thin_json: flags.append(f"JSON_THIN{thin_json}")
    if not json_ok: flags.append("JSON_BAD")
    if faq_q!=len(details): flags.append(f"MISMATCH visible={len(details)} ld={faq_q}")
    if bw<1000: flags.append("LT1000")
    if not (140<=dlen<=160): flags.append(f"DESC{dlen}")
    if prods!=6: flags.append(f"PROD{prods}")
    if flags: issues+=1
    print(f"{p}\n  desc={dlen} body={bw} faqs={len(details)}/{faq_q} prods={prods} scripts={scripts} {'  <<< '+' '.join(flags) if flags else 'OK'}")
print("\nPAGES WITH ISSUES:",issues)
