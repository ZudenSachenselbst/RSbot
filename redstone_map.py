

import pprint
import re
import os
import glob
import xmltodict, json
import networkx as nx
import matplotlib.pyplot as plt
import unicodedata
import pickle

from globals import *

G = nx.DiGraph()
#G = nx.Graph()

総合2func = {}
総合2func[  'オアシス都市アリアン'     ]                = [ 'op総合ポータル', 0, 575 ,77 ]
総合2func[  '古都ブルンネンシュティグ' ]                = [ 'op総合ポータル', 0, 575 ,157 ]
総合2func[  '港街シュトラセラト'       ]                = [ 'op総合ポータル', 0, 575 ,177 ]
総合2func[  '港街ブリッジヘッド'       ]                = [ 'op総合ポータル', 0, 575 ,197 ]
総合2func[  '鉱山町ハノブ'             ]                = [ 'op総合ポータル', 0, 575 ,217 ]
総合2func[  '新興王国ビガプール'       ]                = [ 'op総合ポータル', 0, 575 ,237 ]
総合2func[  '神聖都市アウグスタ'       ]                = [ 'op総合ポータル', 0, 575 ,257 ]
#総合2func[  'ガディウス大砂漠 / モリネルタワー付近'  ]  = [ 'op総合ポータル', 0, 575 ,277 ]

#総合2func[  'グレートフォレスト / プラトン街道' ]       = [ 'op総合ポータル', 1, 575 ,97 ]
総合2func[  'スウェブタワー　１Ｆ'     ]                = [ 'op総合ポータル', 1, 575 ,117 ]
総合2func[  'ソゴム山脈赤山'           ]                = [ 'op総合ポータル', 1, 575 ,137 ]
総合2func[  'ナラダ平原の沼地帯 / ノーススワンプ' ]     = [ 'op総合ポータル', 1, 575 ,157 ]
総合2func[  'ハンヒ山脈/ドレム川付近'  ]                = [ 'op総合ポータル', 1, 575 ,177 ]
総合2func[ "フォーリン望楼　地下" ]                     = [ 'op総合ポータル', 1, 575 ,217 ]
総合2func[ "ヘムクロス高原 / アラク湖付近" ]            = [ 'op総合ポータル', 1, 575 ,237 ]


総合2func[ "モリネルタワー　地上１階"]                  = [ 'op総合ポータル', 3, 575 ,137 ]
総合2func[ "河口ダンジョン　'ド'　Ｂ１"]                = [ 'op総合ポータル', 3, 575 ,177 ]
総合2func[ "河口ダンジョン　'ミ'　Ｂ１"]                = [ 'op総合ポータル', 3, 575 ,197 ]
総合2func[ "河口ダンジョン　'ラ'　Ｂ１"]                = [ 'op総合ポータル', 3, 575 ,217 ]
総合2func[ "河口ダンジョン　'レ'　Ｂ１"]                = [ 'op総合ポータル', 3, 575 ,237 ]
総合2func[ "廃墟スバイン要塞"]                          = [ 'op総合ポータル', 3, 575 ,257 ]
総合2func[ "北フォーリンロード / ネイダック平原地帯"]   = [ 'op総合ポータル', 3, 575 ,277 ]


総合テレポーター = [ 'ナイルローニ', 'パナパレ', 'レロック', 'ジーニ', 'ミレバン' ]

def edge2func( characterName, mapName ):
    global 総合2func
    global 総合テレポーター

    if characterName in 総合テレポーター:
        return 総合2func[ mapName ]
    else:
        print("edge2func: not supported %s->%s" % (characterName, mapName) )
        return None


def is_korean_chr(chr_u) :
    '''
    check if korean characters
    see http://www.unicode.org/reports/tr44/#GC_Values_Table
    '''
    category = unicodedata.category
    if category(chr_u)[0:2] == 'Lo' : # other characters
        if 'HANGUL' in unicodedata.name(chr_u) : return True
    return False

def prepare_world_map():
    print("enter prepare_world_map")
    global G
    debug = False
    #debug = True
    def my_print(*args, **kwargs):
        if debug:
            print(*args, **kwargs)
    

    map_pickle_file = "graph.pickle"
    if os.path.exists( map_pickle_file ):
        print("reading ", map_pickle_file ) 
        G = pickle.load(open( map_pickle_file, "rb"  ))
    else: 
        files = glob.glob("Map/*.xml")
        for i, file in enumerate(files):
            print("reading (%d/%d) %s" % ( i, len(files), file )  )
            with  open(file, "r", encoding='utf-8') as f:
                xml_string = f.read()
                o = xmltodict.parse( xml_string )
                # my_print( json.dumps(o, ensure_ascii=False, indent=4 )  ) 
                mapname = o["MapData"]["Details"]["MapName"]
                my_print( "\t", mapname ) 

                pngfile = file
                pngfile = re.sub( '\.xml', 'Sys.png', pngfile ) 
                G.add_node(mapname)
                G.nodes[mapname]["pngfile"] = pngfile
                G.nodes[mapname]["type"] = "map"

                G.nodes[mapname]["TgaWidth"]    = int( o["MapData"]["Details"]["TgaWidth"] ) 
                G.nodes[mapname]["TgaHeight"]   = int( o["MapData"]["Details"]["TgaHeight"] ) 
                G.nodes[mapname]["SysWidth"]    = int( o["MapData"]["Details"]["SysWidth"] ) 
                G.nodes[mapname]["SysHeight"]   = int( o["MapData"]["Details"]["SysHeight"] ) 



                ###############################
                # read characters

                flag = True
                try:
                    dummy = o["MapData"]["CharacterData"]["Character"]
                    
                except:
                    flag = False

                if flag:
                    for item in o["MapData"]["CharacterData"]["Character"]:
                        # print("item=", item)
                        if type(item) is str:   # only 1 character

                            CharacterName = o["MapData"]["CharacterData"]["Character"]["CharacterName"]
                            x             = o["MapData"]["CharacterData"]["Character"]["PopPoint_X"] 
                            y             = o["MapData"]["CharacterData"]["Character"]["PopPoint_Y"] 
                            x = re.sub( '\.\d+$', "", x)
                            y = re.sub( '\.\d+$', "", y)
                            x = int(x)
                            y = int(y)
                            my_print( "\t\tadding %s → %s" % ( mapname, CharacterName ) ) 
                            G.add_edge( mapname, CharacterName)
                            G.nodes[mapname]["type"] = "map"
                            G.nodes[CharacterName]["type"] = "character"
                            G.nodes[CharacterName]["Pos"] = ( x, y )
                            break

                        else:

                            CharacterName = item["CharacterName"] 
                            if CharacterName == 'null' or CharacterName is None:
                                continue
                            x             = item["PopPoint_X"] 
                            y             = item["PopPoint_Y"] 
                            x = re.sub( '\.\d+$', "", x)
                            y = re.sub( '\.\d+$', "", y)
                            x = int(x)
                            y = int(y)

                            flag = False
                            for chr_u in CharacterName:
                                if is_korean_chr(chr_u): 
                                    flag = True
                                    break
                            if flag:
                                my_print("\tkorean CharacterName", CharacterName)
                                continue

                            my_print( "\t\tadding %s → %s" % ( mapname, CharacterName ) ) 
                        

                            G.add_edge( mapname, CharacterName)
                            G.nodes[mapname]["type"] = "map"
                            G.nodes[CharacterName]["type"] = "character"
                            G.nodes[CharacterName]["Pos"] = ( x, y )


                ###############################
                # read Area( gate ) 

                flag = True
                try:
                    dummy = o["MapData"]["AreaData"]["Area"]
                except:
                    flag = False

                if flag:
                    for item in o["MapData"]["AreaData"]["Area"]:
                        if item["AccessMapName"] == 'null'or item["AccessMapName"] is None:
                            continue
                        AccessMapName = item["AccessMapName"]

                        if item["AreaName"] == 'null' or item["AreaName"] is None:
                            continue
                        AreaName = item["AreaName"] 

                        '''
                        flag = False
                        for chr_u in AreaName:
                            if is_korean_chr(chr_u): 
                                flag = True
                                break
                        if flag:
                            print("\tkorean", AreaName)
                            continue
                        '''


                        flag = False
                        for chr_u in AccessMapName:
                            if is_korean_chr(chr_u): 
                                flag = True
                                break
                        if flag:
                            my_print("\tkorean AccessMapName", AccessMapName)
                            continue

                        my_print( "\t\tadding %s → %s → %s" % ( mapname, AreaName, AccessMapName ) ) 
                    
                        x = item["AreaPos_X"]
                        y = item["AreaPos_Y"]
                        x = re.sub( '\.\d+$', "", x)
                        y = re.sub( '\.\d+$', "", y)
                        x = int(x)
                        y = int(y)

                        G.add_edge( mapname, AccessMapName )
                        G.nodes[mapname]["type"] = "map"
                        G.nodes[AccessMapName]["type"] = "map"
                        G.edges[     mapname, AccessMapName ]["Area"]    = AreaName
                        G.edges[     mapname, AccessMapName ]["Pos"] = (x,y)

        # 一部のマップが古いのでここで修正
        G.remove_edge( 'オアシス都市アリアン' , '古都ブルンネンシュティグ' ) 
        # グレートフォレスト / プラトン街道'  は迷路になっているので無視する
        G.remove_node( 'グレートフォレスト / プラトン街道' )
        G.remove_node( 'ガディウス大砂漠 / モリネルタワー付近' )

        pickle.dump(G, open('graph.pickle', 'wb'))

    # テレポーター関連
    # node(mapname, character) は登録済みである前提


    global 総合テレポーター
    for person in  総合テレポーター: 
        G.add_edge( person        ,  'オアシス都市アリアン' )
        G.add_edge( person        ,  '古都ブルンネンシュティグ' )
        G.add_edge( person        ,  '港街シュトラセラト' )
        G.add_edge( person        ,  '港街ブリッジヘッド' )
        G.add_edge( person        ,  '鉱山町ハノブ' )
        G.add_edge( person        ,  '新興王国ビガプール' )
        G.add_edge( person        ,  '神聖都市アウグスタ' )
        # G.add_edge( person        ,  'ガディウス大砂漠 / モリネルタワー付近'  )

        # G.add_edge( person        ,  'グレートフォレスト / プラトン街道' )
        G.add_edge( person        ,  'スウェブタワー　１Ｆ' )
        G.add_edge( person        ,  'ソゴム山脈赤山' )
        G.add_edge( person        ,  'ナラダ平原の沼地帯 / ノーススワンプ' )
        G.add_edge( person        ,  'ハンヒ山脈/ドレム川付近' )
        G.add_edge( person        ,  "フォーリン望楼　地下" )
        G.add_edge( person        ,  "ヘムクロス高原 / アラク湖付近" ) 

        G.add_edge( person        ,  "モリネルタワー　地上１階")
        G.add_edge( person        ,  "河口ダンジョン　'ド'　Ｂ１")
        G.add_edge( person        ,  "河口ダンジョン　'ミ'　Ｂ１")
        G.add_edge( person        ,  "河口ダンジョン　'ラ'　Ｂ１")
        G.add_edge( person        ,  "河口ダンジョン　'レ'　Ｂ１")
        G.add_edge( person        ,  "廃墟スバイン要塞")
        G.add_edge( person        ,  "北フォーリンロード / ネイダック平原地帯")


    if debug:
        show_around_burunen()
        '''
        # ブルンネンシュティグを中心とする小さなネットワーク図を作成する。
        # print( G.edges() ) 
        G2 = nx.ego_graph(G, "古都ブルンネンシュティグ",  radius=4 ) 
        edges = G2.edges()
        for edge in edges:
            # my_print(  edge )
            _from, _to = edge
            if G.nodes[_to]["type"] == "map":
                area = G.edges[_from, _to]["Area"]
                x,y =  G.edges[_from, _to]["Pos"]
                my_print(  "%s → (%s[%s,%s]) → %s" % (_from, area, x, y, _to ) ) 
            else:
                x,y =  G.node[_to]["Pos"]
                my_print(  "%s → %s[%s,%s]" % (_from, _to, x, y ) )
        '''

def show_around_burunen():
    show_around_city( "古都ブルンネンシュティグ",  4 ) 

def show_around_city(city_name, radius=4):
    global G

    # ブルンネンシュティグを中心とする小さなネットワーク図を作成する。
    # print( G.edges() ) 
    #G2 = nx.ego_graph(G, "古都ブルンネンシュティグ",  radius=4 ) 
    G2 = nx.ego_graph(G, city_name ,  radius=radius ) 
    edges = G2.edges()
    for edge in edges:
        # my_print(  edge )
        _from, _to = edge
        if G.nodes[_to]["type"] == "map":
            area = G.edges[_from, _to]["Area"]
            x,y =  G.edges[_from, _to]["Pos"]
            print(  "%s → (%s[%s,%s]) → %s" % (_from, area, x, y, _to ) ) 
        else:
            x,y =  G.node[_to]["Pos"]
            print(  "%s → %s[%s,%s]" % (_from, _to, x, y ) )

    # pprint(  G2.edges() )
    # edges = G2.edges()
    #for edge in G2.edges():
    #    print( edge )

    #G3 = G2.to_undirected()
    #nx.write_graphml(G3, "graph.xml")
    #nx.write_graphml(G2, "graph2.xml")

    #nx.draw(G2,with_labels=True)
    #plt.savefig("graph.png")
    #plt.show()



################################

import editdistance
import jaconv

def guess_mapname(ocr_string):
    ocr_string = jaconv.normalize(ocr_string)
    print("normalized ocr_string=", ocr_string)
    #global mapname
    # mapnames = [ jaconv.normalize(i) for i in mapnames ] 
    mapnames = list_mapname()
    mapname_normalized2org = {} 
    mapnames_normalized = []
    for mapname_org in mapnames:
        mapname_normalized = jaconv.normalize( mapname_org ) 
        mapname_normalized2org[mapname_normalized] = mapname_org
        mapnames_normalized.append( mapname_normalized)

    #print( " normalized mapnames=", mapnames_normalized )
    min_value = 1000
    min_map = None
    for normalized_map in mapnames_normalized:
        value = editdistance.eval( normalized_map, ocr_string ) 
        if value < min_value:
            min_value = value
            min_map = normalized_map
    print( min_map, " value=",  min_value )
    #return min_map
    return mapname_normalized2org[ min_map ] 


def find_route(_from, _to):
    global G
    path = nx.shortest_path(G, _from, _to) 
    print(path, flush=True )
    # [ map名, 出口(area)のx座標, 出口(area)のy座標  ]  の配列で返す。
    #  下記に変更 
    # 
    # [ map名, そのmapの出口(area)のx座標, そのmapの出口(area)のy座標, "map", null       ] 
    #   or 
    # [ character名, characterのx座標, characterのy座標  "character", func ]  の配列で返す。


    out = []
    for i in range(len(path)-1): 
        from_ = path[i]
        to_   = path[i+1]

        from_type = G.nodes[from_]["type"]
        to_type   = G.nodes[to_]["type"]
        if   from_type == "map" and to_type == "map" :
            x,y = G.edges[ from_, to_ ]["Pos"]
            out.append( [from_, to_, x, y, "map", "map", None  ] ) 

        elif from_type == "map" and to_type == "character" :
            (x,y) = G.nodes[to_]["Pos"]
            out.append( [from_, to_, x, y, "map","character",  None ] ) 

        elif from_type == "character" and to_type == "map" :
            #func, arg1, arg2, arg3  = edge2func["",""] 
            #functor = edge2func[from_, to_]
            functor = edge2func(from_, to_)
            out.append( [from_, to_, -1, -1, "character", "map", functor ] ) 

        else:  # from_type == "character" and to_type == "character" :
            print("find_route() error! character -> character ")
            return []

    return out

def list_mapname2png():
    global G
    for node in G.nodes():
        if G.nodes[node]["type"] == "map":
            print( G.nodes[node]["pngfile"], "\t", node ) 

def list_mapname():
    global G
    return list( G.nodes() ) 



def get_mapname2png(mapname):
    global G
    return G.nodes[mapname]["pngfile"]

def find_area_nearby():
    print("entered find_area_nearby()")
    global G
    global status
    mapname = status["mapName"]
    px, py  = status["pos"]
    # 現在の map の area の中で近そうなものを上げる
    neighbors = G.neighbors( mapname ) 
    min_distance = 1000000
    out = None
    out_x = None
    out_y = None
    for neighbor in neighbors:
        if G.nodes[neighbor]["type"] == "map":
            qx, qy = G.edges[mapname, neighbor]["Pos"]
            print( "find_area_nearby() checking %s → %s gate (%d, %d) " % (mapname, neighbor, qx, qy) )
            distance = abs(px-qx) + abs( py-qy) 
            if distance < min_distance:
                min_distance = distance
                out = neighbor
                out_x = qx
                out_y = qy

    print( "find_area_nearby() return ", out, out_x, out_y)
    return (out, out_x, out_y)


def get_name2pixel(name):
    if G.nodes[name]["type"] == "character":
        return G.nodes[name]["Pos"] 
    else:
        return None


#############################

def update_map_pos2pixel():
    global G
    global status
    mapname = status["mapName"]

    status["TgaWidth"]  = G.nodes[mapname]["TgaWidth"]    
    status["TgaHeight"] = G.nodes[mapname]["TgaHeight"]   
    status["SysWidth"]  = G.nodes[mapname]["SysWidth"]    
    status["SysHeight"] = G.nodes[mapname]["SysHeight"]   
    

########################
