# v3 自動制作（11/27）型 F27 シリーズ「名画が教える、逆転の法則 #1」（posts/08 ロイツェ《デラウェア川を渡るワシントン》）朝
# 構成：0-1秒 部屋の画像＋「ワシントンの奇襲」／1-2.5秒 ワシントンの顔の寄り／2.5-5秒「この小舟の行き先に国の運命」と約束／1776年12月 減っていく軍→雪の夜の渡河→目標トレントン→立って前を見る男（細部）→氷と舟の誇張・75年後のドイツ（細部）→奇襲成功・超大国の始まりで回収／負けが続く人へ「逆転は一夜の決断から」と返し、冒頭の「奇襲」へループ
IMAGES={'room':'../../rooms/08/room.jpg','d':'../../posts/08/src/master.jpg'}
CATEGORY='逆転'
ENDCARD='負けが続いている同僚に、送ってあげてください。'
DUR=[1.0,1.5,2.8,3.0,3.0,3.0,3.0,3.2,3.6,3.6]
END=1.8
XF=0.25
ZOOM=1.32
HSIZE=78
TSIZE=62
HOOK_Y=0.62
SLIDES=[
 {'img':'room','cam':(0.5,0.52,1.0),'t':['ワシントンの','奇襲'],'size':170,'en':"Washington's surprise attack."},
 {'hook':True,'img':'d','cam':(0.425,0.40,0.40),'t':['ワシントンの','奇襲'],'size':170,'en':"Washington's surprise attack."},
 {'hook':True,'img':'d','cam':(0.50,0.55,0.62),'t':['この小さな舟に、','アメリカの運命がかかっていた。'],'en':'The fate of America rode on this little boat.'},
 {'img':'d','cam':(0.50,0.50,1.00),'t':['1776年、ワシントンの軍は','負け続け、兵も逃げていた。'],'en':'In 1776, Washington’s army kept losing, and soldiers were deserting.'},
 {'img':'d','cam':(0.12,0.62,0.55),'t':['そこで彼は、雪の夜に','凍った川を渡ると決めた。'],'en':'So he decided to cross a frozen river on a snowy night.'},
 {'img':'d','cam':(0.86,0.50,0.55),'t':['狙いは、川の向こうで','眠っている敵の町。'],'en':'The target: an enemy town asleep across the river.'},
 {'img':'d','cam':(0.43,0.45,0.50),'t':['揺れる舟で、一人だけ','立って前を見ているのが彼だ。'],'en':'In the rocking boat, he alone stands, looking ahead.'},
 {'img':'d','cam':(0.40,0.80,0.50),'t':['ちなみにこの絵、描かれたのは','75年後のドイツ。'],'en':'By the way, this was painted 75 years later, in Germany.'},
 {'img':'d','cam':(0.60,0.55,0.80),'t':['奇襲は大成功。今のアメリカは、','この一夜から始まった。'],'en':'The surprise attack worked. Today’s America began with that one night.'},
 {'img':'d','cam':(0.425,0.40,0.42),'t':['負け続きでも、','逆転は一晩の決断で始まる。'],'en':'Even after many losses, a comeback can start with one night’s decision.'},
 {'img':'d','mock':True},
]
