#!/usr/bin/env python3
"""
SEO HTTPS auditor & fixer for bpaau.org
Scans all HTML files in public/ (recursive) plus technical config files,
finds any http://bpaau.org references, reports them, and fixes them to https://.
"""
import os
import re
import sys

ROOT = r"C:\Users\User\Documents\GitHub\Australia igaming website"
PUBLIC = os.path.join(ROOT, "public")

# Files to scan
TARGET_EXTENSIONS = {".html", ".htm"}

# Technical files (relative to ROOT)
TECH_FILES = [
    os.path.join(PUBLIC, "sitemap.xml"),
    os.path.join(PUBLIC, "robots.txt"),
    os.path.join(PUBLIC, "llms.txt"),
    os.path.join(ROOT, "redirects.json"),
    os.path.join(PUBLIC, "site.webmanifest"),
]

# Pattern: http://bpaau.org  (NOT https://bpaau.org)
# We use a regex that matches http://bpaau.org but is careful not to match https://bpaau.org
PATTERN = re.compile(r"http://bpaau\.org")
REPLACEMENT = "https://bpaau.org"


def find_html_files(public_dir):
    """Recursively find all HTML files in public/."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(public_dir):
        # Skip backup / hidden dirs just in case
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in TARGET_EXTENSIONS:
                html_files.append(os.path.join(dirpath, fn))
    return sorted(html_files)


def scan_file(path):
    """
    Scan a file for http://bpaau.org occurrences.
    Returns list of (line_number, line_text, matched_url).
    """
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  ! Could not read {path}: {e}")
        return findings

    for i, line in enumerate(lines, start=1):
        for m in PATTERN.finditer(line):
            # Extract a bit of context around the match
            start = max(0, m.start() - 20)
            end = min(len(line), m.end() + 80)
            context = line[start:end].strip()
            findings.append((i, context))
    return findings


def fix_file(path):
    """
    Replace all http://bpaau.org with https://bpaau.org in a file.
    Returns number of replacements made.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        print(f"  ! Could not read {path}: {e}")
        return 0

    new_content, count = PATTERN.subn(REPLACEMENT, content)
    if count > 0:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            print(f"  ! Could not write {path}: {e}")
            return 0
    return count


def rel(path):
    try:
        return os.path.relpath(path, ROOT)
    except Exception:
        return path


def main():
    print("=" * 70)
    print("BPAU.ORG HTTPS AUDIT & FIX")
    print("=" * 70)

    # 1. Collect all HTML files
    html_files = find_html_files(PUBLIC)
    print(f"\n[1] HTML files found in public/ (recursive): {len(html_files)}")

    # 2. Build full scan list
    scan_list = list(html_files)
    for tf in TECH_FILES:
        if os.path.exists(tf):
            scan_list.append(tf)
        else:
            print(f"  (note: technical file not found, skipping: {rel(tf)})")

    total_scanned = len(scan_list)
    print(f"[2] Total files to scan (HTML + technical): {total_scanned}")

    # 3. Pre-fix scan: collect all findings
    print("\n[3] SCANNING for http://bpaau.org references...")
    findings_by_file = {}
    total_found = 0
    for path in scan_list:
        findings = scan_file(path)
        if findings:
            findings_by_file[path] = findings
            total_found += len(findings)

    print(f"    Total http://bpaau.org references FOUND: {total_found}")
    if findings_by_file:
        print("\n    --- Detailed findings (BEFORE fix) ---")
        for path, findings in findings_by_file.items():
            print(f"\n    FILE: {rel(path)}")
            for line_no, ctx in findings:
                print(f"      line {line_no}: {ctx}")
    else:
        print("    (none found - site may already be fully https)")

    # 4. Fix
    print("\n[4] FIXING http://bpaau.org -> https://bpaau.org ...")
    total_fixed = 0
    files_modified = []
    for path in scan_list:
        n = fix_file(path)
        if n > 0:
            files_modified.append((rel(path), n))
            total_fixed += n

    print(f"    Total replacements made: {total_fixed}")
    if files_modified:
        print("\n    --- Files modified ---")
        for rp, n in files_modified:
            print(f"      {rp}  ({n} replacement(s))")
    else:
        print("    (no files needed modification)")

    # 5. Re-scan to confirm zero remaining
    print("\n[5] RE-SCANNING to confirm zero http://bpaau.org references remain...")
    remaining = 0
    remaining_files = []
    for path in scan_list:
        findings = scan_file(path)
        if findings:
            remaining_files.append((rel(path), findings))
            remaining += len(findings)

    print(f"    Remaining http://bpaau.org references: {remaining}")
    if remaining_files:
        print("    !!! STILL FOUND - details below !!!")
        for rp, findings in remaining_files:
            print(f"    FILE: {rp}")
            for line_no, ctx in findings:
                print(f"      line {line_no}: {ctx}")
    else:
        print("    OK - zero http://bpaau.org references remain.")

    # 6. Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total files scanned:                          {total_scanned}")
    print(f"Total http://bpaau.org references found:       {total_found}")
    print(f"Total references fixed:                        {total_fixed}")
    print(f"Remaining http://bpaau.org references:         {remaining}")
    print(f"Files modified:                                {len(files_modified)}")
    if files_modified:
        print("\nList of files modified:")
        for rp, n in files_modified:
            print(f"  - {rp}")

    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
