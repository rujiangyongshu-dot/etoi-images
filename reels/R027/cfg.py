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
 {'hook':True,'img':'d','cam':(0.50,0.55,0.62),'t':['この小舟の行き先に、','一つの国の運命がかかっていた。'],'en':'The fate of a nation rode on where this small boat was going.'},
 {'img':'d','cam':(0.50,0.50,1.00),'t':['1776年12月、ワシントンの軍は','数を減らしていた。'],'en':"December 1776: Washington's army was dwindling."},
 {'img':'d','cam':(0.12,0.62,0.55),'t':['雪の降る夜、','氷の浮かぶ川を渡る。'],'en':'On a snowy night, they crossed a river full of ice.'},
 {'img':'d','cam':(0.86,0.50,0.55),'t':['目指すは対岸のトレントン。','英軍とヘッセン兵がいる町だ。'],'en':'The target across the river: Trenton, held by British and Hessian troops.'},
 {'img':'d','cam':(0.43,0.45,0.50),'t':['揺れる小舟で、ただ一人','立って前を見る男。'],'en':'In the rocking boat, one man stands and looks ahead.'},
 {'img':'d','cam':(0.40,0.80,0.50),'t':['氷は大きく、舟は小さく。','描かれたのは75年後のドイツ。'],'en':'The ice made bigger, the boat smaller: it was painted 75 years later, in Germany.'},
 {'img':'d','cam':(0.60,0.55,0.80),'t':['奇襲は成功した。今の超大国は、','雪の夜の小舟から始まった。'],'en':"The attack succeeded. Today's superpower began with a small boat on a snowy night."},
 {'img':'d','cam':(0.425,0.40,0.42),'t':['負けが続いても、逆転は','一夜の決断から始まる。'],'en':'Even after losses, a turnaround can begin with one night’s decision.'},
 {'img':'d','mock':True},
]
