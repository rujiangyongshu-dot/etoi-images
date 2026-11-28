# 座標グリッドを重ねた縮小画像。python3 tools/grid.py img x0,y0,x1,y1 out.png
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('RGB'); x0, y0, x1, y1 = map(int, sys.argv[2].split(','))
c = im.crop((x0, y0, x1, y1)); s = 700 / max(c.size); c = c.resize((int(c.width * s), int(c.height * s))); d = ImageDraw.Draw(c)
for x in range((x0 // 50 + 1) * 50, x1, 50): X = (x - x0) * s; d.line([(X, 0), (X, c.height)], fill=(255, 0, 0) if x % 100 == 0 else (255, 160, 160)); d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // 50 + 1) * 50, y1, 50): Y = (y - y0) * s; d.line([(0, Y), (c.width, Y)], fill=(0, 0, 255) if y % 100 == 0 else (160, 160, 255)); d.text((2, Y + 2), str(y), fill=(0, 255, 255))
c.save(sys.argv[3])
