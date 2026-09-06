"""Quick accessibility (WCAG 2.2 AA) sweep across all pages."""
import os, re
from bs4 import BeautifulSoup

PUB = r"C:\Users\User\Documents\GitHub\Australia igaming website\public"

issues = []
for dirpath, dirnames, filenames in os.walk(PUB):
    dirnames[:] = [d for d in dirnames if not d.startswith("_img_backup_")]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, PUB).replace("\\", "/")
        if rel.startswith("google"):
            continue
        c = open(full, encoding="utf-8").read()
        soup = BeautifulSoup(c, "html.parser")

        # 1. Skip link
        if not soup.find("a", class_="skip-link") and "skip to content" not in c.lower() and "skip-to-content" not in c.lower():
            issues.append(f"{rel}: NO_SKIP_LINK")

        # 2. Buttons with no accessible name
        for btn in soup.find_all("button"):
            txt = btn.get_text(strip=True)
            aria_label = btn.get("aria-label", "")
            if not txt and not aria_label:
                issues.append(f"{rel}: BUTTON_NO_NAME (class={btn.get('class')})")

        # 3. aria-expanded on accordion triggers
        triggers = soup.find_all(class_=re.compile(r"acc__trigger"))
        for t in triggers:
            if not t.get("aria-expanded"):
                issues.append(f"{rel}: ACC_TRIGGER_NO_ARIA_EXPANDED")
                break

        # 4. Images with empty alt (decorative should have alt="", meaningful should have text)
        for img in soup.find_all("img"):
            alt = img.get("alt")
            if alt is None:
                issues.append(f"{rel}: IMG_MISSING_ALT_ATTR src={img.get('src','')[:50]}")

        # 5. Lang attribute
        html = soup.find("html")
        if html and not html.get("lang"):
            issues.append(f"{rel}: NO_LANG_ATTR")

for i in issues:
    print(i)
print(f"\nTotal accessibility issues: {len(issues)}")
