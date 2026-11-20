"""読み解きリール（reels/NN.mp4, reel2.py で作成）を、Instagram 音楽ライブラリの曲を付けて公開する。
usage: python3 publish_reel2.py TOKEN_FILE NN AUDIO_ID[,AUDIO_ID2,...] "HOOK LINE" [--publish]
  AUDIO_ID は music.py で探す。最初の曲で失敗したら次の曲を試す。全部失敗したら公開しない（音なしでは出さない）。
  公開後、media_audio_type（MUSIC になっているか）も返す。トークンは表示しない。1回の実行で公開するのは1本だけ。
"""
import sys, json, time, urllib.request, urllib.parse

tok = open(sys.argv[1]).read().strip()
NN = '%02d' % int(sys.argv[2])
AIDS = [a.strip() for a in sys.argv[3].split(',') if a.strip()]
hook = sys.argv[4].strip()
PUB = '--publish' in sys.argv
IG = '17841474297409504'
G = 'https://graph.facebook.com/v25.0/'
RAW = 'https://raw.githubusercontent.com/rujiangyongshu-dot/etoi-images/main/'


def call(path, data=None):
    try:
        if data is None:
            r = urllib.request.urlopen(G + path + ('&' if '?' in path else '?') + 'access_token=' + tok, timeout=60)
        else:
            r = urllib.request.urlopen(urllib.request.Request(G + path, urllib.parse.urlencode(dict(data, access_token=tok)).encode()), timeout=60)
        return json.load(r)
    except urllib.error.HTTPError as e:
        return {'error': e.read().decode(errors='replace')[:400]}


cap = urllib.request.urlopen(RAW + f'posts/{NN}/caption.txt', timeout=30).read().decode('utf-8').strip()
caption = f'{hook}\n\n▶ 全10枚の解説は @etoi.art の投稿で。保存して、あとで読み返せます。\n\n{cap}'[:2200]
c = None; used = None; errs = []
for aid in AIDS:
    r = call(IG + '/media', {'media_type': 'REELS', 'video_url': RAW + f'reels/{NN}.mp4', 'cover_url': RAW + f'posts/{NN}/01.jpg',
                             'caption': caption, 'share_to_feed': 'false',
                             'audio_configuration': json.dumps({'audio_id': aid, 'audio_volume': 100, 'video_volume': 0})})
    if 'id' not in r:
        errs.append({aid: r.get('error')}); continue
    for _ in range(100):
        s = call(r['id'] + '?fields=status_code,status')
        if s.get('status_code') == 'FINISHED':
            c, used = r['id'], aid; break
        if s.get('status_code') in ('ERROR', 'EXPIRED') or 'error' in s:
            errs.append({aid: s}); break
        time.sleep(6)
    if c: break
if not c:
    raise SystemExit(json.dumps({'error': 'no container with music', 'detail': errs}, ensure_ascii=False))
if not PUB:
    print(json.dumps({'reel': {'dry_run': c, 'audio_id': used}}))
    raise SystemExit
p = call(IG + '/media_publish', {'creation_id': c})
if 'id' not in p:
    raise SystemExit(json.dumps({'error': p}, ensure_ascii=False))
m = p['id']; time.sleep(5)
info = call(m + '?fields=permalink,media_audio_type')
print(json.dumps({'reel': {'media_id': m, 'permalink': info.get('permalink', ''), 'audio_id': used,
                           'media_audio_type': info.get('media_audio_type', info.get('error', ''))}}, ensure_ascii=False))
