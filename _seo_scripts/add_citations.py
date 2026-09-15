#!/usr/bin/env python3
"""Add source citation to overview paragraph in pages missing it."""
import os
from bs4 import BeautifulSoup

PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"

# brand -> (official site, citation text)
CITATIONS = {
    "mrbluey-review.html": "All offer details, game names and payment information in this review are sourced from the official MR BLUEY website and verified by the BPAAU editorial team (September 2026).",
    "1xace-review.html": "All offer details, RTP percentages, game names and licence information in this review are sourced from the official 1XACE website and verified by the BPAAU editorial team (September 2026).",
    "toystory9-review.html": "All offer details, game names and payment information in this review are sourced from the official TOY STORY 9 website and verified by the BPAAU editorial team (September 2026).",
}

for filename, citation in CITATIONS.items():
    path = os.path.join(PUB, filename)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "verified by the BPAAU editorial team" in html:
        print(f"  {filename}: already has source citation, skipping")
        continue
    
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    
    # Find overview section
    overview_p = None
    for section in main.find_all("section", class_="section"):
        st = section.find("div", class_="section-title")
        if st and "overview" in st.get_text().lower():
            overview_p = section.find("p")
            break
    
    if not overview_p:
        print(f"  {filename}: ERROR - could not find overview paragraph")
        continue
    
    # Append citation
    overview_p.append(" " + citation)
    
    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    
    new_size = os.path.getsize(path)
    print(f"  {filename}: added source citation, new size {new_size:,} bytes")

print("\nDone.")
