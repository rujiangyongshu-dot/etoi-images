"""Publish reels/NN.mp4 as an Instagram Reel (also shown in the feed grid), cover = posts/NN/01.jpg.
usage: python3 publish_reel.py TOKEN_FILE NN "HOOK LINE" [--publish]
Caption = hook line + pointer to the full carousel + the carousel's caption (credits, sources, hashtags).
Prints one JSON line. The token is never printed.
"""
import sys, json, time, urllib.request, urllib.parse

tok = open(sys.argv[1]).read().strip()
NN = '%02d' % int(sys.argv[2])
hook = sys.argv[3].strip()
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


cap = urllib.request.urlopen(RAW + f'posts/{NN}/caption.txt', timeout=30).read().decode('utf-8').strip()
caption = f'{hook}\n\n▶ 全10枚の解説は @etoi.art の投稿で。保存して、あとで読み返せます。\n\n{cap}'[:2200]
c = call(IG + '/media', {'media_type': 'REELS', 'video_url': RAW + f'reels/{NN}.mp4', 'cover_url': RAW + f'posts/{NN}/01.jpg',
                         'caption': caption, 'share_to_feed': 'true'})['id']
for _ in range(100):
    s = call(c + '?fields=status_code,status')
    if s.get('status_code') == 'FINISHED':
        break
    if s.get('status_code') in ('ERROR', 'EXPIRED'):
        raise SystemExit(json.dumps({'error': 'reel container ' + str(s.get('status'))}, ensure_ascii=False))
    time.sleep(6)
else:
    raise SystemExit(json.dumps({'error': 'reel timeout'}))
if not PUB:
    print(json.dumps({'reel': {'dry_run': c}}))
    raise SystemExit
m = call(IG + '/media_publish', {'creation_id': c})['id']
print(json.dumps({'reel': {'media_id': m, 'permalink': call(m + '?fields=permalink').get('permalink', '')}}, ensure_ascii=False))
