"""Fix homepage Latest Guides card image mappings."""
path = r'C:\Users\User\Documents\GitHub\Australia igaming website\public\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Each card has unique alt text. Match full img tag and replace src.
fixes = [
    # Card 1: Legality -> use the generated legality banner
    ('alt="Are online pokies legal in Australia" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 12.webp"',
     'alt="Are online pokies legal in Australia" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/pokies-legality-banner.webp"'),
    # Card 2: No Deposit -> blogpost 12 is "No Deposit Bonus" (correct topic)
    ('alt="No deposit free bonus guide Australia" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/pokies-legality-banner.webp"',
     'alt="No deposit free bonus guide Australia" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 12.webp"'),
    # Card 3: PayID -> blogpost 13 is "Payid Cashouts" (correct topic)
    ('alt="PayID cashouts Australia" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/pokies-legality-banner.webp"',
     'alt="PayID cashouts Australia" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 13.webp"'),
    # Card 4: Curacao -> generated curacao banner
    ('alt="Curacao casino licence check" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 12.webp"',
     'alt="Curacao casino licence check" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/curacao-licence-check-banner.webp"'),
    # Card 5: High-RTP -> blogpost 1 is "Best High RTP Pokies Aus" (correct topic)
    ('alt="Best high RTP pokies Australia" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 13.webp"',
     'alt="Best high RTP pokies Australia" decoding="async" height="360" loading="lazy" src="/blog banner/blogpost 1.webp"'),
    # Card 6: Mobile -> generated mobile banner
    ('alt="Mobile pokies Australia" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/curacao-licence-check-banner.webp"',
     'alt="Mobile pokies Australia" decoding="async" height="360" loading="lazy" src="/assets/blog-banners/mobile-pokies-banner.webp"'),
]

count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print('FIXED card', count)
    else:
        print('NOT FOUND:', old[:60])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print()
print('Homepage cards fixed:', count, '/ 6')
