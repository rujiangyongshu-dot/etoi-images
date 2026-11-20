"""ETOI 読み解きリール（絵画深読み型, 2026-11-20）
細部へゆっくり寄るカメラ＋中央の字幕。音は付けない（無音トラック）。曲は投稿時に Instagram の音楽ライブラリから付ける。
usage: python3 reel2.py CONFIG.py OUT.mp4
  CONFIG.py は etoi_carousel の cfg（IMAGES / SLIDES の cam と t / CATEGORY）。画像パスは cfg の場所から読む。
"""
import sys, os, subprocess, importlib.util, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
def _f(n):
    for d in ['/usr/share/fonts/opentype/noto/', HERE + '/fonts/', os.path.expanduser('~/etoi/fonts/')]:
        if os.path.exists(d + n): return d + n
    raise SystemExit('font not found ' + n)
serif = lambda s: ImageFont.truetype(_f('NotoSerifCJK-SemiBold.ttc'), s, index=0)
bold = lambda s: ImageFont.truetype(_f('NotoSerifCJK-Bold.ttc') if os.path.exists('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc') else _f('NotoSerifCJK-SemiBold.ttc'), s, index=0)

spec = importlib.util.spec_from_file_location('cfg', sys.argv[1]); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
OUT = sys.argv[2]; CFGDIR = os.path.dirname(os.path.abspath(sys.argv[1]))
SRC = {}
for k, v in C.IMAGES.items():
    im = Image.open(os.path.join(CFGDIR, os.path.expanduser(v))).convert('RGB')
    s = 3600 / max(im.size)
    if s < 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    SRC[k] = im

def view(k, cx, cy, h):
    im = SRC[k]; iw, ih = im.size; vh = h * ih; vw = vh * W / H
    if vw > iw: vw = iw; vh = vw * H / W
    if vh > ih:  # 画面に収まらない → ぼかし背景＋全体
        s = W / iw; fg = im.resize((W, int(ih * s)), Image.BILINEAR)
        k2 = H / ih * 1.1; bg = im.resize((int(iw * k2), int(ih * k2)), Image.BILINEAR)
        bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
        bg = Image.eval(bg, lambda v: int(v * .4)); bg.paste(fg, (0, (H - fg.height) // 2)); return bg
    px = min(max(cx * iw, vw / 2), iw - vw / 2); py = min(max(cy * ih, vh / 2), ih - vh / 2)
    return im.resize((W, H), Image.BILINEAR, box=(px - vw / 2, py - vh / 2, px + vw / 2, py + vh / 2))

def caption(lines, size=54, y=None, font=serif):
    f = font(size)
    while max(f.getlength(x) for x in lines) > 940: size -= 2; f = font(size)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); lh = int(size * 1.55)
    blk = len(lines) * lh - (lh - size); y0 = int((y or H * .5) - blk / 2)
    for i, ln in enumerate(lines): d.text((W / 2, y0 + i * lh), ln, font=f, fill=(255, 255, 255, 255), anchor='ma')
    a = lay.split()[3].filter(ImageFilter.GaussianBlur(9))
    sh = Image.fromarray(np.clip(np.asarray(a, dtype=np.float32) * 2.6, 0, 210).astype(np.uint8))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.putalpha(sh); return Image.alpha_composite(out, lay)

def endcard(k):
    im = Image.new('RGB', (W, H), (20, 18, 16)); src = SRC[k]
    s = min(820 / src.width, 1000 / src.height); art = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    fw, fh = art.width + 48, art.height + 48; x = (W - fw) // 2; y = 420 + (1000 - art.height) // 2 - 24
    d = ImageDraw.Draw(im); d.rectangle([x, y, x + fw, y + fh], fill=(150, 122, 70)); d.rectangle([x + 12, y + 12, x + fw - 12, y + fh - 12], fill=(240, 236, 226)); im.paste(art, (x + 24, y + 24))
    d.text((W / 2, 250), 'ETOI｜名画の読み方', font=serif(44), fill=(236, 231, 220), anchor='ma')
    d.text((W / 2, y + fh + 90), '全10枚の解説は、プロフィールの投稿で', font=serif(40), fill=(236, 231, 220), anchor='ma')
    d.text((W / 2, y + fh + 160), '答えのない世界で、自分の答えを描く。', font=serif(30), fill=(180, 172, 160), anchor='ma')
    return im

shots = [s for s in C.SLIDES if not s.get('mock')]
mock = next((s for s in C.SLIDES if s.get('mock')), shots[0])
DUR = [3.4] + [3.6] * (len(shots) - 2) + [4.2]
XF = 0.5; END = 3.0
ease = lambda t: t * t * (3 - 2 * t)
layers = []
for i, s in enumerate(shots):
    if i == 0:
        cat = getattr(C, 'CATEGORY', '')
        L = caption(s['t'], size=68, y=H * .5, font=bold)
        if cat:
            dd = ImageDraw.Draw(L); dd.text((W / 2, H * .5 + 190), 'ETOI ｜ ' + cat, font=serif(32), fill=(236, 231, 220, 230), anchor='ma')
    else:
        L = caption(s['t'], size=54, y=(H * .66) if s.get('en') else (H * .5))
    en = s.get('en')
    if en:  # 英語の小さな字幕（2026-11-20）。日本語の下、リールの操作ボタンにかからない高さ
        dd = ImageDraw.Draw(L); fe = ImageFont.truetype(_f('NotoSansCJK-Medium.ttc'), 30, index=0)
        words = en.split(' '); rows = ['']
        for w in words:
            t = (rows[-1] + ' ' + w).strip()
            if dd.textlength(t, font=fe) <= 900: rows[-1] = t
            else: rows.append(w)
        ey = (H * .5 + 260) if i == 0 else (H * .66 + 135)
        for k, r in enumerate(rows[:2]):
            dd.text((W / 2, ey + k * 42), r, font=fe, fill=(232, 226, 214, 225), anchor='ma', stroke_width=2, stroke_fill=(0, 0, 0, 120))
    layers.append(L)

def shot_frame(i, t):  # t: 0..1 within shot
    s = shots[i]; cx, cy, h = s['cam']
    # ゆっくり寄る（1.18倍→1.0倍）、少し横に流す
    z = 1.18 - 0.18 * ease(t); dx = (0.012 if i % 2 else -0.012) * (1 - ease(t))
    fr = view(s['img'], cx + dx, cy, min(h * z, 1.0))
    a = min(1, t * DUR[i] / 0.45)  # 字幕フェードイン
    L = layers[i] if a >= 1 else Image.fromarray((np.asarray(layers[i]) * np.array([1, 1, 1, a])).astype(np.uint8))
    return Image.alpha_composite(fr.convert('RGBA'), L).convert('RGB')

total = sum(DUR) + END
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                       '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
starts = np.cumsum([0] + DUR)
ec = endcard(mock['img'])
n = int(total * FPS)
for f in range(n):
    T = f / FPS
    i = int(np.searchsorted(starts, T, side='right') - 1)
    if i >= len(shots):
        a = min(1, (T - starts[-1]) / 0.6)
        fr = Image.blend(shot_frame(len(shots) - 1, 1.0), ec, a) if a < 1 else ec
    else:
        t = (T - starts[i]) / DUR[i]; fr = shot_frame(i, t)
        if i + 1 < len(shots) and T > starts[i + 1] - XF:
            b = (T - (starts[i + 1] - XF)) / XF; fr = Image.blend(fr, shot_frame(i + 1, 0.0), ease(b))
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print(OUT, round(total, 1), 's')
