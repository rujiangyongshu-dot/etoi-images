# v3 自動制作（11/27）型 F20 失敗作と呼ばれた名画（posts/55 マネ《鉄道》）昼 約31秒
# 構成：0-1秒 部屋→彼女の顔の寄り＋「マネに勝ったモデル」／1-3秒「13年後、思いもよらない立場に」を約束／1862モデル→1863オランピアで非難→最後の絵→1874入選→絵を学ぶ→1876入選・同年マネ落選で回収／「見られる側から描く側へ」で1ショット目へループ
IMAGES={'room':'../../rooms/55/room.jpg','d':'../../posts/55/src.jpg'}
CATEGORY='立場'
ENDCARD='裏方で支えている同僚に、送ってあげてください。'
DUR=[1.0,1.5,2.8,2.8,3.0,3.0,3.0,2.8,3.0,3.0,3.6]
END=1.8
XF=0.25
ZOOM=1.32
HSIZE=78
TSIZE=62
HOOK_Y=0.62
SLIDES=[
 {'img':'room','cam':(0.5,0.52,1.0),'t':['マネに勝った','モデル'],'size':170,'en':'The model who beat Manet.'},
 {'hook':True,'img':'d','cam':(0.24,0.335,0.22),'t':['マネに勝った','モデル'],'size':170,'en':'The model who beat Manet.'},
 {'hook':True,'img':'d','cam':(0.26,0.34,0.36),'t':['非難の的だった彼女は、','13年後、思いもよらない立場に。'],'en':'Once the target of scorn, 13 years later she stood somewhere no one expected.'},
 {'img':'d','cam':(0.24,0.36,0.42),'t':['1862年から、','彼女はマネのモデルを務める。'],'en':'From 1862, Victorine Meurent modeled for Manet.'},
 {'img':'d','cam':(0.22,0.30,0.30),'t':['1863年《オランピア》の裸婦。','絵は、激しい非難を浴びた。'],'en':'In 1863 she was the nude in "Olympia" — a painting met with fierce criticism.'},
 {'img':'d','cam':(0.26,0.70,0.32),'t':['膝には本と、眠る子犬。','マネが彼女を描いた、最後の絵だ。'],'en':'A book and a sleeping puppy on her lap: the last painting Manet made of her.'},
 {'img':'d','cam':(0.62,0.42,0.55),'t':['1874年、この絵は','国の展覧会「サロン」に入選。'],'en':'In 1874 this painting was accepted at the Salon, the official exhibition.'},
 {'img':'d','cam':(0.24,0.33,0.26),'t':['そのころ彼女は、','自ら絵を学び始めていた。'],'en':'Around then, she began to study painting herself.'},
 {'img':'d','cam':(0.30,0.45,0.60),'t':['1876年、サロンの審査。','彼女の絵は、入選した。'],'en':'1876, the Salon jury: her painting was accepted.'},
 {'img':'d','cam':(0.50,0.50,1.00),'t':['同じ年、','マネの絵は落とされた。'],'en':"That same year, Manet's entry was rejected."},
 {'img':'d','cam':(0.24,0.335,0.22),'t':['見られる側から、描く側へ。','その一歩は、今日からでも。'],'en':'From being looked at to being the one who paints. That step can start today.'},
 {'img':'d','mock':True},
]
