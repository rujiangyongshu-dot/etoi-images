"""トライアルリール用：冒頭（部屋の画像と2コマ目）の一言だけを変えた版を作る（2026-11-28）。
python3 tools/hook_variants.py RID B "1行目" "2行目" "English"   → reels/RID-B/ と reels/RID-B.mp4、表紙・ストーリーも作る
本編・曲・説明文（1行目だけ差し替え）は元のまま。"""
import sys, os, re, json, shutil, subprocess
RID, tag, l1, l2, en = sys.argv[1:6]
NEW = f'{RID}-{tag}'; src = f'reels/{RID}'; dst = f'reels/{NEW}'
shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
p = f'{dst}/cfg.py'; L = open(p).read().split('\n'); n = 0
for i, l in enumerate(L):
    if "'t':" in l and n < 2:
        l = re.sub(r"'t':\[[^\]]*\]", "'t':" + repr([l1, l2]), l, count=1)
        l = re.sub(r"'en':(\"[^\"]*\"|'(?:[^'\\\\]|\\\\.)*')", "'en':" + repr(en), l, count=1)
        L[i] = l; n += 1
open(p, 'w').write('\n'.join(L))
m = json.load(open(f'{dst}/meta.json')); old = m.get('hook', '')
m['hook'] = l1 + l2; m['caption'] = m['caption'].replace(old, l1 + l2, 1) if old else m['caption']
m['variant_of'] = RID; json.dump(m, open(f'{dst}/meta.json', 'w'), ensure_ascii=False, indent=1)
subprocess.run(['python3', 'tools/reel2.py', p, f'reels/{NEW}.mp4'], check=True)
room = re.search(r"'room':'\.\./\.\./(rooms/[^']+)'", open(p).read())
if room: subprocess.run(['python3', 'tools/cover.py', room.group(1), f'{dst}/cover.jpg', l1, l2, en], check=True)
print(NEW)
