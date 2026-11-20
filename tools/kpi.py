"""投稿ごとの数字をいま取る（KPI点検タスク用）。
usage: python3 kpi.py TOKEN_FILE [日数=7]
直近N日の投稿（フィード・リール）について、views, reach, likes, comments, saved, shares, profile_visits, follows,
total_interactions（リールは平均視聴秒数も）と、アカウントのフォロワー数・きょうのリーチを JSON で出す。トークンは表示しない。
"""
import sys, json, datetime, urllib.request, urllib.parse
T = open(sys.argv[1]).read().strip(); DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 7
IG = '17841474297409504'; G = 'https://graph.facebook.com/v25.0/'
JST = datetime.timezone(datetime.timedelta(hours=9)); now = datetime.datetime.now(JST)
errs = []
def get(p, **q):
    try: return json.load(urllib.request.urlopen(G + p + '?' + urllib.parse.urlencode(dict(q, access_token=T)), timeout=60))
    except urllib.error.HTTPError as e:
        errs.append(p.split('/')[-1] + ' ' + q.get('metric', '') + ' ' + e.read().decode(errors='replace')[:120]); return None
acc = get(IG, fields='followers_count,media_count') or {}
for m in ['reach', 'views', 'profile_views', 'accounts_engaged']:
    r = get(IG + '/insights', metric=m, period='day', metric_type='total_value')
    if r and r.get('data'): acc['today_' + m] = r['data'][0].get('total_value', {}).get('value')
out = []
r = get(IG + '/media', fields='id,timestamp,media_product_type,permalink,like_count,comments_count', limit=50) or {}
for x in r.get('data', []):
    t = datetime.datetime.strptime(x['timestamp'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc).astimezone(JST)
    if (now - t).days >= DAYS: continue
    mets = ['views', 'reach', 'likes', 'comments', 'saved', 'shares', 'total_interactions']
    mets += ['profile_visits', 'follows'] if x['media_product_type'] != 'REELS' else ['ig_reels_avg_watch_time']
    v = {'id': x['id'], 'type': x['media_product_type'], 'posted': t.strftime('%Y/%m/%d %H:%M'),
         'elapsed_h': round((now - t).total_seconds() / 3600, 1), 'permalink': x['permalink']}
    ins = get(x['id'] + '/insights', metric=','.join(mets))
    if ins is None and x['media_product_type'] == 'REELS':
        ins = get(x['id'] + '/insights', metric='views,reach,likes,comments,saved,shares,total_interactions')
    for d in (ins or {}).get('data', []):
        v[d['name']] = d['values'][0]['value']
    if 'ig_reels_avg_watch_time' in v: v['avg_watch_s'] = round(v.pop('ig_reels_avg_watch_time') / 1000, 1)
    out.append(v)
print(json.dumps({'measured': now.strftime('%Y/%m/%d %H:%M'), 'account': acc, 'media': out, 'errors': errs[:10]}, ensure_ascii=False))
