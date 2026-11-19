"""Instagram音楽ライブラリ検索。usage: python3 music.py TOKEN_FILE "検索語" [検索語...]
各語の上位を表示（audio_id, 秒, 曲名, アーティスト）。リールには publish_reel2.py で audio_id を付ける。"""
import sys, json, urllib.request, urllib.parse
T = open(sys.argv[1]).read().strip(); IG = '17841474297409504'
def search(q):
    u = 'https://graph.facebook.com/v25.0/ig_audio?' + urllib.parse.urlencode(dict(audio_type='music', ig_user_id=IG, search_query=q, access_token=T))
    return json.load(urllib.request.urlopen(u)).get('audio', [])
if __name__ == '__main__':
    for q in sys.argv[2:]:
        print('==', q)
        for a in search(q)[:8]:
            print(' ', a['audio_id'], round(a.get('duration_in_ms', 0) / 1000), '|', a.get('title'), '|', a.get('display_artist'))
