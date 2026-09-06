"""Fix UTF-8 mojibake (double-encoded cp1252->utf8) across all HTML files."""
import os
import sys

PUBLIC = r'C:\Users\User\Documents\GitHub\Australia igaming website\public'

# Targeted replacements for common mojibake patterns
REPLACEMENTS = [
    # Em dash
    ('â€"', '—'),
    ('â€”', '—'),
    # En dash
    ('â€"', '–'),
    ('â€“', '–'),
    # Left double quote
    ('â€œ', '"'),
    # Right double quote
    ('â€', '"'),
    ('â€\u009d', '"'),
    # Left single quote
    ('â€˜', "'"),
    # Right single quote / apostrophe
    ('â€™', "'"),
    # Bullet
    ('â€¢', '•'),
    # Ellipsis
    ('â€¦', '…'),
    # Euro sign (rare)
    ('â‚¬', '€'),
    # Trademark
    ('â„¢', '™'),
    # Registered
    ('Â®', '®'),
    # Copyright
    ('Â©', '©'),
    # Degree
    ('Â°', '°'),
    # Non-breaking space leftover
    ('Â ', ' '),
    ('Â\xa0', ' '),
]

def fix_mojibake(text):
    """Try the cp1252 round-trip first, then targeted replacements."""
    # Method 1: cp1252 round-trip (fixes most double-encoded UTF-8)
    try:
        fixed = text.encode('cp1252', errors='strict').decode('utf-8', errors='strict')
        # If the result has fewer mojibake markers, use it
        if fixed.count('â€') < text.count('â€'):
            text = fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # Method 2: targeted replacements (catches anything the round-trip missed)
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    return text

def main():
    fixed_count = 0
    total_files = 0
    mojibake_files = []

    for root, dirs, files in os.walk(PUBLIC):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            total_files += 1

            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                original = fh.read()

            # Check if mojibake is present
            if 'â€' not in original and 'Â' not in original:
                continue

            fixed = fix_mojibake(original)

            if fixed != original:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(fixed)
                fixed_count += 1
                rel = os.path.relpath(path, PUBLIC)
                mojibake_files.append(rel)
                print(f'FIXED: {rel}')

    print(f'\n=== SUMMARY ===')
    print(f'Total HTML files scanned: {total_files}')
    print(f'Files with mojibake fixed: {fixed_count}')

    # Verify no mojibake remains
    remaining = 0
    for root, dirs, files in os.walk(PUBLIC):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            if 'â€' in content:
                remaining += 1
                print(f'STILL HAS MOJIBAKE: {os.path.relpath(path, PUBLIC)}')

    print(f'Files still containing â€: {remaining}')
    if remaining == 0:
        print('SUCCESS: All mojibake removed!')
    else:
        print('WARNING: Some mojibake remains (may be in non-HTML-safe contexts)')

if __name__ == '__main__':
    main()
