import os

games_dir = r'C:\Users\User\Documents\GitHub\Australia igaming website\public\assets\games'
if os.path.exists(games_dir):
    files = [f for f in os.listdir(games_dir) if f.endswith('.webp')]
    print('Game images:', len(files))
    for f in sorted(files):
        print(' ', f)
else:
    print('games dir not found')

with open(r'C:\Users\User\Documents\GitHub\Australia igaming website\public\index.html', 'r', encoding='utf-8') as f:
    hp = f.read()
print()
print('Homepage game-grid count:', hp.count('game-grid'))
print('Homepage game-card count:', hp.count('game-card'))

with open(r'C:\Users\User\Documents\GitHub\Australia igaming website\public\assets\theme.css', 'r', encoding='utf-8') as f:
    css = f.read()
print()
print('CSS has .game-grid:', '.game-grid' in css)
print('CSS has .game-card:', '.game-card' in css)

pages_with_games = 0
for root, dirs, files in os.walk(r'C:\Users\User\Documents\GitHub\Australia igaming website\public'):
    for f in files:
        if f.endswith('.html'):
            with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
                if 'game-grid' in fh.read():
                    pages_with_games += 1
print()
print('Pages with game sections:', pages_with_games)
