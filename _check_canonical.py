import os, re
d = r'C:\Users\User\Documents\GitHub\bpaau2\public'
if os.path.exists(d):
    files = [f for f in os.listdir(d) if f.endswith('.html')]
    print('bpaau2/public exists, HTML files:', len(files))
    for f in sorted(files)[:5]:
        with open(os.path.join(d, f), 'r', encoding='utf-8') as fh:
            c = fh.read()
        m = re.search(r'<link[^>]*canonical[^>]*>', c)
        print(f, '->', m.group(0)[:120] if m else 'NO CANONICAL')
else:
    print('bpaau2/public NOT FOUND')
