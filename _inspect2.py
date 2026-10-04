# -*- coding: utf-8 -*-
import io, os, re
os.chdir(os.path.join(os.path.dirname(__file__), "public"))
h = io.open("index.html", encoding="utf-8").read()
i = h.find("blog-card-grid")
print("=== HOME grid inner (first) ===")
print(h[i:i+500])
print()
leg = io.open("online-pokies-legality-australia-2026.html", encoding="utf-8").read()
print("=== LEGALITY mentions ===")
for kw in ["Aristocrat", "social casino", "social casinos", "land-based", "Lightning", "clubs"]:
    print(kw, "->", leg.count(kw))
print("=== LEGALITY tail around main close ===")
j = leg.find("</main>")
print(leg[j-400:j+60])
