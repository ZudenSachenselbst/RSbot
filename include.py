

#from guess_mapname import *
from basics import * 
from redstone_map import *
from skill import *
from redstone_map import *
from vision import *


################

from globals import *

################

import asyncio
import itertools

################

# 以下は basics.py に移動
'''
def click(x,y, duration=0.1):
    MoveMouse(x,y, M_LEFTDOWN)
    time.sleep(duration)
    MoveMouse(x,y, M_LEFTUP)
    time.sleep(duration)

def click2(x,y, duration=0.1):
    MoveMouse(x,y)
    time.sleep(duration)
    MoveMouse(x,y, M_LEFTDOWN)
    time.sleep(duration)
    MoveMouse(x,y, M_LEFTUP)
    time.sleep(duration)

def focusRS():
    # キャラクタが移動しないようHPゲージをクリックする。
    click(400,560) 

def clickCenter(duration = 0.1):
    #click(400,244,0.1)
    click(400,244,duration)
    #click2(400,244,0.3)

def closeMap():
    focusRS()

    rgb = pyautogui.pixel(797,26)
    if (173,107,41) == rgb:
        print("マップを閉じる")
        click(789,11, 0.2)

'''
# ここまで

def closeDialogue():
    focusRS()
    rgb = pyautogui.pixel(1,400)
    if (173,107,41) == rgb:
        print("ダイアログを閉じる")
        click(140,481,0.3) 




def getFieldName():
    global status
    focusRS()
    click(743,11, 0.2)
    time.sleep(0.1)
    # 現在位置を示すアイコンがブリンクするので、３回試す
    pos = None
    for i in range(3):
        time.sleep(0.3)
        pos = pyautogui.locateCenterOnScreen( "img/currentPosInWorldMap.bmp", 
                    grayscale=None, region=(0,0,800,600)  , confidence=0.9)
        if pos is not None:
            break
    # 戻るボタンを押す
    click( 777,541)

    if pos is None:
        print("failed to locate worldMap!")
        return None
   
    if is_vicinity( pos, (273,232), 20 ) :
        print(  '■中央プラトン街道 ／ ブルンネンシュティグ入口付近'  )
        status["fieldName"] = '■中央プラトン街道 ／ ブルンネンシュティグ入口付近' 
    else :
        print(  'area not known') 
        return None


def getMapName(mapname_arg = None):
    global status

    if mapname_arg is not None:
        status["mapName"] = mapname_arg
        return mapname_arg

    focusRS()
    clickCenter()
    closeMap()  # これをしないと座標表示位置がずれてクリックしてもマップ名が表示されない。
    # 位置座標のあたりをクリック
    #click(620, 10) 
    MoveMouse(620, 10) 
    time.sleep(1.0)
    # 横に日本語でマップ名が表示される。その表示領域（マップ名の長さで変わる）を枠の位置から判断して画像取得する。


    '''
    pyautogui.screenshot( "test.png",  region=(290,5,509-290, 20-5 ) ) 
    box  = pyautogui.locateOnScreen( "img/map_fringe3.bmp", grayscale=None, region=(290,5,509-290, 20-5 ), confidence=1.0)
    print(box)
    x = box.left
    y = box.top
    pos = (x,y)
    '''
    for x in range( 290, 550 ):
        rgb = pyautogui.pixel(x, 5) 
        if (173,107,41) == rgb:
            break
    print( "offset=", x )
    if x == 550:
       return None
    sc = pyautogui.screenshot(region=(x+2, 5, 596-x, 20-5 ) ) 
    sc.save("mapname_all.png")

    # map 名は "「コボルトの洞窟 B1」の用になっている。末尾のアルファベットの手前で分離する。

    gray = np.array(sc)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    _thre, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY ) 

    fig = cv2.imread("img/black_rectangle.bmp")
    fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
    _thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
    needle = np.array(fig)

    pos = compare_bitmap( gray, needle )
    print("black_rectangle pos=", pos)

    w1, h1 = gray.shape
    w2, h2 = needle.shape

    kanji_image = None
    floor_image = None
    # if pos is None: # floor 情報がない
    if pos is None or w1 - pos[1] < 10: # floor 情報がない or map名最後の余白にマッチ
        kanji_image = "mapname_all.png"
    else:
        sc = pyautogui.screenshot(region=(x+2, 5, pos[1]+1, 20-5 ) ) 
        sc.save("mapname.png")
        kanji_image = "mapname.png"

        x_offset = x + pos[1]+ 7 
        sc = pyautogui.screenshot(region=(x_offset, 5,  596-x_offset, 20-5 ) )
        sc.save("mapname_floor.png")
        floor_image = "mapname_floor.png"

    ocr_mapname = None

    process = subprocess.run(
            [
                #'C:\Users\IEUser\Downloads\Capture2Text_v4.6.2_32bit\Capture2Text\Capture2TextCLI.exe',
                'c:/Users/IEUser/Downloads/Capture2Text_v4.6.2_32bit/Capture2Text/Capture2Text_CLI.exe',
                "-l",
                "Japanese",
                "-i",
                # "mapname.png"
                kanji_image
                ], 
            check=True,stdout=subprocess.PIPE) 
    #number= process.stdout.decode(cp932).strip()
    string = process.stdout  # byte 文字列
    string = string.decode('utf-8').strip()
    print(string + "<" )
    ocr_mapname = string

    if floor_image is not None:

        process = subprocess.run(
                [
                    #'C:\Users\IEUser\Downloads\Capture2Text_v4.6.2_32bit\Capture2Text\Capture2TextCLI.exe',
                    'c:/Users/IEUser/Downloads/Capture2Text_v4.6.2_32bit/Capture2Text/Capture2Text_CLI.exe',
                    "-i",
                    # "mapname_floor.png"
                    floor_image
                    ], 
                check=True,stdout=subprocess.PIPE) 
        #number= process.stdout.decode(cp932).strip()
        string = process.stdout  # byte 文字列
        string = string.decode('utf-8').strip()
        print(string + "<" )

        ocr_mapname += " " + string

    mapname_string = guess_mapname( ocr_mapname ) 
    status["mapName"] = mapname_string
    return mapname_string




def character_login( character ):

    os.chdir("z:\\")
    # choose laocoon
    #x,y  = pyautogui.locateCenterOnScreen('laocoon.bmp', grayscale=True, region=(675, 100, 270, 200  ))
    x,y  = pyautogui.locateCenterOnScreen( "img/" + character + ".png", grayscale=True, region=(526,74,231,155 ))
    print(x,y)
    click(x,y,0.5)
    time.sleep(1.0)

    # start game
    # click twice 
    MoveMouse(664,486)
    time.sleep(1.0)
    click(664,486, 0.5)
    time.sleep(1.0)
    click(664,486, 0.5)


    # wait loading 
    time.sleep(10.0)

    '''
    # cancel ログインプレゼント
    click(725,69, 0.5)
    time.sleep(1.0)
    click(725,69, 0.5)
    time.sleep(1.0)

    closeMap()
    time.sleep(1.0)
    closeDialogue()
    '''



player = cv2.imread("img/player.bmp")

fig = cv2.imread("img/fig0.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig0 = np.array(fig)

fig = cv2.imread("img/fig1.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig1 = np.array(fig)

fig = cv2.imread("img/fig2.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig2 = np.array(fig)

fig = cv2.imread("img/fig3.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig3 = np.array(fig)

fig = cv2.imread("img/fig4.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig4 = np.array(fig)

fig = cv2.imread("img/fig5.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig5 = np.array(fig)

fig = cv2.imread("img/fig6.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig6 = np.array(fig)

fig = cv2.imread("img/fig7.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig7 = np.array(fig)

fig = cv2.imread("img/fig8.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig8 = np.array(fig)

fig = cv2.imread("img/fig9.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig9 = np.array(fig)

fig = cv2.imread("img/comma3.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
comma3 = np.array(fig)

fig = cv2.imread("img/hp_slash.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
hp_slash = np.array(fig)


#######################
# CP 用 fig

fig = cv2.imread("img/fig0s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
# 最上行を削除
fig = fig[1:,:]
fig0s = np.array(fig)

fig = cv2.imread("img/fig1s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig1s = np.array(fig)

fig = cv2.imread("img/fig2s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig2s = np.array(fig)

fig = cv2.imread("img/fig3s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig3s = np.array(fig)

fig = cv2.imread("img/fig4s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig4s = np.array(fig)

fig = cv2.imread("img/fig5s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig5s = np.array(fig)

fig = cv2.imread("img/fig6s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig6s = np.array(fig)

fig = cv2.imread("img/fig7s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig7s = np.array(fig)

fig = cv2.imread("img/fig8s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig8s = np.array(fig)

fig = cv2.imread("img/fig9s.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
fig = fig[1:,:]
fig9s = np.array(fig)

fig = cv2.imread("img/slashs.bmp")
fig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
_thre, fig = cv2.threshold(fig, 127, 255, cv2.THRESH_BINARY ) 
# 最上行を削除
fig = fig[1:,:]
slashs = np.array(fig)


def compare_bitmap( haystack, needle ):

    if len(haystack.shape) != 2:
        return None
    if len(needle.shape) != 2:
        return None

    w1, h1 = haystack.shape
    w2, h2 = needle.shape


    if  w1 < w2   or h1 < h2:
        return None

    #print( "w1,h1=", w1, h1)
    #print( "w2,h2=", w2, h2)

    #print("needle=", needle)
    #print("haystack=", haystack)

    for x in range(0, w1-w2+1) :
        for y in range(0, h1-h2+1) :
            #subarray = haystack[ x:w2 , y:h2 ]
            subarray = np.array( haystack[ x:x+w2 , y:y+h2 ] )
            
            #print( "subarray=" )
            #print( subarray )
            if(subarray==needle).all():
                #return True
                return (x,y)
    return None


def findDigitNew(gray, x,y):
    os.chdir("z:\\")
    # port of uwsc:findDigit()
    # haystack = gray[y:y+20, x:x+9]
    haystack = np.array( gray[y:y+20, x:x+9] ) 
    #cv2.imshow('haystack', haystack)
    #cv2.moveWindow("haystack", 1000,20)
    #print( "haystack=") 
    #print(  haystack)
    #cv2.waitKey(200)
    #print( "fig0=")
    #print( fig0 )


    #print(fig0)
    # if find_image(haystack, fig0 ) is None:
    if compare_bitmap(haystack, fig0 ) is None:
        pass
    else:
        #print("0")
        return 0

    #print(fig4)
    #if find_image(haystack, fig4 ) is None:
    if compare_bitmap(haystack, fig4 ) is None:
        pass
    else:
        #print("4")
        return 4

    #print(fig1)
    #if find_image(haystack, fig1 ) is None:
    if compare_bitmap(haystack, fig1 ) is None:
        pass
    else:
        #print("1")
        return 1

    #print(fig2)
    #if find_image(haystack, fig2 ) is None:
    if compare_bitmap(haystack, fig2 ) is None:
        pass
    else:
        #print("2")
        return 2

    #print(fig3)
    #if find_image(haystack, fig3 ) is None:
    if compare_bitmap(haystack, fig3 ) is None:
        pass
    else:
        #print("3")
        return 3

    #print(fig8)
    #if find_image(haystack, fig8 ) is None:
    if compare_bitmap(haystack, fig8 ) is None:
        pass
    else:
        #print("8")
        return 8

    #print(fig5)
    #if find_image(haystack, fig5 ) is None:
    if compare_bitmap(haystack, fig5 ) is None:
        pass
    else:
        #print("5")
        return 5

    #print(fig6)
    #if find_image(haystack, fig6 ) is None:
    if compare_bitmap(haystack, fig6 ) is None:
        pass
    else:
        #print("6")
        return 6

    #print(fig7)
    #if find_image(haystack, fig7 ) is None:
    if compare_bitmap(haystack, fig7 ) is None:
        pass
    else:
        #print("7")
        return 7

    #print(fig9)
    # if find_image(haystack, fig9 ) is None:
    if compare_bitmap(haystack, fig9 ) is None:
        pass
    else:
        #print("9")
        return 9

    print("-1")
    return -1;


#########################

def getPositionNew():
    os.chdir("z:\\")

    global status
    start = datetime.datetime.now()

    sc1 = pyautogui.screenshot( region=(0,0,800, 20) )
    gray = np.array(sc1)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    _thre, gray = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY ) 
    #print(gray) 
    #cv2.imshow('gray', gray)
    #cv2.moveWindow("gray", 900,20)
    #cv2.waitKey(2000)
    #print(gray) 
    #gray = cv2pil(gray)
    #gray.save("gray.bmp")


    # region=(603, 3, 60, 40 ), confidence=0.9)
    #gray2 = np.array( gray[  603:603+60, 3:3+20 ] )
    gray2 = np.array( gray[  3:3+20, 603:603+60 ] ) 

    # print("gray2") 
    # print(gray2) 
    
    # print("comma3") 
    # print(comma3) 

    # port of uwsc:getPositionNew()
    x = -1
    y = -1

    # pyautogui.screenshot( 'test.png',  region=(603, 3, 60, 40 ))
    # pos = pyautogui.locateOnScreen( "img/comma3.bmp", grayscale=True, region=(603, 3, 60, 40 ), confidence=0.9)
    pos = compare_bitmap( gray2, comma3 )
    if pos is None:
        print("getPositionNew error")
        return (x,y)
    #print(pos)
    #xx,yy = pos
    #xx = pos.left
    #yy = pos.top
    #print( "xx=%d, yy=%d" % (xx,yy))
    #xx,yy = pos
    yy,xx = pos
    xx = 603 + xx
    yy = 3 + yy
    # print( "xx=%d, yy=%d" % (xx,yy))

    p = 606 
    q = 3

    x0 = findDigitNew(gray, p, q)
    x1 = findDigitNew(gray, p+ 6, q)
    x2 = findDigitNew(gray, p+ 12, q)
    

    if (xx < p + 12 ) and  (x0 >= 0):
        x = x0
    else:
        if (xx < p + 18) and  (x1 >= 0):
            x = x0 * 10 + x1
        else: 
            if (xx < p + 24) and  (x2 >= 0):
                x = x0 * 100 + x1 * 10 + x2

    p = xx + 2

    y0 = findDigitNew(gray, p, q)
    #print("y0=", y0)
    y1 = findDigitNew(gray, p+ 6, q)
    #print("y1=", y1)
    y2 = findDigitNew(gray, p+ 12, q)
    #print("y2=", y2)


    if  y0 >= 0 and y1 == -1:
        y = y0
    else:
        if  y0 >= 0 and y1 >= 0 and  y2 == -1:
            y = y0 * 10 + y1
        else :
            if  y0 >= 0 and y1 >= 0 and  y2 >= 0:
                y = y0 * 100 + y1 * 10 + y2

    #print( "getPosition return:x=%d, y=%d" % (x,y) ) 
    end = datetime.datetime.now()
    elapse = end - start
    print("getPositionNew",  elapse ) 
    status["pos"] = (x,y) 
    return (x,y)



#########################

def getHP():
    start = datetime.datetime.now()
    global status
    # os.chdir("z:\\")

    # focusRS()
    #click(410,560, 1.0)
    click(410,560) 

    # sc1 = pyautogui.screenshot( region=(0,0,800, 20) )
    sc1 = pyautogui.screenshot( region=( 353, 547, 60, 20 ) ) 
    # pyautogui.screenshot( "sc.png",  region=( 353, 547, 60, 20 ) ) 

    gray = np.array(sc1)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    _thre, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY ) 

    #gray2 = np.array( gray[  3:3+20, 603:603+60 ] ) 
    #gray2 = np.array( gray[  353:353+20, 549:549+60 ] ) 

    #show_np_array("gray=", gray) 
    #show_np_array("hp_slash=", hp_slash)


    # return


    #x = -1
    #y = -1

    pos = compare_bitmap( gray, hp_slash )
    if pos is None:
        # current, full
        return (-1,-1)

    # rectangle 内部の slash 位置
    yy,xx = pos
    #print( "xx=%d, yy=%d" % (xx,yy))


    #return


    c0 = findDigitNew(gray, xx-6*3+1, yy-1)
    c1 = findDigitNew(gray, xx-6*2+1, yy-1)
    c2 = findDigitNew(gray, xx-6+1,   yy-1)
   
    #print (c0,c1,c2)


    current = c2;
    if 0 < c1:
        current = c1 * 10 + c2
    if 0 < c0:
        current = c0 * 100 + c1 * 10 + c2

    #print ("current=", current)


    f0 = findDigitNew(gray, xx+7,     yy-1)
    f1 = findDigitNew(gray, xx+7+6,   yy-1)
    f2 = findDigitNew(gray, xx+7+6+6, yy-1)
   
    #print (f0,f1,f2)


    full = f2;
    if 0 < f1:
        full = f1 * 10 + f2
    if 0 < f0:
        full = f0 * 100 + f1 * 10 + f2

    print ("current=", current, " full=", full)

    status["currentHP"] = current
    status["fullHP"] = full

    end = datetime.datetime.now()
    elapse = end - start
    print("getHP ", elapse ) 
    return (current, full)


#########################



def findDigitFooter_normal(x, y):

    
    #pyautogui.screenshot( 'temp' + str(x) + str(y) + ".png",  region=(x,y,9,20 )) 
    if pyautogui.locateOnScreen( "img/digit0.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 0

    if pyautogui.locateOnScreen( "img/digit4.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 4

    if pyautogui.locateOnScreen( "img/digit2.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 2

    if pyautogui.locateOnScreen( "img/digit1.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 1

    if pyautogui.locateOnScreen( "img/digit8.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 8


    if pyautogui.locateOnScreen( "img/digit9.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 9


    if pyautogui.locateOnScreen( "img/digit3.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 3


    if pyautogui.locateOnScreen( "img/digit5.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 5

    if pyautogui.locateOnScreen( "img/digit6.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 6


    if pyautogui.locateOnScreen( "img/digit7.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 7

    return -1


def findDigitFooter_reverse(x, y):


    #pyautogui.screenshot( 'ttemp' + str(x) + str(y) + ".png",  region=(x,y,9,20 )) 
    if pyautogui.locateOnScreen( "img/digit0r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 0

    if pyautogui.locateOnScreen( "img/digit4r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 4

    if pyautogui.locateOnScreen( "img/digit2r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 2

    if pyautogui.locateOnScreen( "img/digit1r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 1

    if pyautogui.locateOnScreen( "img/digit8r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 8


    if pyautogui.locateOnScreen( "img/digit9r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 9


    if pyautogui.locateOnScreen( "img/digit3r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 3


    if pyautogui.locateOnScreen( "img/digit5r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 5

    if pyautogui.locateOnScreen( "img/digit6r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 6


    if pyautogui.locateOnScreen( "img/digit7r.bmp", grayscale=True, region=(x,y,9,20 ), confidence=0.9) is None:
        pass
    else:
        return 7

    return -1



def findDigitFooterMinus(x, y):



    if pyautogui.locateOnScreen( "img/minus.bmp", grayscale=True, region=(x,y,9,11 ), confidence=0.9) is None:
        pass
    else:
        return 1

    if pyautogui.locateOnScreen( "img/minusr.bmp", grayscale=True, region=(x,y,9,11 ), confidence=0.9) is None:
        pass
    else:
        return 1

    if pyautogui.locateOnScreen( "img/minusr2.bmp", grayscale=True, region=(x,y,9,11 ), confidence=0.9) is None:
        pass
    else:
        return 1

    return 0

##############################################

def findDigitCP(gray, x,y):

    # os.chdir("z:\\")

    haystack = np.array( gray[y:y+10, x:x+6] ) 

    #print(fig0)
    #print( "haystack=", haystack);
    #print( "fig0s=", fig0s);

    if compare_bitmap(haystack, fig0s ) is None:
        pass
    else:
        my_print("0")
        return 0

    #print(fig4)
    if compare_bitmap(haystack, fig4s ) is None:
        pass
    else:
        my_print("4")
        return 4

    #print(fig1)
    if compare_bitmap(haystack, fig1s ) is None:
        pass
    else:
        my_print("1")
        return 1

    #print(fig2)
    if compare_bitmap(haystack, fig2s ) is None:
        pass
    else:
        my_print("2")
        return 2

    #print(fig3)
    if compare_bitmap(haystack, fig3s ) is None:
        pass
    else:
        my_print("3")
        return 3

    #print(fig8)
    if compare_bitmap(haystack, fig8s ) is None:
        pass
    else:
        my_print("8")
        return 8

    #print(fig5)
    if compare_bitmap(haystack, fig5s ) is None:
        pass
    else:
        my_print("5")
        return 5

    #print(fig6)
    if compare_bitmap(haystack, fig6s ) is None:
        pass
    else:
        my_print("6")
        return 6

    #print(fig7)
    if compare_bitmap(haystack, fig7s ) is None:
        pass
    else:
        my_print("7")
        return 7

    #print(fig9)
    if compare_bitmap(haystack, fig9s ) is None:
        pass
    else:
        my_print("9")
        return 9

    print("-1")
    return -1



def getCPNew():
    start = datetime.datetime.now()
    global status
    # os.chdir("z:\\")

    # focusRS()
    #click(410,560, 1.0)
    #click(410,560) 

    #sc1 = pyautogui.screenshot( region=( 370, 585, 60, 11 ) ) 
    # １行減らす
    sc1 = pyautogui.screenshot( region=( 370, 586, 60, 10 ) ) 
    # gray スケールにする。
    gray = np.array(sc1)

    # 補正前
    #cv2.imwrite('gray0.bmp', gray) 
    

    #print(gray[9, :, :]) 
    # 反転している箇所を探す

    for i in range( 60):
        if gray [ 9, i, 0] > 127: # 地が白い
            pass
        else:   # 地が黒い
            break
    if i == 0:
        #print("全領域白地")
        pass
    elif i == 60:
        #print("全領域黒地")
        # do nothing
        gray = cv2.bitwise_not(gray)
    else:
        #print("x = 370 + %d の箇所から黒地" % (i) ) 

        # 反転している箇所をもとに戻す。

        gray1 = gray[:, 0:i, :]
        gray2 = gray[:, i:, :]
        gray2inv = cv2.bitwise_not(gray2)
        # 2値化してからinverse を取る
        #_thre, gray2inv = cv2.threshold(gray2, 128, 255, cv2.THRESH_BINARY ) 
        #gray2inv = cv2.bitwise_not(gray2inv)

        gray = cv2.hconcat( [gray1, gray2inv] ) 

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    _thre, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY ) 

    #show_np_array( "反転補正後", gray) 
    #print( "gray=", gray ) 
    #print( "shashs=", slashs ) 
    #cv2.imwrite('gray1.bmp', gray) 
    #cv2.imwrite('slashs.bmp', slashs) 

    # 一番上の行はノイズが多いので削除
    # gray = gray[1:,:,:]

    #x = -1
    #y = -1

    # gray = gray[:, 29:29+6]

    pos = compare_bitmap( gray, slashs )
    if pos is None:
        # current, full
        return (-1,-1)

    # rectangle 内部の slash 位置
    yy,xx = pos
    #print( "xx=%d, yy=%d" % (xx,yy))


    #return


    c0 = findDigitCP(gray, xx-6*3, yy)
    c1 = findDigitCP(gray, xx-6*2, yy)
    c2 = findDigitCP(gray, xx-6,   yy)
   
    #print (c0,c1,c2)


    current = c2;
    if 0 < c1:
        current = c1 * 10 + c2
    if 0 < c0:
        current = c0 * 100 + c1 * 10 + c2

    #print ("current=", current)


    f0 = findDigitCP(gray, xx+6,     yy)
    f1 = findDigitCP(gray, xx+6+6,   yy)
    f2 = findDigitCP(gray, xx+6+6+6, yy)
   
    #print (f0,f1,f2)


    full = f2;
    if 0 < f1:
        full = f1 * 10 + f2
    if 0 < f0:
        full = f0 * 100 + f1 * 10 + f2

    print ("current=", current, " full=", full)

    status["currentCP"] = current
    status["fullCP"] = full

    end = datetime.datetime.now()
    elapse = end - start
    print("getCPNew ", elapse ) 
    return (current, full)



##############################################

def getCP():
    start = datetime.datetime.now()
    global status
    # port of uwsc:getCP()
    current = -1
    full = -1

    x = 0
    y = 0


    xx = 0
    yy = 0
    pos = pyautogui.locateOnScreen( "img/slash.bmp", grayscale=True, region=(380,584,40,20 ),confidence=0.9)
    if pos is not None:
        xx = pos.left
        yy = pos.top
    else:
        pos = pyautogui.locateOnScreen( "img/slashr2.bmp", grayscale=True, region=(380,584,40,20 ),confidence=0.9)
        if pos is not None:
            xx = pos.left
            yy = pos.top

    if xx == 0 and yy == 0:
        return (current, full)

    #print("xx=%d, yy=%d" % (xx,yy))

    mx0 = findDigitFooterMinus(xx - 24, yy )
    mx1 = findDigitFooterMinus(xx - 18, yy )
    mx2 = findDigitFooterMinus(xx - 12, yy )

    
    x2 = findDigitFooter_normal(xx - 6, yy )
    x1 = findDigitFooter_normal(xx - 12, yy )
    x0 = findDigitFooter_normal(xx - 18, yy ) 


    if  x0 < 0  or x1 < 0 or x2 < 0 :
        x2 = findDigitFooter_reverse(xx - 6, yy )
        x1 = findDigitFooter_reverse(xx - 12, yy )
        x0 = findDigitFooter_reverse(xx - 18, yy ) 


    if x0 < 0 and x1 < 0 and x2 >= 0:
        current = x2
    else: 
        if x0 < 0 and x1 >= 0 and x2 >= 0:
            current  = x1 * 10 + x2
        else :
            if x0 >= 0 and x1 >= 0 and x2 >= 0:
                current = x0 * 100 + x1 * 10 + x2

    if mx0 == 1 or mx1 == 1 or mx2 == 1 :
        current = current * -1


    y0 = findDigitFooter_normal(xx + 6, yy )
    y1 = findDigitFooter_normal(xx + 12, yy )
    y2 = findDigitFooter_normal(xx + 18, yy ) 


    if  y0 < 0  or y1 < 0 or y2 < 0 :
        y0 = findDigitFooter_reverse(xx + 6, yy )
        y1 = findDigitFooter_reverse(xx + 12, yy )
        y2 = findDigitFooter_reverse(xx + 18, yy ) 


    if  y0 >= 0 and y1 == -1:
        full  = y0
    else :
        if  y0 >= 0 and y1 >= 0 and  y2 == -1:
            full = y0 * 10 + y1
        else :
            if  y0 >= 0 and y1 >= 0 and  y2 >= 0:
                full = y0 * 100 + y1 * 10 + y2

    #print( "current=" + str(current) + ", full=" + str(full) )

    status["currentCP"] = current
    status["fullCP"]    = full

    end = datetime.datetime.now()
    elapse = end - start
    print("getCP ", elapse )
    return (current, full)


###############

#chat_area = [1,467, 149-1,490-467]
#player_area = [360,146,444-360,292-146 ]


###############
#
#  移動関連
#

#center_pos = (400,244)
#center_pos = (360,200)  # moved to globals.py
#center_pos = (400,200)
#center_pos = (340,200)

# 画面          800, 600

# position coordinate    

# ■中央プラトン街道 ／ ブルンネンシュティグ入口付近.  
#       position 193,176  -> 200,180
#                             |   |
#                             V   V
#       bitmap               400,185
# (0,0)- (193,176) ≒ (200,180)

# ■中央プラトン街道 / グレートフォレスト入口付近    
#        position   248,307
#                    |   |
#                    V   V
#       bitmap      400,248



def map_locate( file ):
    img = my_imread(file)

    height = img.shape[0]
    width  = img.shape[1]
    # print( "height, width=%d,%d" % ( height, width) )    
    #x,y = getPosition()
    x,y = getPositionNew()
    print(x,y)
    mx,my = pos2pixel(x,y)

    print("mx,my=", mx,my)
    #cv2.rectangle(img, (mx, my), (mx + 2, my + 2), (0, 255, 0), 2)
    cv2.rectangle(img, (mx, my), (mx + 2, my + 2), (0, 255, 255), 2)    # yellow
    resized_img = cv2.resize(img,(width*3, height*3))
    #resized_img = cv2.resize(img,(width*2.5, height*2.5))
    cv2.imshow('map2', resized_img)
    #cv2.moveWindow("map2", 1200,40)
    cv2.moveWindow("map2", 1000,40)
    #cv2.waitKey(100)
    cv2.waitKey(10)


def is_vicinity( p, q, offset=10): # not used
    px,py = p
    qx,qy = q

    #if abs (px-qx) <= 10 and abs (py-qy) <= 10:
    if abs (px-qx) <= offset  and abs (py-qy) <= offset:
        return True
    else:
        return False

def pos2pixel(x,y): # position x,y
    global status

    TgaWidth  = status["TgaWidth"]  
    TgaHeight = status["TgaHeight"] 
    SysWidth  = status["SysWidth"]  
    SysHeight = status["SysHeight"] 

    pixel_x =  math.floor( x / ( SysWidth  / TgaWidth ) ) 
    pixel_y =  math.floor( y / ( SysHeight / TgaHeight ) ) 

    return ( pixel_x, pixel_y ) 

def pixel2pos(x,y): # pixel x,y

    global status
    TgaWidth  = status["TgaWidth"]  
    TgaHeight = status["TgaHeight"] 
    SysWidth  = status["SysWidth"]  
    SysHeight = status["SysHeight"] 

    pos_x =  math.floor( x / ( TgaWidth  / SysWidth ) ) 
    pos_y =  math.floor( y / ( TgaHeight / SysHeight ) ) 

    return ( pos_x, pos_y) 






def pixel2view(x,y):    # pixel x,y
    return (x*23, y*23)

@asyncio.coroutine
def goto_object(name): 
    # 現在のマップや別のマップの人物やオブジェクトのところへ移動する。
    global status
    route = find_route( status["mapName"], name)    # usually player is on gate
    print("route=", route)
    status["where"] = ""
    #for waypoint in route:
    for i, waypoint in enumerate(route):
        from_name, to_name, x, y, from_type, to_type, info = waypoint
        if   from_type == "map" and to_type == "map":
            mapname = from_name
            initialize2(mapname)   # 新しいmap に入った時点ですること
            #result = goto_pixel( x, y) 
            #t1 = asyncio.async( goto_pixel( x, y) )
            result = yield from goto_pixel( x, y) 
            if result:
                click_gate()
                status["where"] = "gate"
                time.sleep(5)
            else:
                print("failed!")
                break

        elif from_type == "map" and to_type == "character":
            mapname = from_name
            character_name = to_name
            initialize2(mapname)   # 新しいmap に入った時点ですること
            #result = goto_pixel( x, y) 
            result = yield from  goto_pixel( x, y) 
            if result:
                #click_object(character_name) 
                click_NPC(character_name) 
            else:
                print("failed!")
                break

        elif from_type == "character" and to_type == "map":
                func, arg1, arg2, arg3 = info
                print("execute ", func)
                # func(arg1, arg2, arg3)
                globals()[func](arg1, arg2, arg3)

@asyncio.coroutine
def goto_pixel(x,y):  # pixel x,y
    print("●entered goto_pixel")
    # 現在のマップの特定の pixel 位置に移動する。
    goal = (x,y)    # pixel coordinate
    cx,cy = getPositionNew()
    #start = (cx,cy)
    dx,dy =  pos2pixel(cx,cy)
    start = (dx,dy)

    print("map goal pixel =",x,y,"map start pixel=",  dx,dy ) 
    #file = current_map
    global status
    file = get_mapname2png( status["mapName"] )
    waypoints = find_path(file, start, goal)
    if waypoints == None:
        waypoints = find_path(file, start, goal, True)  # retry mode

    #waypoints = remote_find_path(file, start, goal)
    #print(waypoints)
    list(map( lambda x: {print(x)} , enumerate(waypoints)))
    prev_xx = xx = 0
    prev_yy = yy = 0
    for i, waypoint in enumerate(waypoints):
        print("moving to ", i, waypoint ) 
        prev_xx = xx
        prev_yy = yy

        (bx,by, _, _)  = waypoint
        xx, yy = pixel2pos( bx,by )

        vec = (xx-prev_xx, yy - prev_yy)
        vecr = (-1 * vec[0], -1 * vec[1] ) 
        vec1 = ( vec[1], -1 * vec[0] ) # orthogonal to vector
        vec2 = ( -1 * vec[1], vec[0] ) # orthogonal to vector
        

        my_status = move_to( xx,yy ) 
        yield from asyncio.sleep(0.001)

        try_count = 0
        while not my_status:
            try_count += 1
            if try_count == 10:
                break

            # とりあえず１つ前のwaypoint にもどる　

            move_to( prev_xx,prev_yy ) 

            # 障害物から離れる方向に移動する
            # だんだん大きく離れる

            qx,qy = getPositionNew()
            if try_count % 2 == 0:
                print( "avoid obstacle: direction=", vec1 ) 
                # 少し戻る
                for i in range( int((try_count+1)/2) ):
                    move_toward( qx + 10 * vecr[0], qy + 10 * vecr[1] ) 
                    time.sleep(1.0) 
                for i in range( int((try_count+1)/2) ):
                    move_toward( qx + 10 * vec1[0], qy + 10 * vec1[1] ) 
                    time.sleep(1.0) 
            else:
                print( "avoid obstacle: direction=", vec2 ) 
                # 少し戻る
                for i in range( int((try_count+1)/2) ):
                    move_toward( qx + 10 * vecr[0], qy + 10 * vecr[1] ) 
                    time.sleep( 1.0) 
                for i in range( int((try_count+1)/2) ):
                    move_toward( qx + 10 * vec2[0], qy + 10 * vec2[1] ) 
                    time.sleep(1.0) 

            my_status = move_to( xx,yy ) 
        if my_status:
            print( "reached waypoint(%d)  %d,%d" % (i, bx,by) )
        else:
            print( "stacked!!") 
            break
    if my_status:
        return True
    else:
        return False
#######################################
##############################################################################
# import packages
##############################################################################


def adjust_point(array, point): # not used
    x,y=point
    h = array.shape[0]
    w = array.shape[1]
    if x == 0 or x == w-1:
        return point
    if y == 0 or y == h-1:
        return point




import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



##############################################################################
# plot the path
##############################################################################

def adjust_waypoint( grid, x,y):    # pixel x,y

    #print( "grid.shape:")
    #print( type(grid)) 
    #print( grid.shape)
    adj_x = 0
    adj_y = 0
    if x==0 or y==0:
        return ( adj_x, adj_y)

    if x+1 == grid.shape[0] or y+1 == grid.shape[1]:
        return ( adj_x, adj_y)

    #v = grid[ x-1:x+2, y-1:y+2 ] 
    #print(v) 

    #print("v:")
    #print(v)

    #top  = sum( matrix[0])
    #down = sum( matrix[2])
    #left = sum( matrix[:,0])
    #right= sum( matrix[:,2])

    #top  = v[0][0] + v[0][1] + v[0][2]
    #down = v[2][0] + v[2][1] + v[2][2]
    #left = v[0][0] + v[1][0] + v[2][0]
    #right= v[0][2] + v[1][2] + v[2][2]
                          
    top  = grid[x-1][y-1] + grid[x  ][y-1] + grid[x+1][y-1]
    down = grid[x-1][y+1] + grid[x  ][y+1] + grid[x+1][y+1]

    left = grid[x-1][y-1] + grid[x-1][y  ] + grid[x-1][y+1]
    right= grid[x+1][y-1] + grid[x+1][y  ] + grid[x+1][y+1]

                            
                            


    if top >  0 and down  == 0 :
        adj_y = 1
    if top == 0 and down  >  0 :
        adj_y = -1
    if left== 0 and right >  0 :
        adj_x = -1
    if left > 0 and right == 0 :
        adj_x = 1

    return ( adj_x, adj_y)

def find_path(file, start, goal, retry=False):   # pixel x,y



    # goal/start 地点が image の縁周辺だと astar() がエラーするので調整する。

    x,y = start
    if x < 2:
        x=2
    if y < 2:
        y=2
    start = (y,x)
    start_org = start

    x,y =goal
    if x < 2:
        x=2
    if y < 2:
        y=2
    goal = (y,x)
    goal_org = goal


    img = my_imread(file)
    ret,bg = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    grid = cv2.bitwise_not(bg)


    # 出発地、目的地が地図上でブランク(0,0,0)でないと astar() がエラーする
    # その場合は出発地、目的地を近傍の blank 地点に変更する。

    '''
    # globals.py に移動
    def circle_around(point):
        x, y = point
        r = 1
        i, j = x-1, y-1
        while True:
            while i < x+r:
                i += 1
                yield r, (i, j)
            while j < y+r:
                j += 1
                yield r, (i, j)
            while i > x-r:
                i -= 1
                yield r, (i, j)
            while j > y-r:
                j -= 1
                yield r, (i, j)
            r += 1
            j -= 1
            yield r, (i, j)
    '''


    def find_room_nearby(grid, point ):
        print("entered find_room_nearby")
        gen = circle_around( point ) 
        point2 = point
        thres = 20
        for i in range(thres):
            j, point2 = next(gen)
            # if( 0 == grid[ point2[0], point2[1], 0] ):
            if np.all(  0 == grid[point2[0]][point2[1]] ):
                break
        if i == thres-1:
            print( "find_room_nearby() return None")
            return None
        else:
            return point2


    def block_diagonal(haystack):

        # print ( haystack[ 0:10, 0:10, 0] ) 
        w, h, _dummy = haystack.shape
        print(w, h, _dummy)
        for x in range(0, w-1) :
            for y in range(0, h-1) :
                if(    0 <  haystack[x,y,  0]  and   0 == haystack[x+1,y,   0]  and 
                       0 == haystack[x,y+1,0]  and   0 <  haystack[x+1,y+1, 0]  ) : 
                    #haystack[x+1,y, :]  = 255
                    #haystack[x,y+1, :]  = 255
                    haystack[x+1,y, :]  = 128   # gray
                    haystack[x,y+1, :]  = 128
                    continue

                if(    0 == haystack[x,y,  0]  and   0 <  haystack[x+1,y,   0]  and 
                       0 <  haystack[x,y+1,0]  and   0 == haystack[x+1,y+1, 0]  ) : 
                    #haystack[x,y,     :]  = 255
                    #haystack[x+1,y+1, :]  = 255
                    haystack[x,y,     :]  = 128
                    haystack[x+1,y+1, :]  = 128
                    continue


        return haystack

    def block_narrow_path(haystack):

        print ( "entered block_narrow_path ") 
        #  any    any
        #   ↓    ↓
        #  [+][ ][ ]
        #  [ ][o][ ]
        #  [ ][ ][+]
        #  
        #  [+][ ][ ]← any
        #  [ ][o][ ]
        #  [ ][ ][ ]← any
        #
        #


        grid2 = np.copy(grid)
        # print ( haystack[ 0:10, 0:10, 0] ) 
        w, h, _dummy = haystack.shape
        print(w, h, _dummy)
        for x in range(1, w-2) :
            for y in range(1, h-2) :
                if np.all(  0 == haystack[x][y] ) :
                    if( np.any( 0 <  haystack[x-1:x+2, y ] ) and 
                        np.any( 0 <  haystack[x-1:x+2, y ] ) ): 
                        #print( "%d,%d" % ( x,y )  ) 
                        #haystack[x,y] = [192,192,192]   # silver 
                        grid2[x,y,:] = 192   # silver 
                        continue
                    if( np.any( 0 <  haystack[x, y-1:y+2 ] ) and 
                        np.any( 0 <  haystack[x, y-1:y+2 ] ) ): 
                        # haystack[x,y] = [192,192,192]   # silver 
                        grid2[x,y,:] = 192   # silver 
                        #print( "%d,%d" % ( x,y )  ) 
                        continue

        #return haystack
        return grid2



    ##############################################################################
    # plot grid
    ##############################################################################
    # https://www.analytics-link.com/single-post/2018/09/14/Applying-the-A-Path-Finding-Algorithm-in-Python-Part-1-2D-square-grid
     

    ##############################################################################
    # heuristic function for path scoring
    ##############################################################################

     

    def heuristic(a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

     

    ##############################################################################
    # path finding function
    ##############################################################################

     

    def astar(array, start, goal):

        neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:heuristic(start, goal)}
        oheap = []

        heapq.heappush(oheap, (fscore[start], start))
        
        while oheap:

            current = heapq.heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                if 0 <= neighbor[0] < array.shape[0]:
                    if 0 <= neighbor[1] < array.shape[1]:                
                        #if array[neighbor[0]][neighbor[1]] == 1:
                        '''
                        val = array[neighbor[0]][neighbor[1]]
                        # print(val, type(val))
                        if isinstance(val, np.ndarray):
                            #if val == [255,255,255]:
                            if np.any( 0 < val ):
                                continue
                            else:
                                pass
                        else:
                            if val == 1:
                                continue
                            else:
                                pass
                        '''
                        if np.any( 0 < array[neighbor[0]][neighbor[1]] ):
                            continue

                    else:
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue
                    
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                    
                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
                    
        #return False
        return None


    grid = block_diagonal(grid) # never fail

    grid2 = np.copy(grid)
    #grid2[ start_org[0], start_org[1], :] = [128,0,128] # purple
    # grid2[ goal_org[0], goal_org[1], :]   = [0,255,0]   # lime
    grid2[ start_org[0], start_org[1], :] = [255,0,0  ] # red 
    grid2[ goal_org[0], goal_org[1], :]   = [255,0,255]   # magenta
    cv2.imwrite('path2.png', grid2) 


    #if( 0 < grid[ goal[0], goal[1], 0] ):
    if np.any( 0 < grid[ goal[0], goal[1], :]) :    # たまにある
        goal  = find_room_nearby(grid, goal)    # may fail

    #if( 0 < grid[ start[0], start[1], 0] ):
    if np.any( 0 < grid[ start[0], start[1], :]) :
        start = find_room_nearby(grid, start)   # may fail


    if retry :
        pass    # allow narrow path 
    else:
        grid = block_narrow_path(grid)  # never fail
        # start, goal は 塞がない
        grid[start[0], start[1],:] = [0,0,0]
        grid[ goal[0],  goal[1],:] = [0,0,0]

    if goal is None or start is None:
        return None

    # plot 
    grid2 = np.copy(grid)

    grid2[ start_org[0], start_org[1], :] = [255,0,0  ] # red 
    grid2[ goal_org[0], goal_org[1], :]   = [255,0,255]   # magenta

    grid2[ start[0], start[1], :]         = [0,255,255] # cyan 
    grid2[ goal[0], goal[1], :]           = [255,255,0] # yellow

    cv2.imwrite('path2.png', grid2) 


    route = astar(grid, start, goal)

    if route is None: # astar fail
        return None

    route = route + [start]
    route = route[::-1]
    # print(route)

    

    ##############################################################################
    # plot the path
    ##############################################################################

    waypoints = []
    #height = grid.shape[0]
    #width  = grid.shape[1]
    #path_image = np.zeros((height,width,3), np.uint8) 

    #extract x and y coordinates from route list
    x_coords = []
    y_coords = []

    grid2 = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
    #_thre, grid2 = cv2.threshold(grid2, 127, 255, cv2.THRESH_BINARY ) 
    for i in (range(0,len(route))):
        x = route[i][0]
        y = route[i][1]
        x_coords.append(x)
        y_coords.append(y)

        #grid [x][y] = [255,255,255]
        #if i % 5 == 0:
        #if True:
        if i % 3 == 0:
            #cv2.circle(grid , (y, x), 1, (0,255,0), -1) 
            #cv2.circle(grid , (y, x), 1, (0,255,0), -1) 
            #grid [x][y] = [0,255,0] # green 

            adj_x, adj_y = adjust_waypoint( grid2 , x, y) 
            #adj_x = 0
            #adj_y = 0
            grid [x+adj_x][y+adj_y] = [0,255,0] # green 
            #waypoints.append( (x+adj_x, y+adj_y) )  
            waypoints.append( ( y+adj_y, x+adj_x, adj_y, adj_x) )  
    cv2.imwrite( 'path.png', grid) 

    return waypoints
    ###############################

    '''
    # plot map and path
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(grid, cmap=plt.cm.Dark2)
    ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 200)
    ax.scatter(goal[1],goal[0], marker = "*", color = "red", s = 200)
    ax.plot(y_coords,x_coords, color = "red")
    plt.show()
    '''


##################
# util
# Python OpenCV の cv2.imread 及び cv2.imwrite で日本語を含むファイルパスを取り扱う際の問題への対処について - Qiita https://qiita.com/SKYS/items/cbde3775e2143cad7455

def my_imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def find_image(im, tpl):
    im = np.atleast_3d(im)
    tpl = np.atleast_3d(tpl)
    H, W, D = im.shape[:3]
    h, w = tpl.shape[:2]

    # Integral image and template sum per channel
    sat = im.cumsum(1).cumsum(0)
    tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

    # Calculate lookup table for all the possible windows
    iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:] 
    lookup = iD - iB - iC + iA
    # Possible matches
    possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))

    # Find exact match
    for y, x in zip(*possible_match):
        if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
            print("found")
            return (y+1, x+1)

    #raise Exception("Image not found")
    return None


def is_reached(x,y):   #position x,y
    cx,cy = getPositionNew()
    # if  5 >= abs(x-cx) and 5 >= abs(y-cy):
    #range=5
    #range=4
    range=3
    if  range >= abs(x-cx) and range >= abs(y-cy):
        print("reached!")
        return True
    else:
        return False


def click_gate():
    # 見えている範囲のゲートをクリックする。
    # 30,10 - 70x40
    # gateAnm_13.png    gate1.bmp
    # gateAnm_19.png    gate2.bmp
    # gateAnm_25.png    gate3.bmp
    # gateAnm_31.png    gate4.bmp
    # gateAnm_37.png    gate5.bmp
    # gateAnm_43.png    gate6.bmp
    # gateAnm_49.png    gate7.bmp
    # gateAnm_55.png    gate8.bmp

    gate_image = [
            "gateAnm/gate1.bmp", 
            "gateAnm/gate2.bmp", 
            "gateAnm/gate3.bmp", 
            "gateAnm/gate4.bmp", 
            "gateAnm/gate5.bmp", 
            "gateAnm/gate6.bmp",
            "gateAnm/gate7.bmp",
            "gateAnm/gate8.bmp",
            "gateAnm/gate8.bmp",
            "gateAnm/gate10.bmp",
            "gateAnm/gate11.bmp",
            "gateAnm/gate12.bmp",
            "gateAnm/gate13.bmp",
            "gateAnm/gate14.bmp",
            "gateAnm/gate15.bmp",
            "gateAnm/gate16.bmp",
            "gateAnm/gate17.bmp",
            "gateAnm/gate18.bmp",
            "gateAnm/gate19.bmp",
            "gateAnm/gate20.bmp",
            "gateAnm/gate21.bmp"
            ] 

    for gate in gate_image:
        pos = pyautogui.locateCenterOnScreen( gate, grayscale=True, region=(0,0,800,600 ),confidence=0.7)
        if pos is not None:
            print("found gate")
            x,y = pos
            print(x,y)
            # click(x,y,0.5)
            #MoveMouse(x,y ) 
            #time.sleep(1.0)
            click(x,y,2.0)
            '''
            click(x-100,y-100,0.5)
            click(x    ,y-100,0.5)
            click(x+100,y-100,0.5)

            click(x-100,y    ,0.5)
            #click(x   ,y    ,0.5)
            click(x+100,y    ,0.5)

            click(x-100,y+100,0.5)
            click(x    ,y+100,0.5)
            click(x+100,y+100,0.5)
            '''
            break
    if pos is None:
        print("cannot found gate")


def click_object(name):
    # 見えている範囲の人物やオブジェクトをクリックする。
    x, y = get_name2pixel(name)
    click_pixel(x,y)

def click_pixel(x,y):   # pixel x,y
    # 見えている範囲の pixel をクリックする。

    cx,cy = getPositionNew()
    print("cx,cy=", cx,cy)
    dx,dy = pos2pixel(cx,cy)
    print("dx,dy=", dx,dy)
    ex,ey = (x-dx, y-dy )
    print("ex,ey=", ex,ey)
    fx,fy = pixel2view(ex,ey)
    print("fx,fy=", fx,fy)
    global center_pos
    nx, ny = center_pos
    #MoveMouse( nx+fx, ny+fy  ) 
    click( nx+fx, ny+fy, 1.0  ) 
    time.sleep(3.0) 


def click_NPC(name):   # pixel x,y
    # 見えている範囲の人物やオブジェクトをクリックする。
    # 指定された pixel 周辺をマウスで動かす。
    # マウスの形状変化した箇所をクリックする。
    x, y = get_name2pixel(name)
    # click_pixel(x,y)

    cx,cy = getPositionNew()
    print("cx,cy=", cx,cy)
    dx,dy = pos2pixel(cx,cy)
    print("dx,dy=", dx,dy)
    ex,ey = (x-dx, y-dy )
    print("ex,ey=", ex,ey)
    fx,fy = pixel2view(ex,ey)
    print("fx,fy=", fx,fy)
    global center_pos
    nx, ny = center_pos
    # click( nx+fx, ny+fy, 1.0  ) 
    xx = nx+fx
    yy = ny+fy

    MoveMouse(xx, yy)
    time.sleep(0.1)
    if is_NPC():
        print("found", name )
        click(x,y, 2.0)
        return
    else:
        gen = circle_around( (xx,yy), 20 ) 
        thres = 30
        for i in range(thres):
            j, point = next(gen)
            xx, yy = point
            MoveMouse(xx, yy)
            time.sleep(0.1)
            if is_NPC():
                print("found", name )
                click(xx,yy, 2.0)
                return
    print("not found", name)



def move_toward(x,y):   #position x,y
    if is_reached(x,y):
        return

    cx,cy = getPositionNew()

    a = x-cx
    a = a * 1.7
    b = y-cy
    c = math.sqrt( abs(a)**2 + abs(b)**2) 

    # print( "x:%d, y:%d, cx:%d, cy:%d, a:%d, b:%d, c:%d" % ( x,y,cx,cy,a,b,c ) )  

    global center_pos
    nx, ny = center_pos
    '''
    bx = nx + int(200*a/c)
    by = ny + int(200*b/c)
    print( "click %d,%d" % ( bx,by) ) 
    click(bx,by)
    '''
    for radius in range(200,300,20):
        bx = nx + int(radius * a/c)
        by = ny + int(radius * b/c)
        # print("checking %d,%d" % (bx,by) ) 
        MoveMouse(bx, by) 
        time.sleep(0.1)
        #if is_enemy() or is_roten():
        if is_enemy() or is_roten() or is_player():
            continue
        else:
            # print( "click %d,%d" % ( bx,by) ) 
            click(bx,by)
            break


def move_to(x,y):   #position x,y
    #for i in range(100): 
    #while True:
    #for i in range(10):
    for i in range(5):
        move_toward(x,y)
        map_locate("path.png")
        time.sleep(0.5) 
        if is_reached(x,y):
            # break
            return True
    return False

############################
# cursor 関係

def setCursorNormal():
    global cursor
    focusRS()
    clickCenter()
    time.sleep(0.1)
    out = win32gui.GetCursorInfo()  # flags, hcursor, (x,y) = GetCursorInfo()
    cursor["normal"] = out[1]

def getCursor():
    global cursor

    out = win32gui.GetCursorInfo()  # flags, hcursor, (x,y) = GetCursorInfo()
    if out[1] ==cursor["normal"]:
        #print("normal")
        return "normal"
    if 0 <= cursor["enemy"] and out[1] ==cursor["enemy"]:
        #print("enemy")
        return("enemy")
    if 0 <= cursor["NPC"] and out[1] ==cursor["NPC"]:
        #print("NPC")
        return("NPC")
    if 0 <= cursor["roten"] and out[1] ==cursor["roten"]:
        #print("roten")
        return("roten")

    info = win32gui.GetIconInfo( out[1] ) 
    print(info)

    if info[1] == 9:    # NPC 
        cursor["NPC"] = out[1]
        #print("NPC")
        return("NPC")

    if info[1] == 1:    # roten 
        cursor["roten"] = out[1]
        #print("roten")
        return("roten")

    # enemy
    cursor["enemy"] = out[1]
    #print("enemy")
    return("enemy")


def is_NPC():
    if getCursor() == "NPC":
        return True
    else:
        return False


def is_enemy():
    if getCursor() == "enemy":
        return True
    else:
        return False

def is_roten():
    if getCursor() == "roten":
        return True
    else:
        return False


def is_player():
    #debug = False
    debug = True
    global player
    x, y = pyautogui.position()
    time.sleep(0.1)
    sc = pyautogui.screenshot( region=( x-50, y-100, 100, 150 ) ) 
    sc = np.array(sc)
    sc = cv2.cvtColor(sc, cv2.COLOR_RGB2BGR)
    #pos = compare_bitmap( sc, player ) 
    val = check_enchanted_status( sc, player) 
    print("is_player: val=", val) 
    if val > 0.99:
        return True
    else:
        return False


# cursor type
# 
# (1, 524887, (395, 338))  通常
# (1, 13435405, (513, 302))   吹き出し
# (1, 8258077, (302, 390))   fighting(敵)
# (1, 1376837, (467, 166))  ハンド 露店など

def adjustRSWindow():

    #window = pyautogui.getWindow('Red Stone')  が no attribute error になる

    handle = win32gui.FindWindow(None, "Red Stone")  
    # l, t, r, b = win32gui.GetWindowRect(handle)
    # print(handle)
    # ウィンドウの移動
    # MoveWindow(ウィンドウハンドル, x座標, y座標, 横幅, 縦幅, 再描画するか)

    #(3,22) が (0,0) に来るようにする
    win32gui.MoveWindow(handle,-3,-22,800 + 6 ,600 + 22 , 1)

def resetRSWindow():
    # 元の位置に戻す

    handle = win32gui.FindWindow(None, "Red Stone")  
    # l, t, r, b = win32gui.GetWindowRect(handle)
    # print(handle)
    # ウィンドウの移動
    # MoveWindow(ウィンドウハンドル, x座標, y座標, 横幅, 縦幅, 再描画するか)

    #(0,0) が (0,0) に来るようにする
    win32gui.MoveWindow(handle,0,0,800,600, 1) 



def show_np_array(name, np_array): 
    print( name, np_array) 
    cv2.imshow(name, np_array)
    cv2.moveWindow(name, 1000,20)
    cv2.waitKey(5000)


##################################

def RSlogin():
    time.sleep(3.0)

    # click ID area
    MoveMouse(656,333, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(656,333, M_LEFTUP)
    time.sleep(0.1)

    # erase existing chars
    for i in range(10):
        PressKey( DIK_RIGHT ) 
        time.sleep(0.01)
    for i in range(10):
        PressKey( DIK_BACK ) 
        time.sleep(0.01)

    # input ID
    chars = list('LAOCOON')
    for char in chars:
        # x = ord(char)
        x = eval( "DIK_" + char ) 
        #print(x, hex(x))
        PressKey(x)
        time.sleep(0.01)
        ReleaseKey(x)
        time.sleep(0.01)

        #myPressKey(x)
        #time.sleep(0.1)
        #myReleaseKey(x)
        #time.sleep(0.1)

    # input password
    # click password area 
    MoveMouse(656,353, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(656,353, M_LEFTUP)
    time.sleep(0.1)

    # erase existing chars
    for i in range(10):
        PressKey( DIK_RIGHT ) 
        time.sleep(0.01)
    for i in range(10):
        PressKey( DIK_BACK ) 
        time.sleep(0.01)

    chars = list('HEIDEGGER2009')
    for char in chars:
        # x = ord(char)
        x = eval( "DIK_" + char ) 
        #print(x, hex(x))
        PressKey(x)
        time.sleep(0.01)
        ReleaseKey(x)
        time.sleep(0.01)

    PressKey(DIK_RETURN)
    time.sleep(0.01)
    ReleaseKey(DIK_RETURN)
    time.sleep(0.01)


    MoveMouse(658,421, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(658,421, M_LEFTUP)
    time.sleep(0.1)

    # wait until number is displayed
    time.sleep(3.0)

    # 数字画像取得

    sc = pyautogui.screenshot(region=(358,320,91,28  )) 
    sc.save('number.png')

    # 数字認識
    img = Image.open( 'number.png')
    # print(img)


    #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    #number = pytesseract.image_to_string(img)

    '''
    txt = tool.image_to_string(
        img,
        lang="eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))
    '''

    process = subprocess.run(
            [
                #'C:\Users\IEUser\Downloads\Capture2Text_v4.6.2_32bit\Capture2Text\Capture2TextCLI.exe',
                'c:/Users/IEUser/Downloads/Capture2Text_v4.6.2_32bit/Capture2Text/Capture2Text_CLI.exe',
                "-i",
                "number.png"], 
            check=True,stdout=subprocess.PIPE) 
    #number= process.stdout.decode(cp932).strip()
    number= process.stdout  # byte 文字列
    number = number.decode('utf-8').strip()
    print(number + "<" )

    # 入力欄をクリック

    MoveMouse(400,385, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(400,385, M_LEFTUP)
    time.sleep(0.1)

    # 数字入力
    chars = list(number)
    for char in chars:
        # x = ord(char)
        x = eval( "DIK_" + char ) 
        #print(x, hex(x))
        PressKey(x)
        time.sleep(0.1)
        ReleaseKey(x)
        time.sleep(0.1)

    time.sleep(1.0)
    MoveMouse(365,414, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(365,414, M_LEFTUP)
    time.sleep(1.0)

    # より安全なワンタイム・・・ -> "いいえ"
    
    MoveMouse(449,352) 
    time.sleep(1.0)
    click(449,352) 
    time.sleep(1.0)
    click(449,352) 
    
#####################


# inventry 

#####################

# skill

#####################

def initialize2(mapname):
    print("entered initialize2")
    # 新マップに入ったときの一連の処理
    # goto_object() から呼ばれることを想定
    global status
    closeMap()
    closeDialogue()
    #getFieldName()
    getMapName(mapname)
    #getCP()
    getCPNew()
    getHP()
    setCursorNormal()
    getPositionNew()
    #prepare_world_map()
    #load_map_pos2pixel()
    update_map_pos2pixel()
    print( json.dumps(status, ensure_ascii=False, indent=4 )  ) 



def initialize():
    os.chdir("z:\\")
    global status
    # RS window の位置の調整
    # login していなければ login する
    # character の選択と login 
    # map, chat window の shrink
    # 現在MAP の確認
    # 
    # 非 async 関数

    os.chdir("z:\\")
    adjustRSWindow()
    focusRS()
    if pyautogui.locateOnScreen( "img/REDSTONE.bmp", grayscale=True, region=(0,0,800,600 ),confidence=0.9):
        print("ログイン画面")
        # ログイン画面
        RSlogin()

    if pyautogui.locateOnScreen( "img/warlocks.png", grayscale=True, region=(0,0,800,600 ),confidence=0.9):
        # キャラクタ選択画面
        print("キャラクタ選択画面")
        character_login("warlocks")

    # 何かの確認メッセージボックスが表示されたいたらどける。
    # pos = pyautogui.locateCenterOnScreen( "img/確認.bmp", grayscale=True, region=(0,0,800,600 ),confidence=0.9)
    pos = pyautogui.locateCenterOnScreen( "img/kakunin.bmp", grayscale=True, region=(0,0,800,600 ),confidence=0.9)
    if pos is not None:
        print("確認ダイアログ")
        x,y = pos
        print(x,y)
        click(x,y,0.5)
        time.sleep(1.0)

    # ログインボーナスのキャンセル
    pos = pyautogui.locateCenterOnScreen( "img/x_button.bmp", grayscale=True, region=(0,0,800,600 ),confidence=0.9)
    if pos is not None:
        print("ログインボーナス")
        x,y = pos
        print(x,y)
        click(x,y,0.5)
        time.sleep(1.0)

    closeMap()
    closeDialogue()
    #getFieldName()
    prepare_world_map()
    prepare_skill()
    getMapName()
    #getCP()
    getCPNew()
    getHP()
    setCursorNormal()
    getPositionNew()
    #load_map_pos2pixel()
    update_map_pos2pixel()
    print( json.dumps(status, ensure_ascii=False, indent=4 )  ) 

########################

def op総合ポータル( scroll_count, x, y ):
    print("entered op総合ポータル")
    time.sleep(1.0)
    PressKey(DIK_1) # 総合ファーストポータルサービスを利用します
    time.sleep(1.0)
    for i in range(scroll_count) :
        click(747,269)
    click(x,y)
    time.sleep(1.0)
    click(353,353)  # **に移動します。ポータル利用料 1万gold 「はい」

##################


@asyncio.coroutine
def loop_update_status():
    global status
    #while True:
    for i in range(10000):
        if i % 3 == 0:
            getHP()
            getCPNew()
            update_enchanted_status()
            if not status["enchanted"]["haste"][0]: # haste が切れている           
                if status["where"] != "gate":
                    print(">>>haste")
                    clickCenter()
                    PressKey( DIK_W ) 
                    time.sleep(0.01)
                    ReleaseKey(DIK_W)
                    time.sleep(0.01)

            # getPositionNew()
        yield from asyncio.sleep(0.001)

