# v3 自動制作（11/24）型 F13 常識の逆張り（posts/08 ロイツェ《デラウェア川を渡るワシントン》）昼
# 構成：0-1秒 ワシントンの寄り＋「間違いだらけのワシントン」／1-3秒「それでも描かれた理由は最後に」と約束／史実→所蔵館が挙げる間違い（向き・氷・舟・夜明け・75年後のドイツ）→理由で回収／完璧主義の人へ返し、冒頭の「間違いだらけ」へループ
IMAGES={'room':'../../rooms/08/room.jpg','d':'../../posts/08/src/master.jpg'}
CATEGORY='完璧主義'
ENDCARD='完璧主義でしんどい同僚に、送ってあげてください。'
DUR=[1.0,1.5,2.8,3.0,3.0,2.8,3.2,2.8,3.0,3.4,3.6]
END=1.8
XF=0.25
ZOOM=1.32
HSIZE=78
TSIZE=62
HOOK_Y=0.62
SLIDES=[
 {'img':'room','cam':(0.5,0.52,1.0),'t':['間違いだらけの','ワシントン'],'size':150,'en':'Washington, painted all wrong.'},
 {'hook':True,'img':'d','cam':(0.425,0.42,0.42),'t':['間違いだらけの','ワシントン'],'size':150,'en':'Washington, painted all wrong.'},
 {'img':'d','cam':(0.45,0.45,0.60),'t':['史実と違うところだらけ。','それでも描かれた理由が、最後に。'],'hook':True,'en':'It is full of historical errors. Why it was painted this way comes at the end.'},
 {'img':'d','cam':(0.50,0.50,1.00),'t':['1776年12月、雪の夜。','減った兵で、凍る川を渡った。'],'en':'December 1776, a snowy night: with a shrinking army, he crossed an icy river.'},
 {'img':'d','cam':(0.80,0.48,0.60),'t':['対岸の英軍への奇襲は成功。','独立の戦いは、息を吹き返した。'],'en':'The surprise attack on the other side succeeded, and the fight for independence revived.'},
 {'img':'d','cam':(0.45,0.66,0.55),'t':['でも、所蔵館は言う。','舟は、逆向きに渡っている。'],'en':'But the museum points out: the boat is crossing in the wrong direction.'},
 {'img':'d','cam':(0.35,0.80,0.50),'t':['氷は大きすぎ、舟は小さすぎ。','実際の舟に、馬も大砲もなかった。'],'en':'The ice is too big, the boat too small, and the real boats carried no horses or cannon.'},
 {'img':'d','cam':(0.30,0.22,0.55),'t':['夜の出来事なのに、','描かれたのは夜明けの光。'],'en':'It happened at night, yet it is painted in the light of dawn.'},
 {'img':'d','cam':(0.62,0.55,0.75),'t':['しかも描かれたのは、75年後。','ドイツで、ライン川を見立てて。'],'en':'And it was painted 75 years later, in Germany, with the Rhine standing in for the Delaware.'},
 {'img':'d','cam':(0.425,0.40,0.40),'t':['正確さより、描きたかったのは','逆境で前を向く、その一瞬だろう。'],'en':'More than accuracy, the painter wanted that one moment of facing forward in hardship.'},
 {'img':'d','cam':(0.50,0.50,1.00),'t':['間違いだらけでも、いい。','前を向く姿は、ちゃんと伝わる。'],'en':'It is fine to be full of mistakes. Facing forward still comes through.'},
 {'img':'d','mock':True},
]
