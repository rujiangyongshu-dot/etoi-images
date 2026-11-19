"""Download a public-domain artwork image and save it as a JPEG (long side <= 4000px).
usage: python3 tools/fetch.py URL OUT.jpg
Sources that work from the cloud: AIC IIIF (https://www.artic.edu/iiif/2/<image_id>/full/3000,/0/default.jpg),
Met (https://images.metmuseum.org/CRDImages/...), Wikimedia (https://upload.wikimedia.org/...)."""
import sys, io, urllib.request
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
url, out = sys.argv[1], sys.argv[2]
req = urllib.request.Request(url, headers={'User-Agent': 'ETOI-bot/1.0 (https://www.instagram.com/etoi.art/)'})
data = urllib.request.urlopen(req, timeout=120).read()
im = Image.open(io.BytesIO(data)).convert('RGB')
m = max(im.size)
if m > 4000:
    s = 4000 / m
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
im.save(out, quality=95)
print(out, im.size)
