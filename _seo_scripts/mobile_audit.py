#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mobile pre-flight audit across all public HTML files."""
import os, re, glob

ROOT = os.path.join(os.path.dirname(__file__), "..", "public")
ROOT = os.path.abspath(ROOT)

files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))

def rel(p):
    return os.path.relpath(p, ROOT)

print(f"Total HTML files: {len(files)}\n")
print(f"{'file':55} {'vpFit':5} {'lang':4} {'theme':5} {'bodyId':6} {'table':6} {'cta':4} {'btt':4} {'backdrop':8} {'nonLDscript'}")
print("-"*130)

issues = []
for f in files:
    name = rel(f)
    if "google" in name:
        continue
    raw = open(f, "r", encoding="utf-8").read()
    has_vp = 'name="viewport"' in raw or "name='viewport'" in raw or 'name="viewport"' in raw.replace('content=','')
    vp_fit = "viewport-fit=cover" in raw
    lang = bool(re.search(r'<html[^>]*lang=', raw))
    theme = 'name="theme-color"' in raw or "theme-color" in raw
    body_id = 'id="top"' in raw or "id='top'" in raw
    table = bool(re.search(r'<table', raw, re.I)) or "score-table" in raw
    cta = 'mobile-cta' in raw
    btt = 'back-to-top' in raw
    backdrop = 'nav-backdrop' in raw
    # non-json-ld scripts
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', raw, re.S|re.I)
    nonld = [s for s in scripts if 'ld+json' not in s and s.strip()!='']
    # also script tags with src
    script_src = re.findall(r'<script[^>]*\bsrc=', raw, re.I)
    flag = ""
    if nonld or script_src:
        flag = f"NONLD={len(nonld)} SRC={len(script_src)}"
    print(f"{name:55} {str(vp_fit):5} {str(lang):4} {str(theme):5} {str(body_id):6} {str(table):6} {str(cta):4} {str(btt):4} {str(backdrop):8} {flag}")
    if not vp_fit: issues.append((name,"no viewport-fit=cover"))
    if not body_id: issues.append((name,"no id=top on body"))
    if not cta: issues.append((name,"no mobile-cta"))
    if not btt: issues.append((name,"no back-to-top"))
    if not backdrop: issues.append((name,"no nav-backdrop"))
    if not lang: issues.append((name,"no lang"))
    if not theme: issues.append((name,"no theme-color"))

print("\n=== FILES WITH TABLES ===")
for f in files:
    name=rel(f)
    raw=open(f,encoding="utf-8").read()
    if re.search(r'<table', raw, re.I):
        n=len(re.findall(r'<table', raw, re.I))
        wrapped = raw.count('table-wrap')
        print(f"{name:55} tables={n} table-wrap occurrences={wrapped}")

print("\n=== SUMMARY ===")
from collections import Counter
c=Counter(i[1] for i in issues)
for k,v in c.items():
    print(f"  {v:3} files: {k}")
