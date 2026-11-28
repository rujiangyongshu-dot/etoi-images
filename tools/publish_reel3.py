"""実験リール（reels/RID/ に cfg.py・meta.json、動画は reels/RID.mp4）を、Instagram の音楽を付けて公開する。
usage: python3 publish_reel3.py TOKEN_FILE RID [--publish]
  meta.json: {"caption": "...", "audio_ids": ["id1","id2"], "format": "F01", ...}
  2026-11-28 オーナー決定：メイングリッドにも表示（share_to_feed=true。--nofeed で従来のリールタブのみ）。
  --trial=MANUAL のときはトライアル（フォロワー外だけ）。トライアルはストーリーを出さない。曲が付かなければ公開しない。1回の実行で公開は1本。
"""
import sys, json, time, urllib.request, urllib.parse
tok = open(sys.argv[1]).read().strip(); RID = sys.argv[2]; PUB = '--publish' in sys.argv
# 2026-11-28：トライアルリール（フォロワー外だけに試す）。--trial=SS_PERFORMANCE（伸びたら自動で全員に）／--trial=MANUAL
TRIAL = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--trial=')), None)
# 2026-11-28 オーナー決定：リールはメイングリッドにも出す（既定 true）
FEED = 'false' if '--nofeed' in sys.argv else 'true'
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
# 制作基準 v2（2026-11-22）：黒い画面から始めない／長さ16秒以内
first = next((l for l in cfg.splitlines() if "'t':" in l), '')
if "'img':None" in first.replace(' ', ''): prob.append('1ショット目が黒い画面（v2では絵の寄りから始める）')
try:
    ns = {}; exec(compile(cfg, 'cfg', 'exec'), {'__builtins__': {}}, ns)
    nshot = len([x for x in ns.get('SLIDES', []) if not x.get('mock')])
    total = sum(ns['DUR']) if ns.get('DUR') else (3.4 + 3.6 * max(0, nshot - 2) + 4.2)
    total += ns.get('END', 3.0)
    if total > 75: prob.append(f'長さ約{total:.0f}秒（75秒以内）')  # v3（11/23）：16秒上限は効果がなかったので撤廃
except Exception as e:
    prob.append('cfg.py を読めない: ' + str(e)[:60])
if prob: raise SystemExit(json.dumps({'error': 'rule_gate', 'rid': RID, 'problems': prob}, ensure_ascii=False))
c = used = None; errs = []
for aid in meta['audio_ids']:
    d = {'media_type': 'REELS', 'video_url': RAW + f'reels/{RID}.mp4', 'caption': caption, **({} if TRIAL else {'share_to_feed': FEED}), **({'trial_params': json.dumps({'graduation_strategy': TRIAL})} if TRIAL else {}),
         'audio_configuration': json.dumps({'audio_id': str(aid), 'audio_volume': 70 if meta.get('narration') else 100, 'video_volume': 100})}
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
story = {'status': 'skipped_trial'} if TRIAL else {'status': 'failed'}
for _ in (range(0) if TRIAL else range(2)):
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
