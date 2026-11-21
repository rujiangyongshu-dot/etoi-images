"""1本のカルーセル投稿につき3枚のストーリーを作る（2026-11-21）。
usage: python3 tools/make_stories.py NN [NN ...]
  stories/NN.jpg   … 1枚目（NEW POST・フック）
  stories/NN_2.jpg … 4枚目の字幕（2 / 3・この先に、意外な展開が。）
  stories/NN_3.jpg … 7枚目の字幕（3 / 3・最後の一言は、投稿で。）
"""
import sys, subprocess, os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'story.py')
for a in sys.argv[1:]:
    NN = '%02d' % int(a); P = f'posts/{NN}'
    cap = f'{P}/caption.txt'
    runs = [[f'{P}/01.jpg', cap, f'stories/{NN}.jpg'],
            [f'{P}/04.jpg', cap, f'stories/{NN}_2.jpg', '--label=2 / 3', '--cta=この先に、意外な展開が。'],
            [f'{P}/07.jpg', cap, f'stories/{NN}_3.jpg', '--label=3 / 3', '--cta=最後の一言は、投稿で。']]
    for r in runs:
        if os.path.exists(r[0]):
            subprocess.run(['python3', T] + r, check=True, stdout=subprocess.DEVNULL)
    print(NN, 'ok')
