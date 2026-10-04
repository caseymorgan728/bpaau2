# -*- coding: utf-8 -*-
"""Fix the 37 pre-existing broken refs found by exhaustive_link_audit."""
import io, os, glob

PUB = os.path.join(os.path.dirname(__file__), "public")
os.chdir(PUB)

# (old substring, new substring) applied globally
REPL = [
 # OG / twitter images missing /blog banner/ prefix
 ('https://bpaau.org/for%20blogpost%201%20and%206.webp',
  'https://bpaau.org/blog%20banner/for%20blogpost%201%20and%206.webp'),
 ('https://bpaau.org/blogpost%20',
  'https://bpaau.org/blog%20banner/blogpost%20'),
 # literal-space / wrong-dir img src
 ('src="/blog banner/blogpost 6.webp"',
  'src="/blog%20banner/for%20blogpost%201%20and%206.webp"'),
 ('src="/blog%20banner/blogpost%201.webp"',
  'src="/blog%20banner/for%20blogpost%201%20and%206.webp"'),
 ('src="/blog%20banner/blogpost%206.webp"',
  'src="/blog%20banner/for%20blogpost%201%20and%206.webp"'),
 ('src="/blog banner/bonus-types-banner.webp"',
  'src="/assets/sections/bonus-types-banner.webp"'),
 ('src="/blog banner/daily-free-credits-banner.webp"',
  'src="/assets/sections/daily-free-credits-banner.webp"'),
 # JSON-LD breadcrumb items
 ('https://bpaau.org/blog/reviews', 'https://bpaau.org/blog'),
 ('https://bpaau.org/blog/fast-payouts', 'https://bpaau.org/blog/fast-cashouts'),
 # broken internal links
 ('href="/bankroll-management"', 'href="/blog/winning-tips"'),
 ('href="/crypto-pokies-australia-bitcoin-2026"',
  'href="/crypto-pokies-australia-2026"'),
]

changed_files = 0
total_repl = 0
for f in glob.glob("**/*.html", recursive=True):
    t = io.open(f, encoding="utf-8").read()
    orig = t
    n = 0
    for old, new in REPL:
        c = t.count(old)
        if c:
            t = t.replace(old, new); n += c
    if t != orig:
        io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        changed_files += 1; total_repl += n
        print("fixed %3d in %s" % (n, f))
print("files changed:", changed_files, "replacements:", total_repl)
