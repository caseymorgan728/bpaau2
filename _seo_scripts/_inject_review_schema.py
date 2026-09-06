import os, json
PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

# review page -> (brand name, canonical, rating)
reviews = {
 "freecredit777-review.html": ("FreeCredit777 Aus", "https://bpaau.org/freecredit777-review", 4.6,
    "FreeCredit777 Aus is evaluated on daily free chips, no-deposit credits and PayID payout speed across multiple test rounds by BPAAU."),
 "megawin33-review.html": ("MegaWin33 AU", "https://bpaau.org/megawin33-review", 4.4,
    "MegaWin33 AU is tested for high-volatility big-win pokies, bonus differentiation and PayID cashout reliability by BPAAU."),
 "lockrespin-review.html": ("LockRespin88", "https://bpaau.org/lockrespin-review", 4.3,
    "LockRespin88 is reviewed on Hold & Win pokie mechanics, respin features and AU PayID withdrawals by BPAAU."),
 "ausmegaways-review.html": ("AusMegaways44", "https://bpaau.org/ausmegaways-review", 4.7,
    "AusMegaways44 is assessed on Megaways free spins, cascading reels, wagering terms and PayID cashouts by BPAAU."),
 "nodepspin-review.html": ("NoDepSpin22", "https://bpaau.org/nodepspin-review", 4.5,
    "NoDepSpin22 is tested on the 77 free spins no-deposit pack, play-through pacing and PayID withdrawal terms by BPAAU."),
 "bestrtp-review.html": ("BestRTP44 Aus", "https://bpaau.org/bestrtp-review", 4.6,
    "BestRTP44 Aus is evaluated on 96%+ RTP pokies, free chips no deposit and PayID withdrawals under a Gaming Curacao licence by BPAAU."),
 "payid-withdraw-review.html": ("PayIDWithdraw44", "https://bpaau.org/payid-withdraw-review", 4.8,
    "PayIDWithdraw44 is tested end-to-end on fast PayID cashouts, KYC speed and rejected-payout rates by BPAAU."),
}

def script_block(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=2) + "</script>\n"

for fn,(brand,canon,rating,body) in reviews.items():
    p=os.path.join(PUB,fn)
    h=open(p,encoding="utf-8").read()
    review_ld={
        "@context":"https://schema.org","@type":"Review",
        "itemReviewed":{"@type":"Organization","name":brand,"url":canon},
        "reviewBody":body,
        "reviewRating":{"@type":"Rating","ratingValue":str(rating),"bestRating":"5"},
        "author":{"@type":"Person","name":"Daniel Hart"},
        "publisher":{"@type":"Organization","name":"BPAAU","logo":{"@type":"ImageObject","url":"https://bpaau.org/assets/logo.png"}}
    }
    agg_ld={
        "@context":"https://schema.org","@type":"AggregateRating",
        "itemReviewed":{"@type":"Organization","name":brand,"url":canon},
        "ratingValue":str(rating),"bestRating":"5","reviewCount":"1"
    }
    inject = "\n" + script_block(review_ld) + script_block(agg_ld)
    # insert before </head>
    assert "</head>" in h
    h = h.replace("</head>", inject + "</head>", 1)
    open(p,"w",encoding="utf-8").write(h)
    print("review schema added:", fn, brand, rating)

# BreadcrumbList for index.html (Home)
p=os.path.join(PUB,"index.html")
h=open(p,encoding="utf-8").read()
bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://bpaau.org/"}]}
h=h.replace("</head>", "\n"+script_block(bc)+"</head>",1)
open(p,"w",encoding="utf-8").write(h)
print("breadcrumb added: index.html")

# BreadcrumbList for payid-cashouts
p=os.path.join(PUB,"payid-cashouts-australia-2026.html")
h=open(p,encoding="utf-8").read()
bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://bpaau.org/"},
    {"@type":"ListItem","position":2,"name":"PayID Cashouts Australia 2026","item":"https://bpaau.org/payid-cashouts-australia-2026"}]}
h=h.replace("</head>", "\n"+script_block(bc)+"</head>",1)
open(p,"w",encoding="utf-8").write(h)
print("breadcrumb added: payid-cashouts-australia-2026.html")
