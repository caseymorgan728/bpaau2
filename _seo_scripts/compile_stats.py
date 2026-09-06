import json
d = json.load(open(r'C:\Users\User\Documents\GitHub\Australia igaming website\_seo_scripts\audit_results.json', encoding='utf-8'))
print('Files:', d['files'])
print('CSS bytes:', d['css_size'])
print('Sitemap URLs:', d['sitemap_urls'])
content = [r for r in d['results'] if r['file'] not in ('404.html','google6c4a857337176f53.html')]
over800 = [r for r in content if r['words'] >= 800]
under800 = [r for r in content if r['words'] < 800]
print(f'Content pages: {len(content)}, >=800w: {len(over800)}, <800w: {len(under800)}')
for r in under800:
    print(f"  {r['words']}w  {r['file']}")
wcs = sorted([r['words'] for r in content])
print(f'Word count range: {wcs[0]} - {wcs[-1]}')
print(f'Average: {sum(wcs)//len(wcs)}')
titles = [r['title'] for r in content]
print(f'Unique titles: {len(set(titles))}/{len(titles)}')
long_titles = [r for r in content if r['title_len'] > 60]
print(f'Titles >60 chars: {len(long_titles)}')
for r in long_titles:
    print(f"  {r['title_len']}c  {r['file']}: {r['title'][:70]}")
h1_issues = [r for r in content if r['h1'] != 1]
print(f'Pages with !=1 H1: {len(h1_issues)}')
from collections import Counter
types = Counter()
for r in content:
    for t in r['jsonld_types']:
        types[t] += 1
print('JSON-LD types present:')
for t, c in types.most_common(20):
    print(f'  {t}: {c}')
# FAQ details count
faq_pages = [(r['file'], r['faq_details']) for r in content if r['faq_details'] > 0]
print(f'Pages with FAQ <details>: {len(faq_pages)}')
