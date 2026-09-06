"""Remove duplicate RG banner asides added by a content agent."""
import re
from pathlib import Path

BASE = Path(r"C:\Users\User\Documents\GitHub\Australia igaming website\public")

# Pattern: a second <aside aria-label="Responsible gambling notice" ...>...</aside>
# possibly wrapped in <div class="container">...</div>
PATTERN = re.compile(
    r'\s*<div class="container">\s*'
    r'<aside aria-label="Responsible gambling notice" class="rg-banner" role="note">.*?</aside>\s*'
    r'</div>\s*',
    re.DOTALL,
)

files = list(BASE.rglob("*.html"))
fixed = []
for f in files:
    txt = f.read_text(encoding="utf-8")
    if 'aria-label="Responsible gambling notice"' in txt:
        new_txt, n = PATTERN.subn("\n", txt)
        if n:
            f.write_text(new_txt, encoding="utf-8")
            fixed.append((f.relative_to(BASE).as_posix(), n))

for path, n in fixed:
    print(f"Fixed {path}: removed {n} duplicate RG block(s)")
print(f"\nTotal files fixed: {len(fixed)}")
