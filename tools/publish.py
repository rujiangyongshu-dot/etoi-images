"""Publish one ETOI post (carousel + its story) through the Instagram Graph API.
usage: python3 publish.py TOKEN_FILE NN [--publish]
  - slides:  https://raw.githubusercontent.com/rujiangyongshu-dot/etoi-images/main/posts/NN/01.jpg ... 10.jpg
  - caption: .../posts/NN/caption.txt
  - story:   .../stories/NN.jpg (published right after the carousel, only if the carousel succeeded)
Without --publish it only builds the containers (dry run) and publishes nothing.
Prints one JSON line: {"feed": {...}, "story": {...}}. The token is never printed.
"""
import sys, json, time, urllib.request, urllib.parse

tok = open(sys.argv[1]).read().strip()
NN = '%02d' % int(sys.argv[2])
PUB = '--publish' in sys.argv
IG = '17841474297409504'
G = 'https://graph.facebook.com/v21.0/'
RAW = 'https://raw.githubusercontent.com/rujiangyongshu-dot/etoi-images/main/'


def call(path, data=None):
    try:
        if data is None:
            r = urllib.request.urlopen(G + path + ('&' if '?' in path else '?') + 'access_token=' + tok, timeout=60)
        else:
            r = urllib.request.urlopen(urllib.request.Request(G + path, urllib.parse.urlencode(dict(data, access_token=tok)).encode()), timeout=60)
        return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(json.dumps({'error': e.read().decode(errors='replace')[:400]}, ensure_ascii=False))


def exists(url):
    try:
        urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=30)
        return True
    except Exception:
        return False


def wait(cid, label):
    for _ in range(60):
        s = call(cid + '?fields=status_code')['status_code']
        if s == 'FINISHED':
            return
        if s in ('ERROR', 'EXPIRED'):
            raise SystemExit(json.dumps({'error': label + ' container ' + s}))
        time.sleep(3)
    raise SystemExit(json.dumps({'error': label + ' timeout'}))


cap = urllib.request.urlopen(RAW + f'posts/{NN}/caption.txt', timeout=30).read().decode('utf-8').strip()
first = cap.splitlines()[0].replace('🎨', '').strip()
title = first.split('（')[0].strip()
painter = ''
for l in cap.splitlines()[1:4]:
    if l.startswith('—'):
        painter = l.lstrip('— ').split('（')[0].strip()
        break
urls = [RAW + f'posts/{NN}/{i:02d}.jpg' for i in range(1, 11) if exists(RAW + f'posts/{NN}/{i:02d}.jpg')]
assert 2 <= len(urls) <= 10, len(urls)

kids = []
for i, u in enumerate(urls, 1):
    alt = f'{painter}《{title}》' if painter else f'《{title}》'
    alt += '。額装した作品の全体とETOIのロゴ' if i == len(urls) else f'の解説スライド{i}枚目（作品の部分と字幕）'
    kids.append(call(IG + '/media', {'image_url': u, 'is_carousel_item': 'true', 'alt_text': alt[:1000]})['id'])
for c in kids:
    wait(c, 'slide')
car = call(IG + '/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': cap})['id']
wait(car, 'carousel')
if not PUB:
    print(json.dumps({'feed': {'dry_run': car, 'slides': len(urls)}}, ensure_ascii=False))
    raise SystemExit
m = call(IG + '/media_publish', {'creation_id': car})['id']
feed = {'media_id': m, 'permalink': call(m + '?fields=permalink').get('permalink', '')}

story = {'status': 'no image'}
su = RAW + f'stories/{NN}.jpg'
if exists(su):
    try:
        c = call(IG + '/media', {'image_url': su, 'media_type': 'STORIES'})['id']
        wait(c, 'story')
        story = {'status': 'published', 'media_id': call(IG + '/media_publish', {'creation_id': c})['id']}
    except SystemExit as e:
        story = {'status': 'failed', 'reason': str(e)[:300]}
print(json.dumps({'feed': feed, 'story': story}, ensure_ascii=False))
