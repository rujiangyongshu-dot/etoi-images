# v3 自動制作（11/27）型 F19 ライバル・嫉妬（posts/60 ボッティチェリ《ジュリアーノ・デ・メディチ》）昼
# 構成：0-1秒 部屋の画像＋「ライバルに殺されたメディチ」／1-2.5秒 伏せた目の寄り／2.5-5秒「殺した側と殺された側、最後に残ったのは？」と約束／1478 対立する銀行家一族の襲撃→24歳・19か所→兄は聖具室へ→処刑された首謀者を画家が壁に→伏せたまぶた・キジバト（細部）→1494 壁の首謀者は消される→殺された側の顔が国立美術館に残るで回収／競争に疲れた人へ返す
IMAGES={'room':'../../rooms/60/room.jpg','d':'../../posts/60/src.jpg'}
CATEGORY='ライバル'
ENDCARD='ライバルとの競争に疲れた同僚に、送ってあげてください。'
DUR=[1.0,1.5,2.8,3.2,3.0,3.0,3.2,3.2,3.0,3.4,3.6]
END=1.8
XF=0.25
ZOOM=1.32
HSIZE=78
TSIZE=62
HOOK_Y=0.62
SLIDES=[
 {'img':'room','cam':(0.5,0.52,1.0),'t':['ライバルに殺された','メディチ'],'size':150,'en':'A Medici, killed by his rivals.'},
 {'hook':True,'img':'d','cam':(0.58,0.355,0.24),'t':['ライバルに殺された','メディチ'],'size':150,'en':'A Medici, killed by his rivals.'},
 {'hook':True,'img':'d','cam':(0.55,0.40,0.60),'t':['殺した側と、殺された側。','最後に勝ったのは、どっちだ。'],'en':'The killers or the killed: who won in the end?'},
 {'img':'d','cam':(0.30,0.20,0.40),'t':['1478年、ライバルの一族が','教会でメディチ兄弟を襲った。'],'en':'In 1478, a rival family attacked the Medici brothers in church.'},
 {'img':'d','cam':(0.55,0.42,0.62),'t':['弟のジュリアーノは24歳。','19か所も刺されて亡くなった。'],'en':'The younger brother, 24, was stabbed 19 times and died.'},
 {'img':'d','cam':(0.50,0.66,0.50),'t':['兄は首を切られながらも、','部屋に逃げ込んで助かった。'],'en':'His older brother, wounded in the neck, escaped into a side room.'},
 {'img':'d','cam':(0.70,0.55,0.50),'t':['犯人たちは処刑され、その姿は','さらし者として壁に描かれた。'],'en':'The attackers were executed, and painted on a wall in shame.'},
 {'img':'d','cam':(0.20,0.82,0.36),'t':['同じ画家は、殺された弟も描いた。','伏せた目は、死の印だ。'],'en':'The same painter also painted the murdered brother. The lowered eyes mark his death.'},
 {'img':'d','cam':(0.30,0.30,0.55),'t':['16年後、壁の犯人たちの絵は','消されてしまう。'],'en':'Sixteen years later, the wall painting of the attackers was erased.'},
 {'img':'d','cam':(0.55,0.50,0.86),'t':['残ったのは、殺された弟の顔。','今はアメリカの国立美術館にある。'],'en':'What remains is the murdered brother’s face, now in America’s National Gallery.'},
 {'img':'d','cam':(0.60,0.31,0.30),'t':['勝ち負けは、いつか忘れられる。','残るのは、心を込めた仕事だ。'],'en':'Wins and losses fade. Work done with heart remains.'},
 {'img':'d','mock':True},
]
