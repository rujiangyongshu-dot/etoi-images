"""実験リール（reels/RID/ に cfg.py・meta.json、動画は reels/RID.mp4）を、Instagram の音楽を付けて公開する。
usage: python3 publish_reel3.py TOKEN_FILE RID [--publish]
  meta.json: {"caption": "...", "audio_ids": ["id1","id2"], "format": "F01", ...}
  リールのタブだけに表示（share_to_feed=false）。曲が付かなければ公開しない。1回の実行で公開は1本。
"""
import sys, json, time, urllib.request, urllib.parse
tok = open(sys.argv[1]).read().strip(); RID = sys.argv[2]; PUB = '--publish' in sys.argv
IG = '17841474297409504'; G = 'https://graph.facebook.com/v25.0/'
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
import re
meta = json.load(urllib.request.urlopen(RAW + f'reels/{RID}/meta.json', timeout=30))
caption = meta['caption'][:2200]
cfg = urllib.request.urlopen(RAW + f'reels/{RID}/cfg.py', timeout=30).read().decode('utf-8')
def exists(u):
    try: urllib.request.urlopen(urllib.request.Request(u, method='HEAD'), timeout=30); return True
    except Exception: return False
# ルールの検査（2026-11-21）：満たさないものは公開しない
prob = []
ts = [l for l in cfg.splitlines() if "'t':" in l]
if not ts: prob.append('cfg.py に字幕がない')
miss = [i + 1 for i, l in enumerate(ts) if "'en':" not in l]
if miss: prob.append(f'英語字幕のないショット: {miss}')
if '🌐 English' not in caption: prob.append('キャプションに 🌐 English がない')
tags = re.findall(r'#\S+', caption.strip().splitlines()[-1])
if len(tags) > 5: prob.append('ハッシュタグが5個を超える')
if not exists(RAW + f'reels/{RID}.mp4'): prob.append('動画がない')
if not exists(RAW + f'reels/{RID}/story.jpg'): prob.append('ストーリー画像がない')
if prob: raise SystemExit(json.dumps({'error': 'rule_gate', 'rid': RID, 'problems': prob}, ensure_ascii=False))
c = used = None; errs = []
for aid in meta['audio_ids']:
    d = {'media_type': 'REELS', 'video_url': RAW + f'reels/{RID}.mp4', 'caption': caption, 'share_to_feed': 'false',
         'audio_configuration': json.dumps({'audio_id': str(aid), 'audio_volume': 100, 'video_volume': 0})}
    if meta.get('cover'): d['cover_url'] = RAW + f'reels/{RID}/' + meta['cover']
    r = call(IG + '/media', d)
    if 'id' not in r: errs.append({aid: r.get('error')}); continue
    for _ in range(100):
        s = call(r['id'] + '?fields=status_code,status')
        if s.get('status_code') == 'FINISHED': c, used = r['id'], aid; break
        if s.get('status_code') in ('ERROR', 'EXPIRED') or 'error' in s: errs.append({aid: s}); break
        time.sleep(8)
    if c: break
if not c: raise SystemExit(json.dumps({'error': 'no container with music', 'detail': errs}, ensure_ascii=False))
if not PUB: print(json.dumps({'reel': {'dry_run': c, 'audio_id': used}})); raise SystemExit
p = call(IG + '/media_publish', {'creation_id': c})
if 'id' not in p: raise SystemExit(json.dumps({'error': p}, ensure_ascii=False))
m = p['id']; time.sleep(5); info = call(m + '?fields=permalink,media_audio_type')
story = {'status': 'failed'}
for _ in range(2):
    r = call(IG + '/media', {'image_url': RAW + f'reels/{RID}/story.jpg', 'media_type': 'STORIES'})
    if 'id' in r:
        for _ in range(30):
            s2 = call(r['id'] + '?fields=status_code')
            if s2.get('status_code') == 'FINISHED': break
            time.sleep(6)
        q = call(IG + '/media_publish', {'creation_id': r['id']})
        if 'id' in q: story = {'status': 'published', 'media_id': q['id']}; break
    story = {'status': 'failed', 'reason': str(r)[:200]}; time.sleep(45)
print(json.dumps({'reel': {'rid': RID, 'media_id': m, 'permalink': info.get('permalink', ''), 'audio_id': used,
                           'media_audio_type': info.get('media_audio_type', info.get('error', '')), 'format': meta.get('format')}, 'story': story}, ensure_ascii=False))
