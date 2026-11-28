"""曲の出だしの強さを測る（2026-11-28 オーナー：最初の0.5〜1秒でBGMが聞こえること）。
python3 tools/music_intro.py TOKEN "検索語" ...   → 候補を出だしの強さ順に表示
関数 intro_score(TOKEN, audio_id) → 0〜1（最初の0.5秒の音量 ÷ 曲全体の中央値の音量。0.6以上を合格）"""
import sys, json, subprocess, urllib.request, urllib.parse, tempfile, os
import numpy as np
IG = '17841474297409504'
def _search(T, q):
    u = 'https://graph.facebook.com/v25.0/ig_audio?' + urllib.parse.urlencode(dict(audio_type='music', ig_user_id=IG, search_query=q, access_token=T))
    return json.load(urllib.request.urlopen(u)).get('audio', [])
def _pcm(url):
    f = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    urllib.request.urlretrieve(url, f)
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-t', '40', '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
    os.remove(f); return np.frombuffer(raw, np.int16).astype(np.float32)
def score_pcm(a, sr=8000):
    if len(a) < sr: return 0.0
    win = sr // 10; rms = np.sqrt(np.array([np.mean(a[i:i + win] ** 2) for i in range(0, len(a) - win, win)]) + 1)
    med = np.median(rms); return float(min(1.0, np.mean(rms[:5]) / med)) if med > 0 else 0.0
def intro_score(T, aid, url=None):
    if not url:
        return None
    return round(score_pcm(_pcm(url)), 2)
if __name__ == '__main__':
    T = open(sys.argv[1]).read().strip(); seen = {}
    for q in sys.argv[2:]:
        for a in _search(T, q)[:8]:
            if a['audio_id'] in seen: continue
            try: s = intro_score(T, a['audio_id'], a.get('download_url'))
            except Exception as e: s = None
            seen[a['audio_id']] = (s, a.get('title'), a.get('display_artist'), round(a.get('duration_in_ms', 0) / 1000))
    for aid, (s, t, ar, d) in sorted(seen.items(), key=lambda x: -(x[1][0] or 0)):
        print(aid, s, d, '|', t, '|', ar)
