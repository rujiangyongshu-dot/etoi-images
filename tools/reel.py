"""Turn a published ETOI carousel into a Reel (1080x1920, 30fps, ~35s, original synthesized BGM).
usage: python3 tools/reel.py SLIDES_DIR OUT.mp4
SLIDES_DIR holds 01.jpg..10.jpg (1080x1440). Slides 1-9 carry the captions already; slide 10 is the framed end card.
Design: hook slide first and short (viewers decide in ~1.5s), gentle push-in on every slide,
quick cross-fades, text stays inside the Reels safe area, original music (no copyright issues).
"""
import sys, os, subprocess, wave, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cafe

W, H, FPS = 1080, 1920, 30
src, out = sys.argv[1], sys.argv[2]
slides = sorted(glob.glob(os.path.join(src, '[0-9][0-9].jpg')))[:10]
assert len(slides) >= 3, slides
N = len(slides)
durs = [2.6] + [3.4] * (N - 2) + [3.2]          # hook / body / end card
XF = 0.35                                          # cross-fade seconds


def font(name, size):
    for d in ['/usr/share/fonts/opentype/noto/', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/')]:
        if os.path.exists(d + name):
            return ImageFont.truetype(d + name, size, index=0)
    raise SystemExit('font not found ' + name)


sans = lambda s: font('NotoSansCJK-Medium.ttc', s)
serif = lambda s: font('NotoSerifCJK-SemiBold.ttc', s)

CW = 1000                       # slide width on the reel canvas
CY = 250                        # top of the slide


def backdrop(im):
    k = max(W / im.width, H / im.height) * 1.15
    bg = im.resize((int(im.width * k), int(im.height * k)), Image.BILINEAR)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(45))
    return Image.eval(bg, lambda v: int(v * .32))


def overlay():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((W // 2, 150), 'ETOI｜名画の読み方', font=serif(34), fill=(244, 240, 231, 235), anchor='mm')
    d.text((W // 2, CY + int(CW * 1440 / 1080) + 70), '保存して、あとで読み返す', font=sans(32), fill=(230, 226, 216, 220), anchor='mm')
    return lay


PRE = [(Image.open(p).convert('RGB')) for p in slides]
BGS = [backdrop(im) for im in PRE]
OV = overlay()
CH = int(CW * 1440 / 1080)


def frame(i, p):
    """slide i at progress p in [0,1]: slow push-in 1.00 -> 1.05."""
    im = PRE[i]
    z = 1.0 + 0.05 * p
    cw, ch = int(CW * z), int(CH * z)
    big = im.resize((cw, ch), Image.BILINEAR)
    big = big.crop(((cw - CW) // 2, (ch - CH) // 2, (cw - CW) // 2 + CW, (ch - CH) // 2 + CH))
    f = BGS[i].copy()
    f.paste(big, ((W - CW) // 2, CY))
    f = f.convert('RGBA')
    f.alpha_composite(OV)
    return f.convert('RGB')


starts = np.cumsum([0] + durs[:-1])
T = float(sum(durs))
nf = int(T * FPS)
tmpv = out + '.v.mp4'
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                       '-pix_fmt', 'yuv420p', tmpv], stdin=subprocess.PIPE)
for k in range(nf):
    t = k / FPS
    i = int(np.searchsorted(starts, t, side='right') - 1)
    p = (t - starts[i]) / durs[i]
    img = frame(i, p)
    te = starts[i] + durs[i]
    if i + 1 < N and t > te - XF:              # cross-fade into the next slide
        a = (t - (te - XF)) / XF
        img = Image.blend(img, frame(i + 1, 0.0), a)
    ff.stdin.write(img.tobytes())
ff.stdin.close(); ff.wait()

# original music, final chord lands on the end card
m, bpm = cafe.build(float(starts[-1]), T)
m = (m / np.max(np.abs(m)) * 0.6 * 32767).astype(np.int16)
fade = int(0.8 * cafe.SR)
env = np.ones(len(m)); env[-fade:] = np.linspace(1, 0, fade)
m = (m * env[:, None]).astype(np.int16)
wav = out + '.a.wav'
with wave.open(wav, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(cafe.SR); w.writeframes(m.tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmpv, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                '-shortest', '-movflags', '+faststart', out], check=True)
os.remove(tmpv); os.remove(wav)
print(out, round(T, 1), 's')
