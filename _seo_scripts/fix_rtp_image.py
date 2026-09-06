import os
filepath = r'C:\Users\User\Documents\GitHub\Australia igaming website\public\best-high-rtp-pokies-australia-2026.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

anchor = 'RTP is not a guarantee of short-term results'
idx = content.find(anchor)
if idx == -1:
    print('anchor not found')
else:
    para_end = content.find('</p>', idx) + 4
    figure = '\n<figure class="inline-figure">\n<img alt="Mega Ace pokie game - 97 percent RTP, one of the highest-return pokies for Australian players" decoding="async" height="300" loading="lazy" src="/assets/games/mega-ace.webp" width="400"/>\n<figcaption>Mega Ace (JILI) - 97% RTP, a top high-return pokie</figcaption>\n</figure>\n'
    content = content[:para_end] + figure + content[para_end:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('ADDED inline figure to best-high-rtp page')
