

#current_map = '■中央プラトン街道 ／ ブルンネンシュティグ入口付近.png'
#current_pos2pixel = (184,149, 378,153 ) 

'''
https://yotsuba000.github.io/YotsubaDataBase/MapDataBase/Map/[010]G13.rmd/[010]G13.rmd.xml

<MapName>中央プラトン街道 / ブルンネンシュティグ入口付近</MapName>
<SysWidth>195</SysWidth>
<SysHeight>180</SysHeight>
<TgaWidth>400</TgaWidth>
<TgaHeight>185</TgaHeight>
<MapType>1</MapType>
'''



#current_map = '■中央プラトン街道 ／ グレートフォレスト入口付近.png'
#current_pos2pixel = (248,307,400,248 ) 

'''
<MapName>中央プラトン街道 / グレートフォレスト入口付近</MapName>
<SysWidth>250</SysWidth>
<SysHeight>310</SysHeight>
<TgaWidth>400</TgaWidth>
<TgaHeight>248</TgaHeight>
<MapType>1</MapType>
<isPremiumMap>0</isPremiumMap>
'''

# default
#current_map = '■古都ブルンネンシュティグ.png' 
#current_pos2pixel = (66,168, 178,230)
#current_pos2pixel = (205,185,554,250) 

'''

<MapName>古都ブルンネンシュティグ</MapName>
<SysWidth>205</SysWidth>
<SysHeight>185</SysHeight>
<TgaWidth>554</TgaWidth>
<TgaHeight>250</TgaHeight>
<MapType>2</MapType>
<isPremiumMap>0</isPremiumMap>
<isPvPMap>0</isPvPMap>
'''

################


# global objects

status = {
    "fieldName": None, 
    "mapName": None, 
    # "current_pos2pixel": None, 
    "TgaWidth"   :None, 
    "TgaHeight"  :None, 
    "SysWidth"   :None,
    "SysHeight"  :None, 

    "pos" : (0,0), 
    "currentCP" : -1 ,
    "fullCP"    : -1 ,
    "currentHP" : -1 ,
    "fullHP"    : -1 ,

    "enchanted"  : {}, 

    "where":"",     # "initializing", "gate" など
    "shift":None    # 直前の移動vector 

    } 

###############
# 敵関係

moving_objects = []
enemy = []
phase = "travel"

###############
# icon 関連
# 通常カーソルアイコン、敵カーソルアイコン、NPCカーソルアイコンへのポインタ
# RS 実行毎に変化する
# initialize() 時および敵/NPC遭遇時に更新する。
cursor = { 
    "normal":-1,
    "enemy":-1,
    "NPC":-1,
    "roten":-1
    }

###############
#
#  移動関連
#

center_pos = (400,244)
#center_pos = (360,200)
#center_pos = (400,200)
#center_pos = (340,200)
center_area = ( 400, 244, 400+2, 244+2) 

mapaname_list_normalized = []


chat_area = [1,467, 149-1,490-467]
player_area = [360,146,444-360,292-146 ]
coordinate_area = [599,0,  799 - 599, 22]
info_area = [ 599,0,799-599, 153 ]

