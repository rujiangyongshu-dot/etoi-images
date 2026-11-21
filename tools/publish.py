"""Publish one ETOI post (carousel + its 3 stories) through the Instagram Graph API.
usage: python3 publish.py TOKEN_FILE NN [--publish]
  - slides:  .../posts/NN/01.jpg ... 10.jpg, caption: .../posts/NN/caption.txt, cfg: .../posts/NN/cfg.py
  - stories: .../stories/NN.jpg, NN_2.jpg, NN_3.jpg (published right after the carousel)
Without --publish it only checks the rules and builds the containers (dry run).
Prints one JSON line. The token is never printed.

2026-11-21 hardening (owner: 「決めたルールが世に出るものに必ず反映されていること」「二重投稿・ストーリー停止を二度と起こさない」):
  1. RULE GATE: refuses to publish (prints {"error":"rule_gate", ...}) if the post breaks a current rule:
     every text slide in cfg.py has 'en' (English subtitle), caption has '🌐 English', at most 5 hashtags, no '#ETOI', stories/NN.jpg exists.
  2. NO DUPLICATES: if a post with the same first caption line was published in the last 14 days, it does not post again;
     it prints {"feed":{"already":...}} so the task marks the row 済.
  3. If media_publish errors, it checks whether the post went live anyway before reporting an error.
  4. Stories are always attempted after the carousel is live (retries), each story separately.
  5. Fewer API calls (status polling every 8 s) to stay under the app rate limit.
"""
import sys, json, time, re, datetime, urllib.request, urllib.parse

tok = open(sys.argv[1]).read().strip()
NN = '%02d' % int(sys.argv[2])
PUB = '--publish' in sys.argv
IG = '17841474297409504'
G = 'https://graph.facebook.com/v21.0/'
RAW = 'https://raw.githubusercontent.com/rujiangyongshu-dot/etoi-images/main/'


class ApiError(Exception):
    pass


def call(path, data=None, tries=2):
    for k in range(tries):
        try:
            if data is None:
                r = urllib.request.urlopen(G + path + ('&' if '?' in path else '?') + 'access_token=' + tok, timeout=60)
            else:
                r = urllib.request.urlopen(urllib.request.Request(G + path, urllib.parse.urlencode(dict(data, access_token=tok)).encode()), timeout=60)
            return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='replace')[:400]
            if k + 1 < tries and ('"is_transient":true' in msg or e.code >= 500):
                time.sleep(20); continue
            raise ApiError(msg)
        except Exception as e:
            if k + 1 < tries:
                time.sleep(20); continue
            raise ApiError(str(e)[:300])


def fetch(url):
    try:
        return urllib.request.urlopen(url, timeout=30).read().decode('utf-8')
    except Exception:
        return None


def exists(url):
    try:
        urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=30)
        return True
    except Exception:
        return False


def wait(cid, label):
    for _ in range(40):
        s = call(cid + '?fields=status_code').get('status_code')
        if s == 'FINISHED':
            return
        if s in ('ERROR', 'EXPIRED'):
            raise ApiError(label + ' container ' + s)
        time.sleep(8)
    raise ApiError(label + ' timeout')


def out(obj):
    print(json.dumps(obj, ensure_ascii=False)); raise SystemExit


cap = (fetch(RAW + f'posts/{NN}/caption.txt') or '').strip()
cfg = fetch(RAW + f'posts/{NN}/cfg.py') or ''
first = cap.splitlines()[0].strip() if cap else ''

# 1. rule gate
problems = []
if not cap: problems.append('caption.txt がない')
text_slides = [l for l in cfg.splitlines() if "'t':" in l and "'img'" in l]
if not text_slides: problems.append('cfg.py が読めない')
miss = [i + 1 for i, l in enumerate(text_slides) if "'en':" not in l]
if miss: problems.append(f'英語字幕のないスライド: {miss}')
if '🌐 English' not in cap: problems.append('キャプションに 🌐 English がない')
tags = re.findall(r'#\S+', cap.splitlines()[-1] if cap else '')
if len(tags) > 5: problems.append(f'ハッシュタグが{len(tags)}個（5個まで）')
if '#ETOI' in tags: problems.append('#ETOI が残っている')
if not exists(RAW + f'stories/{NN}.jpg'): problems.append('ストーリー画像がない')
if problems:
    out({'error': 'rule_gate', 'nn': NN, 'problems': problems})

title = first.replace('🎨', '').strip().split('（')[0].strip()
painter = ''
for l in cap.splitlines()[1:4]:
    if l.startswith('—'):
        painter = l.lstrip('— ').split('（')[0].strip(); break


def recent_same():
    r = call(IG + '/media?fields=id,timestamp,caption,permalink,media_product_type&limit=25')
    now = datetime.datetime.now(datetime.timezone.utc)
    for x in r.get('data', []):
        if x.get('media_product_type') != 'FEED': continue
        t = datetime.datetime.strptime(x['timestamp'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        if (now - t).days < 14 and (x.get('caption') or '').strip().splitlines()[:1] == [first]:
            return x
    return None


# 2. no duplicates
try:
    dup = recent_same()
except ApiError as e:
    out({'error': 'api', 'step': 'duplicate check', 'detail': str(e)})
if dup:
    out({'feed': {'already': dup['id'], 'permalink': dup.get('permalink', ''), 'timestamp': dup['timestamp']}, 'story': {'status': 'skipped (already posted)'}})

urls = [RAW + f'posts/{NN}/{i:02d}.jpg' for i in range(1, 11) if exists(RAW + f'posts/{NN}/{i:02d}.jpg')]
if not 2 <= len(urls) <= 10:
    out({'error': 'slides', 'count': len(urls)})
try:
    kids = []
    for i, u in enumerate(urls, 1):
        alt = f'{painter}《{title}》' if painter else f'《{title}》'
        alt += '。額装した作品の全体とETOIのロゴ' if i == len(urls) else f'の解説スライド{i}枚目（作品の部分と字幕）'
        kids.append(call(IG + '/media', {'image_url': u, 'is_carousel_item': 'true', 'alt_text': alt[:1000]})['id'])
    time.sleep(10)
    for c in kids:
        wait(c, 'slide')
    car = call(IG + '/media', {'media_type': 'CAROUSEL', 'children': ','.join(kids), 'caption': cap})['id']
    wait(car, 'carousel')
except ApiError as e:
    out({'error': 'api', 'step': 'containers', 'detail': str(e)})
if not PUB:
    out({'feed': {'dry_run': car, 'slides': len(urls)}, 'rule_gate': 'ok'})

# 3. publish, then confirm
feed = None
try:
    m = call(IG + '/media_publish', {'creation_id': car}, tries=1)['id']
    feed = {'media_id': m}
except ApiError as e:
    time.sleep(30)
    try:
        x = recent_same()
    except ApiError:
        x = None
    if not x:
        out({'error': 'api', 'step': 'publish', 'detail': str(e)})
    feed = {'media_id': x['id'], 'note': 'publish returned an error but the post is live'}
try:
    feed['permalink'] = call(feed['media_id'] + '?fields=permalink').get('permalink', '')
except ApiError:
    feed['permalink'] = ''

# 4. stories (each separately, with retry)
stories = []
for name in [f'{NN}.jpg', f'{NN}_2.jpg', f'{NN}_3.jpg']:
    su = RAW + 'stories/' + name
    if not exists(su):
        continue
    st = {'file': name}
    for attempt in range(2):
        try:
            c = call(IG + '/media', {'image_url': su, 'media_type': 'STORIES'})['id']
            wait(c, 'story')
            st['media_id'] = call(IG + '/media_publish', {'creation_id': c})['id']; st['status'] = 'published'
            break
        except ApiError as e:
            st['status'] = 'failed'; st['reason'] = str(e)[:200]
            time.sleep(45)
    stories.append(st)
print(json.dumps({'feed': feed, 'stories': stories,
                  'story': {'status': 'published' if any(s.get('status') == 'published' for s in stories) else 'failed'}}, ensure_ascii=False))
