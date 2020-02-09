

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

    "enchanted"  : {}
    } 

###############
#
#  移動関連
#

center_pos = (400,244)
#center_pos = (360,200)
#center_pos = (400,200)
#center_pos = (340,200)

mapaname_list_normalized = []


def circle_around(point, r=1):
    x, y = point
    i, j = x-r, y-r
    while True:
        while i < x+r:
            i += r
            yield r, (i, j)
        while j < y+r:
            j += r
            yield r, (i, j)
        while i > x-r:
            i -= r
            yield r, (i, j)
        while j > y-r:
            j -= r
            yield r, (i, j)
        r += r
        j -= r
        yield r, (i, j)

