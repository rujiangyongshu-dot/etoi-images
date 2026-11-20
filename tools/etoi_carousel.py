"""ETOI carousel renderer (1080x1350). usage: python3 etoi_carousel.py CONFIG.py OUTDIR"""
import numpy as np, sys, os, importlib.util
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS=None
W,H=1080,1440
import glob
def _f(n):
    for d in ['/usr/share/fonts/opentype/noto/',os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts/'),os.path.expanduser('~/etoi/fonts/')]:
        if os.path.exists(d+n): return d+n
    raise SystemExit('font not found: '+n+' (apt-get install -y fonts-noto-cjk)')
sans=lambda s:ImageFont.truetype(_f('NotoSansCJK-Medium.ttc'),s,index=0)
serif=lambda s:ImageFont.truetype(_f('NotoSerifCJK-SemiBold.ttc'),s,index=0)
bold=lambda s:ImageFont.truetype(_f('NotoSansCJK-Bold.ttc'),s,index=0)
PAPER=(244,240,231); INK=(24,24,26)
spec=importlib.util.spec_from_file_location('cfg',sys.argv[1]); C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
CFGDIR=os.path.dirname(os.path.abspath(sys.argv[1]))
SRC={k:Image.open(os.path.join(CFGDIR,os.path.expanduser(v))).convert('RGB') for k,v in C.IMAGES.items()}
def view(k,c):
    im=SRC[k]; iw,ih=im.size; cx,cy,h=c; vh=h*ih; vw=vh*W/H
    if vw>iw or vh>ih:  # fit inside, blurred backdrop
        s=min(W/iw,H/ih); fg=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
        k2=max(W/iw,H/ih)*1.1; bg=im.resize((int(iw*k2),int(ih*k2)),Image.BILINEAR)
        bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(40))
        bg=Image.eval(bg,lambda v:int(v*.42)); bg.paste(fg,((W-fg.width)//2,(H-fg.height)//2)); return bg
    px=min(max(cx*iw,vw/2),iw-vw/2); py=min(max(cy*ih,vh/2),ih-vh/2)
    return im.crop((int(px-vw/2),int(py-vh/2),int(px+vw/2),int(py+vh/2))).resize((W,H),Image.LANCZOS)
def text(im,lines,pos=None,size=46):
    f=sans(size)
    while max(f.getlength(x) for x in lines)>960: size-=2; f=sans(size)
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); lh=int(size*1.5)
    blk=len(lines)*lh-(lh-size); cy={'high':.2,'low':.8}.get(pos,.5); y=int(H*cy-blk/2)
    for i,ln in enumerate(lines): d.text((W/2,y+i*lh),ln,font=f,fill=(255,255,255,255),anchor='ma')
    a=np.asarray(lay)[:,:,3]; sh=Image.fromarray(np.clip(np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(7)),dtype=np.float32)*3.2,0,240).astype(np.uint8))
    base=im.convert('RGBA'); base=Image.alpha_composite(base,Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[sh])); return Image.alpha_composite(base,lay).convert('RGB')
def wrap(d,txt,f,maxw):
    words=txt.split(' '); out=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def fade(base,start=.48,peak=170):
    g=Image.new('L',(1,H),0)
    for y in range(H):
        t=max(0,(y-H*start)/(H*(1-start))); g.putpixel((0,y),int(peak*t**1.5))
    return Image.alpha_composite(base,Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[g.resize((W,H))]))
def text_bi(im,lines,en,size=46):
    """bilingual (2026-11-20): Japanese lower on the slide, small English under it near the bottom"""
    f=sans(size)
    while max(f.getlength(x) for x in lines)>960: size-=2; f=sans(size)
    base=fade(im.convert('RGBA'))
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); lh=int(size*1.5)
    fe=sans(27); el=wrap(d,en,fe,900)[:2]; elh=38
    eb=H-70-elh*len(el)                      # English block top
    y=int(eb-46-(len(lines)*lh-(lh-size)))   # Japanese block top
    for i,ln in enumerate(lines): d.text((W/2,y+i*lh),ln,font=f,fill=(255,255,255,255),anchor='ma')
    a=np.asarray(lay)[:,:,3]; sh=Image.fromarray(np.clip(np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(7)),dtype=np.float32)*3.2,0,240).astype(np.uint8))
    base=Image.alpha_composite(Image.alpha_composite(base,Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[sh])),lay)
    lay2=Image.new('RGBA',(W,H),(0,0,0,0)); d2=ImageDraw.Draw(lay2)
    for i,ln in enumerate(el): d2.text((W/2,eb+i*elh),ln,font=fe,fill=(232,226,214,215),anchor='ma')
    return Image.alpha_composite(base,lay2).convert("RGB")
def hook(im,lines,category,en=None):
    """first slide (2026-11-20): big bold title bottom-left on a dark fade + 'ETOI | category' label, uniform across the grid"""
    base=im.convert('RGBA'); g=Image.new('L',(1,H),0)
    for y in range(H):
        t=max(0,(y-H*.42)/(H*.58)); g.putpixel((0,y),int(225*t**1.3))
    shade=Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[g.resize((W,H))]); base=Image.alpha_composite(base,shade)
    size=78; f=bold(size)
    while max(f.getlength(x) for x in lines)>936: size-=2; f=bold(size)
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); lh=int(size*1.36)
    y=H-165-lh*len(lines)-(52 if en else 0)
    for i,ln in enumerate(lines): d.text((72,y+i*lh),ln,font=f,fill=(255,255,255,255))
    if en: d.text((74,H-172),wrap(d,en,sans(27),930)[0],font=sans(27),fill=(232,226,214,225))
    lab='ETOI ｜ '+category if category else 'ETOI'
    d.text((74,H-118),lab,font=serif(30),fill=(236,231,220,235))
    return Image.alpha_composite(base,lay).convert('RGB')
def mark(im):
    d=ImageDraw.Draw(im); d.text((W-36,H-34),'ETOI',font=serif(26),fill=(255,255,255),anchor='rs',stroke_width=2,stroke_fill=(0,0,0))
    return im
def mockup(k):
    im=Image.new('RGB',(W,H),(214,210,202)); g=np.linspace(0,1,H)[:,None]
    arr=(np.asarray(im,dtype=np.float32)*(1.06-.16*g[:,:,None])).clip(0,255).astype(np.uint8); im=Image.fromarray(arr)
    src=SRC[k]; mw,mh=760,900; s=min(mw/src.width,mh/src.height); art=src.resize((int(src.width*s),int(src.height*s)),Image.LANCZOS)
    fw=art.width+56; fh=art.height+56; x=(W-fw)//2; y=150+(mh-art.height)//2
    sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).rectangle([x+10,y+24,x+fw+10,y+fh+24],fill=150); sh=sh.filter(ImageFilter.GaussianBlur(22))
    im.paste((60,55,50),(0,0),sh); d=ImageDraw.Draw(im)
    d.rectangle([x,y,x+fw,y+fh],fill=(38,32,26)); d.rectangle([x+14,y+14,x+fw-14,y+fh-14],fill=(246,243,236)); im.paste(art,(x+28,y+28))
    d.text((W/2,y+fh+120),'ETOI',font=serif(64),fill=INK,anchor='ma'); d.text((W/2,y+fh+200),'答えのない世界で、自分の答えを描く。',font=serif(30),fill=INK,anchor='ma')
    return im
for i,s in enumerate(C.SLIDES):
    if s.get('mock'): im=mockup(s['img'])
    else:
        im=view(s['img'],s['cam'])
        if i==0 and hasattr(C,'CATEGORY') and s.get('t'): im=hook(im,s['t'],C.CATEGORY,s.get('en'))
        elif s.get('t') and s.get('en'): im=text_bi(im,s['t'],s['en'],s.get('size',40))
        elif s.get('t'): im=text(im,s['t'],s.get('pos'),s.get('size',40))
    im.save(f'{OUT}/{i+1:02d}.jpg',quality=90,optimize=True)
if hasattr(C,'CAPTION'): open(f'{OUT}/caption.txt','w').write(C.CAPTION.strip()+'\n')
th=[Image.open(f'{OUT}/{i+1:02d}.jpg').resize((270,360)) for i in range(len(C.SLIDES))]
cols=6; rows=(len(th)+cols-1)//cols; sheet=Image.new('RGB',(270*cols,360*rows))
for i,t in enumerate(th): sheet.paste(t,((i%cols)*270,(i//cols)*360))
sheet.save(f'{OUT}/_sheet.jpg',quality=85); print(len(th))
