#!/usr/bin/env python3
"""Verify button rule: generic Play Now/Spin to Win -> bpaau.com, product buttons -> register URLs."""
import os
from bs4 import BeautifulSoup

PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
pages = ['1xaud-review.html','gd8-review.html','mrbluey-review.html',
         '1xace-review.html','garcat8-review.html','toystory9-review.html']
affiliate_domains = ['1xaud.com','gd8au.com','mrblueyau.com','toystory9au.com','garcat8.com','1xaceau.com']

for p in pages:
    with open(os.path.join(PUB, p), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    buttons = soup.find_all('a', class_='btn')
    issues = []
    for b in buttons:
        text = b.get_text(strip=True)
        href = b.get('href', '')
        rel = ' '.join(b.get('rel', [])) if b.get('rel') else ''
        target = b.get('target', '')
        is_generic = text in ('Play Now', 'Spin to Win')
        is_product = any(d in href for d in affiliate_domains)
        if is_generic and href != 'https://bpaau.com':
            issues.append(f'GENERIC_BAD_HREF: "{text}" -> {href}')
        if is_generic and ('sponsored' not in rel or 'nofollow' not in rel or 'noopener' not in rel):
            issues.append(f'GENERIC_BAD_REL: "{text}" rel={rel}')
        if is_product and ('sponsored' not in rel or 'nofollow' not in rel or 'noopener' not in rel or target != '_blank'):
            issues.append(f'PRODUCT_BAD: "{text}" -> {href} rel={rel} target={target}')
    status = 'PASS' if not issues else 'FAIL: ' + '; '.join(issues)
    print(f'{p:30s} buttons={len(buttons):2d}  {status}')
