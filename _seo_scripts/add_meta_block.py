#!/usr/bin/env python3
"""Insert E-E-A-T review-meta block after hero in all 6 brand review pages."""
import os, re

PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
PAGES = {
    "1xaud-review.html": 13,
    "gd8-review.html": 12,
    "mrbluey-review.html": 12,
    "1xace-review.html": 12,
    "garcat8-review.html": 13,
    "toystory9-review.html": 13,
}

META_BLOCK = '''<section class="section">
<div class="container"><p><strong>Reviewed by</strong> <a href="/about">BPAAU Editorial Team</a> &middot; <strong>Last updated:</strong> 15 September 2026 &middot; <strong>Reading time:</strong> {mins} min &middot; <a href="/methodology">How we review casinos</a></p></div>
</section>

'''

for filename, mins in PAGES.items():
    path = os.path.join(PUB, filename)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Check if already inserted
    if "Reviewed by" in html and "Reading time:" in html:
        print(f"  {filename}: already has meta block, skipping")
        continue
    
    # Find the end of page-hero section
    # Pattern: <section class="page-hero"> ... </section> followed by blank line and <section class="section">
    hero_end = html.find('</section>', html.find('page-hero'))
    if hero_end == -1:
        print(f"  {filename}: ERROR - could not find hero end")
        continue
    
    # Find the next section start after hero end
    next_section = html.find('<section class="section">', hero_end)
    if next_section == -1:
        print(f"  {filename}: ERROR - could not find next section")
        continue
    
    # Insert meta block between hero end and next section
    # The text between is typically "</section>\n\n"
    insert_point = html.find('\n', hero_end)  # end of </section> line
    # Find the blank line
    after_closing = html[hero_end:next_section]
    
    new_html = html[:hero_end + len('</section>')] + '\n\n' + META_BLOCK.format(mins=mins) + html[next_section:]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    new_size = os.path.getsize(path)
    print(f"  {filename}: inserted meta block ({mins} min read), new size {new_size:,} bytes")

print("\nDone.")
