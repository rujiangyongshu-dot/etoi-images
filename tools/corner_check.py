# 4隅の拡大（指定の座標に十字）。python3 tools/corner_check.py img "x,y x,y x,y x,y" out.png
import sys
from PIL import Image, ImageDraw
rgb = Image.open(sys.argv[1]).convert('RGB'); C = [tuple(map(float, p.split(','))) for p in sys.argv[2].split()]; tiles = []
for (x, y) in C:
    t = rgb.crop((int(x) - 40, int(y) - 40, int(x) + 40, int(y) + 40)).resize((200, 200), Image.LANCZOS); d = ImageDraw.Draw(t)
    d.line([(100, 0), (100, 200)], fill=(255, 0, 0)); d.line([(0, 100), (200, 100)], fill=(255, 0, 0))
    for k in range(0, 200, 25): d.line([(k, 98), (k, 102)], fill=(0, 255, 255)); d.line([(98, k), (102, k)], fill=(0, 255, 255))
    tiles.append(t)
s = Image.new('RGB', (800, 200)); [s.paste(t, (i * 200, 0)) for i, t in enumerate(tiles)]; s.save(sys.argv[3] if len(sys.argv) > 3 else '/tmp/cc.png')
