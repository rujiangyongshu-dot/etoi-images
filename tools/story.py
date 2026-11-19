"""ETOI story image (1080x1920) that sends viewers to the feed post.
usage: python3 tools/story.py SLIDE1.jpg CAPTION.txt OUT.jpg
- Shows the post's first slide (its hook) large, framed, on a blurred backdrop.
- Top: 'NEW POST' label and the artwork title (from the caption's first line).
- Bottom: a clear call to action (tap @etoi.art at the top left -> latest post, 10 slides).
"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920


def font(name, size):
    for d in ['/usr/share/fonts/opentype/noto/',
              os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/')]:
        if os.path.exists(d + name):
            return ImageFont.truetype(d + name, size, index=0)
    raise SystemExit('font not found: ' + name)


sans = lambda s: font('NotoSansCJK-Medium.ttc', s)
bold = lambda s: font('NotoSansCJK-Bold.ttc', s)
serif = lambda s: font('NotoSerifCJK-SemiBold.ttc', s)

src, cap_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
slide = Image.open(src).convert('RGB')
cap = open(cap_path, encoding='utf-8').read().strip().splitlines()
first = next((l for l in cap if l.strip()), '')
title = first.replace('🎨', '').strip().split('（')[0].strip()
painter = ''
for l in cap[1:4]:
    if l.startswith('—'):
        painter = re.sub(r'（.*', '', l.lstrip('— ').strip())
        break

# backdrop: blurred, darkened slide
k = max(W / slide.width, H / slide.height) * 1.15
bg = slide.resize((int(slide.width * k), int(slide.height * k)), Image.BILINEAR)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg = bg.filter(ImageFilter.GaussianBlur(45))
bg = Image.eval(bg, lambda v: int(v * .35))
im = bg.copy()
d = ImageDraw.Draw(im)

# the post's first slide, framed
cw = 840; ch = int(cw * slide.height / slide.width)
card = slide.resize((cw, ch), Image.LANCZOS)
x = (W - cw) // 2; y = 340
sh = Image.new('L', (W, H), 0)
ImageDraw.Draw(sh).rectangle([x + 8, y + 22, x + cw + 8, y + ch + 22], fill=170)
sh = sh.filter(ImageFilter.GaussianBlur(24))
im.paste((0, 0, 0), (0, 0), sh)
d = ImageDraw.Draw(im)
d.rectangle([x - 6, y - 6, x + cw + 6, y + ch + 6], fill=(244, 240, 231))
im.paste(card, (x, y))

# top: label + title
d.rounded_rectangle([W // 2 - 120, 196, W // 2 + 120, 252], radius=28, fill=(244, 240, 231))
d.text((W // 2, 224), 'NEW POST', font=bold(30), fill=(24, 24, 26), anchor='mm')
t = title
f = sans(40)
while f.getlength(t) > 960 and f.size > 26:
    f = sans(f.size - 2)
d.text((W // 2, 298), t, font=f, fill=(255, 255, 255), anchor='mm')

# bottom: call to action
yb = y + ch + 60
if painter:
    d.text((W // 2, yb), painter, font=sans(30), fill=(220, 214, 200), anchor='mm')
    yb += 62
d.text((W // 2, yb), 'この続きは、投稿で。全10枚', font=bold(46), fill=(255, 255, 255), anchor='mm')
yb += 78
d.rounded_rectangle([W // 2 - 330, yb - 40, W // 2 + 330, yb + 40], radius=40, fill=(244, 240, 231))
d.text((W // 2, yb), '左上の @etoi.art をタップして投稿へ', font=sans(32), fill=(24, 24, 26), anchor='mm')
d.text((W // 2, H - 190), 'ETOI  答えのない世界で、自分の答えを描く。', font=serif(26), fill=(200, 196, 186), anchor='mm')
im.save(out, quality=90, optimize=True)
print(out, title, painter)
