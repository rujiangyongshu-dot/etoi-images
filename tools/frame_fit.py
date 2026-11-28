"""部屋の画像の額の「内側の縁」を、おおよその4隅から精密に合わせる（2026-11-28）。
python3 tools/frame_fit.py room_gpt.png "x0,y0,x1,y1"（おおよその内側の縁）→ 4隅を出力し、/tmp/ff_check.png に4隅の拡大を書く"""
import sys, numpy as np
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('L'); A = np.asarray(im, float)
x0, y0, x1, y1 = map(int, sys.argv[2].split(','))
R = 10
CX, CY = (x0 + x1) / 2, (y0 + y1) / 2
def edge_h(y, xa, xb):  # 横の辺：額（外）→絵（内）の明るさの変わり目。向きは内外の平均で決める
    inside = 1 if CY > y else -1
    o = A[y - inside * 12, xa:xb].mean(); i_ = A[y + inside * 12, xa:xb].mean(); sg = np.sign(i_ - o) * inside or 1
    pts = []
    for x in range(xa, xb, 3):
        col = A[max(0, y - R):y + R + 1, x]; g = np.diff(col) * sg; pts.append((x, max(0, y - R) + int(np.argmax(g)) + 0.5))
    return pts
def edge_v(x, ya, yb):
    inside = 1 if CX > x else -1
    o = A[ya:yb, x - inside * 12].mean(); i_ = A[ya:yb, x + inside * 12].mean(); sg = np.sign(i_ - o) * inside or 1
    pts = []
    for y in range(ya, yb, 3):
        row = A[y, max(0, x - R):x + R + 1]; g = np.diff(row) * sg; pts.append((y, max(0, x - R) + int(np.argmax(g)) + 0.5))
    return pts
def fit(pts):  # 外れ値に強い直線（中央値ベース）
    p = np.array(pts); a, b = np.polyfit(p[:, 0], p[:, 1], 1)
    r = np.abs(p[:, 1] - (a * p[:, 0] + b)); keep = r < max(1.5, np.median(r) * 2.5)
    return np.polyfit(p[keep, 0], p[keep, 1], 1)
mx = (x1 - x0) // 6; my = (y1 - y0) // 6
T = fit(edge_h(y0, x0 + mx, x1 - mx)); B = fit(edge_h(y1, x0 + mx, x1 - mx))
L = fit(edge_v(x0, y0 + my, y1 - my)); Rr = fit(edge_v(x1, y0 + my, y1 - my))
def cross(h, v):  # y = h0 x + h1 ; x = v0 y + v1
    y = (h[0] * v[1] + h[1]) / (1 - h[0] * v[0]); return (v[0] * y + v[1], y)
C = [cross(T, L), cross(T, Rr), cross(B, Rr), cross(B, L)]
print(' '.join(f'{x:.0f},{y:.0f}' for x, y in C))
rgb = Image.open(sys.argv[1]).convert('RGB'); tiles = []
for (x, y) in C:
    t = rgb.crop((int(x) - 45, int(y) - 45, int(x) + 45, int(y) + 45)).resize((180, 180), Image.LANCZOS); d = ImageDraw.Draw(t)
    d.line([(90, 0), (90, 180)], fill=(255, 0, 0)); d.line([(0, 90), (180, 90)], fill=(255, 0, 0)); tiles.append(t)
s = Image.new('RGB', (720, 180)); [s.paste(t, (i * 180, 0)) for i, t in enumerate(tiles)]; s.save('/tmp/ff_check.png')
