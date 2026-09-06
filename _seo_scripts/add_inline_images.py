"""Add inline figures to 8 key pillar pages for SEO."""
import os

PUBLIC = r'C:\Users\User\Documents\GitHub\Australia igaming website\public'

# Each entry: (filename, anchor_text_to_find_paragraph, figure_html)
# The figure is inserted AFTER the paragraph containing the anchor text.

pages = [
    {
        'file': 'best-high-rtp-pokies-australia-2026.html',
        'anchor': 'RTP stands for Return to Player',
        'img_src': '/assets/games/mega-ace.webp',
        'img_alt': 'Mega Ace pokie game — 97% RTP, one of the highest-return pokies for Australian players',
        'caption': 'Mega Ace (JILI) — 97% RTP, a top high-return pokie',
        'width': 400, 'height': 300,
    },
    {
        'file': 'online-pokies-legality-australia-2026.html',
        'anchor': 'Interactive Gambling Act 2001',
        'img_src': '/assets/hero/curacao-verified.webp',
        'img_alt': 'Gaming Curacao licensed and verified online casino for Australian players',
        'caption': 'Gaming Curacao licensed operators are legally accessible to Aussie players',
        'width': 640, 'height': 360,
    },
    {
        'file': 'no-deposit-free-bonus-guide-australia-2026.html',
        'anchor': 'no deposit',
        'img_src': '/assets/games/sweet-bonanza.webp',
        'img_alt': 'Sweet Bonanza pokie — popular game for no-deposit free spins bonuses',
        'caption': 'Sweet Bonanza — a top pick for no-deposit free spin offers',
        'width': 400, 'height': 300,
    },
    {
        'file': 'payid-cashouts-australia-2026.html',
        'anchor': 'PayID',
        'img_src': '/assets/games/money-coming.webp',
        'img_alt': 'Money Coming pokie game — fast wins and fast PayID cashouts',
        'caption': 'Money Coming — win fast, cash out fast with PayID',
        'width': 400, 'height': 300,
    },
    {
        'file': 'mobile-pokies-australia-2026.html',
        'anchor': 'mobile',
        'img_src': '/assets/games/starburst.webp',
        'img_alt': 'Starburst pokie game playing on mobile phone browser',
        'caption': 'Starburst — plays flawlessly in any mobile browser',
        'width': 400, 'height': 300,
    },
    {
        'file': 'curacao-casino-licence-check-australia-2026.html',
        'anchor': 'Curacao',
        'img_src': '/assets/hero/curacao-verified.webp',
        'img_alt': 'Curacao casino licence verification check shield and badge',
        'caption': 'Verify any Gaming Curacao licence in the public registry',
        'width': 640, 'height': 360,
    },
    {
        'file': 'free-chips-australia-guide-2026.html',
        'anchor': 'free chips',
        'img_src': '/assets/games/green-chilli.webp',
        'img_alt': 'Green Chilli pokie game — popular free spins bonus game',
        'caption': 'Green Chilli — a hot free-spins pokie for your free chips',
        'width': 400, 'height': 300,
    },
    {
        'file': 'fastest-withdrawal-casinos-australia-under-1-hour-2026.html',
        'anchor': 'withdrawal',
        'img_src': '/assets/games/big-bass-bonanza.webp',
        'img_alt': 'Big Bass Bonanza pokie game — fast to play and fast to cash out',
        'caption': 'Big Bass Bonanza — reel in the wins, cash out in under an hour',
        'width': 400, 'height': 300,
    },
]

count = 0
for page in pages:
    filepath = os.path.join(PUBLIC, page['file'])
    if not os.path.exists(filepath):
        print(f'NOT FOUND: {page["file"]}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has inline-figure
    if 'inline-figure' in content:
        print(f'SKIP (already has figure): {page["file"]}')
        continue

    # Find the paragraph containing the anchor text
    anchor = page['anchor']
    # Find the <p>...</p> that contains the anchor
    import re
    # Match a paragraph that contains the anchor (case insensitive)
    pattern = r'(<p[^>]*>(?:(?!</p>).)*?' + re.escape(anchor) + r'(?:(?!</p>).)*?</p>)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if not match:
        # Try simpler: find first paragraph after the first H2
        h2_match = re.search(r'<h2[^>]*>.*?</h2>\s*(<p[^>]*>.*?</p>)', content, re.DOTALL)
        if h2_match:
            match = h2_match
        else:
            print(f'NO ANCHOR MATCH: {page["file"]}')
            continue

    para_end = match.end()

    figure = f'''
<figure class="inline-figure">
<img alt="{page['img_alt']}" decoding="async" height="{page['height']}" loading="lazy" src="{page['img_src']}" width="{page['width']}"/>
<figcaption>{page['caption']}</figcaption>
</figure>
'''

    content = content[:para_end] + figure + content[para_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    count += 1
    print(f'ADDED: {page["file"]}')

print(f'\nTotal pages with inline figures added: {count} / 8')
