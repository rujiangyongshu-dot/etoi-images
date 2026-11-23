"""リールの表紙（9:16）を部屋の画像から作る（制作基準 v3・2026-11-23）。動画には部屋の画像を入れず、表紙だけにする。
python3 tools/cover.py rooms/NN/room.jpg reels/RID/cover.jpg "1行目" "2行目" ["English line"]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
def _f(n):
    for d in ['/usr/share/fonts/opentype/noto/', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/')]:
        if os.path.exists(d + n): return d + n
    raise SystemExit('font not found: ' + n)
src, out, *txt = sys.argv[1:]
en = txt[2] if len(txt) > 2 else None
lines = [x for x in txt[:2] if x]
im = Image.open(src).convert('RGB'); s = max(W / im.width, H / im.height)
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).convert('RGBA')
g = Image.new('L', (1, H))
for y in range(H): g.putpixel((0, y), int(200 * max(0, (y - H * .45) / (H * .55)) ** 1.2))
im = Image.alpha_composite(im, Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [g.resize((W, H))]))
d = ImageDraw.Draw(im); size = 150 if len(lines) == 1 else (165 if max(len(x) for x in lines) <= 6 else 76)  # 1行なら大きく（11/23 オーナー：ドンと見せる）
bf = lambda z: ImageFont.truetype(_f('NotoSansCJK-Bold.ttc'), z, index=0)
f = bf(size)
while max(f.getlength(x) for x in lines) > 980: size -= 2; f = bf(size)
y0 = int(H * .64); lh = int(size * 1.35)
for i, ln in enumerate(lines):
    d.text((W / 2, y0 + i * lh), ln, font=f, fill='white', anchor='ma', stroke_width=3, stroke_fill=(0, 0, 0))
if en:
    d.text((W / 2, y0 + len(lines) * lh + 30), en, font=ImageFont.truetype(_f('NotoSansCJK-Medium.ttc'), 30, index=0),
           fill=(232, 226, 214), anchor='ma', stroke_width=2, stroke_fill=(0, 0, 0))
im.convert('RGB').save(out, quality=92)
