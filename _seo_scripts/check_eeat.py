#!/usr/bin/env python3
"""Verify expanded E-E-A-T dimensions across all 6 pages."""
import os, re
from bs4 import BeautifulSoup

PUB = r"C:\Users\User\Documents\GitHub\bpaau2\public"
pages = ['1xaud-review.html','gd8-review.html','mrbluey-review.html',
         '1xace-review.html','garcat8-review.html','toystory9-review.html']

for p in pages:
    with open(os.path.join(PUB, p), 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    main_text = main.get_text(' ', strip=True) if main else ''
    body_text = soup.get_text(' ', strip=True)

    has_byline = 'Reviewed by' in main_text[:2000]
    has_updated = 'Last updated' in main_text[:2000]
    has_readtime = 'Reading time' in main_text[:2000]
    has_source = 'verified by the BPAAU editorial team' in main_text
    body_links = [a.get('href','') for a in main.find_all('a', href=True)] if main else []
    has_method_body = any('methodology' in l for l in body_links)
    has_2026 = '2026' in main_text
    has_iga = 'Interactive Gambling Act' in body_text
    internal_texts = [a.get_text(strip=True).lower() for a in main.find_all('a', href=True) if a.get('href','').startswith('/')] if main else []
    unique_texts = len(set(internal_texts))
    generic = sum(1 for t in internal_texts if t in ('click here','read more','here','learn more'))
    diverse = unique_texts >= 8 and generic == 0

    checks = [has_byline, has_updated, has_readtime, has_source, has_method_body, has_2026, has_iga, diverse]
    status = "ALL PASS" if all(checks) else "GAPS: " + ",".join(
        [n for n, v in zip(['byline','updated','readtime','source','method','2026','iga','diverse'], checks) if not v])
    print(f"{p:30s} {' '.join(str(int(c)) for c in checks)}  {status}")

print("\nKey: byline updated readtime source methodology 2026 iga diverse_anchors")
