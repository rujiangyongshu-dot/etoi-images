# 生成した「絵を飾った部屋」画像の額の中に、本物の作品画像を遠近を合わせてはめ込む
# python3 room_composite.py ROOM.png SRC.jpg OUT.jpg "x1,y1 x2,y2 x3,y3 x4,y4"(左上,右上,右下,左下) [前景の保護領域 x0,y0,x1,y1 ...]
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
room, srcp, outp, quad = sys.argv[1:5]
ROUND = '--round' in sys.argv  # 円形の絵（トンド）：4点の外接四角に内接する楕円で切り抜く
zones = [tuple(map(int, z.split(','))) for z in sys.argv[5:] if z != '--round']
bg = Image.open(room).convert('RGB'); W, H = bg.size
dst = [tuple(map(float, p.split(','))) for p in quad.split()]
src = Image.open(srcp).convert('RGB'); sw, sh = src.size
tw = ((dst[1][0]-dst[0][0]) + (dst[2][0]-dst[3][0])) / 2; th = ((dst[3][1]-dst[0][1]) + (dst[2][1]-dst[1][1])) / 2
tgt = tw / th
if sw / sh > tgt: cw = int(sh * tgt); x0 = (sw - cw) // 2; src = src.crop((x0, 0, x0 + cw, sh))
else: ch = int(sw / tgt); y0 = (sh - ch) // 2; src = src.crop((0, y0, sw, y0 + ch))
sw, sh = src.size
_t = int(tw * 1.5)  # 先に縮めてから貼る（ひび割れのちらつき防止）
if sw > _t: src = src.resize((_t, int(sh * _t / sw)), Image.LANCZOS); sw, sh = src.size
def coeffs(pa, pb):
    A = []; B = []
    for (x, y), (X, Y) in zip(pa, pb):
        A.append([x, y, 1, 0, 0, 0, -X*x, -X*y]); A.append([0, 0, 0, x, y, 1, -Y*x, -Y*y]); B += [X, Y]
    return np.linalg.solve(np.array(A, float), np.array(B, float))
warp = src.transform((W, H), Image.PERSPECTIVE, tuple(coeffs(dst, [(0, 0), (sw, 0), (sw, sh), (0, sh)])), Image.BICUBIC)
m = Image.new('L', (W, H), 0)
if ROUND: ImageDraw.Draw(m).ellipse([min(p[0] for p in dst), min(p[1] for p in dst), max(p[0] for p in dst), max(p[1] for p in dst)], fill=255)
else: ImageDraw.Draw(m).polygon(dst, fill=255)
g = np.asarray(bg, float); lum = g.mean(2)
fg = np.zeros((H, W), bool)
for (a, b, c, d) in zones:   # 明るい前景（人物の頭など）を残す
    sub = lum[b:d, a:c] > 135
    for x in range(sub.shape[1]):
        ys = np.where(sub[:, x])[0]
        if len(ys): sub[ys[0]:, x] = True
    fg[b:d, a:c] |= sub
fgm = Image.fromarray((fg*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
m = Image.fromarray((np.asarray(m, float) * (1 - np.asarray(fgm, float)/255)).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
r = np.asarray(warp, float)
blur = lambda a, k: np.asarray(Image.fromarray(a.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(k)), float)
Lg = blur(g, 50).mean(2, keepdims=True) + 1; Lr = blur(r, 50).mean(2, keepdims=True) + 1
out = r * (Lg / Lr).clip(0.35, 1.4)
mu = out.mean(); out = (out - mu) * 0.9 + mu
out = out * np.array([1.05, 0.97, 0.82])
out = Image.fromarray(out.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
res = Image.composite(out, bg, m)
shm = Image.new('L', (W, H), 0); d = ImageDraw.Draw(shm)
for i in range(0 if ROUND else 14): d.line([(dst[0][0], dst[0][1]+i), (dst[1][0], dst[1][1]+i)], fill=int(110*(1-i/14)))
shm = Image.fromarray((np.asarray(shm, float) * np.asarray(m, float)/255).astype('uint8'))
res = Image.composite(Image.new('RGB', (W, H)), res, shm)
res.save(outp, quality=93)
