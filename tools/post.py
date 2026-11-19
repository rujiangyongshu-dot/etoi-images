import sys,json,time,urllib.request,urllib.parse
# usage: python3 post.py TOKENFILE CAPTIONFILE URLSFILE [--publish]
tok=open(sys.argv[1]).read().strip(); cap=open(sys.argv[2],encoding='utf-8').read().strip()
urls=[l.strip() for l in open(sys.argv[3]) if l.strip()]; pub='--publish' in sys.argv
IG='17841474297409504'; G='https://graph.facebook.com/v21.0/'
def call(path,data=None):
    if data is None: req=G+path+('&' if '?' in path else '?')+'access_token='+tok; r=urllib.request.urlopen(req)
    else:
        data=dict(data,access_token=tok); r=urllib.request.urlopen(urllib.request.Request(G+path,urllib.parse.urlencode(data).encode()))
    return json.load(r)
def wait(cid):
    for _ in range(30):
        s=call(cid+'?fields=status_code')['status_code']
        if s=='FINISHED': return
        if s in('ERROR','EXPIRED'): raise SystemExit('container '+cid+' '+s)
        time.sleep(3)
    raise SystemExit('timeout '+cid)
assert 2<=len(urls)<=10, len(urls)
kids=[]
for u in urls:
    c=call(IG+'/media',{'image_url':u,'is_carousel_item':'true'})['id']; kids.append(c)
for c in kids: wait(c)
car=call(IG+'/media',{'media_type':'CAROUSEL','children':','.join(kids),'caption':cap})['id']; wait(car)
if not pub: print('DRYRUN_OK',car); raise SystemExit
m=call(IG+'/media_publish',{'creation_id':car})['id']
print('PUBLISHED',m, call(m+'?fields=permalink').get('permalink',''))
