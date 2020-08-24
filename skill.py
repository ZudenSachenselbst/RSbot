
import sys
import cv2
import datetime
import pyautogui
import numpy as np
from matplotlib import pyplot as plt

from globals import *
from basics import *


map_skill2icon = {
    "fireBolt":        [ "iconSkill/iconSkill_51.png", 0.9, ""],
    "fireBall":        [ "iconSkill/iconSkill_52.png", 0.9, ""],
    # "fireEnchantment": [ "iconSkill/iconSkill_53.png", 0.9, "Effects/enchanted_hot_enchanting/enchanted_hot_enchanting_1.png"], 
    "fireEnchantment": [ "iconSkill/iconSkill_53.png", 0.93, "Effects/enchanted_hot_enchanting/enchanted_hot_enchanting_1.bmp"], 
    "flameStorm":      [ "iconSkill/iconSkill_54.png", 0.9, ""],
    "meteoShower":     [ "iconSkill/iconSkill_55.png", 0.9, ""],
    "mysticFog":       [ "iconSkill/iconSkill_56.png", 0.9, ""],
    "chillingTouch":   [ "iconSkill/iconSkill_57.png", 0.9, ""],
    "iceStaglamite":   [ "iconSkill/iconSkill_58.png", 0.95, "Effects/skill_icy_stalagmite/skill_icy_stalagmite_9.bmp"], 
    "fountainBarrier": [ "iconSkill/iconSkill_59.png", 0.97, "Effects/20200815/fountainBarrier.bmp"], 
    "waterCannon":     [ "iconSkill/iconSkill_60.png", 0.9, ""],
    "levitate":        [ "iconSkill/iconSkill_61.png", 0.9, ""],
    "teleportation":   [ "iconSkill/iconSkill_62.png", 0.9, ""],
    "tornadoShield":   [ "iconSkill/iconSkill_63.png", 0.9, ""],
    "lightningThunder":[ "iconSkill/iconSkill_64.png", 0.9, ""],
    "haste":           [ "iconSkill/iconSkill_65.png", 0.95, "Effects/20200815/haste2.bmp"],     # 移動速度
#    "haste":           [ "iconSkill/iconSkill_65.png", 0.8, "Effects/status_incline/status_incline_7.png"],     # 移動速度
    #"haste":           [ "iconSkill/iconSkill_65.png", 0.9, "Effects/status_incline/status_incline_5.png"],    # 攻撃速度
    "rockBounding":    [ "iconSkill/iconSkill_66.png", 0.9, ""],
    "gravityAmplifier":[ "iconSkill/iconSkill_67.png", 0.9, ""],
    "earthQuake":      [ "iconSkill/iconSkill_68.png", 0.9, ""],
    "earthHeal":       [ "iconSkill/iconSkill_69.png", 0.9, ""],
    "stoneTouch":      [ "iconSkill/iconSkill_70.png", 0.9, ""],
    "charging":        [ "iconSkill/iconSkill_71.png", 0.9, ""],
    "doubleCharging":  [ "iconSkill/iconSkill_72.png", 0.9, ""],
    "turkeyCharging":  [ "iconSkill/iconSkill_73.png", 0.97, "Effects/20200815/turkeyCharging.bmp"],
    # "forbegerCharging":[ "iconSkill/iconSkill_74.png", 0.9, "Effects/status_incline/status_incline_6.png"],     
    # "forbegerCharging":[ "iconSkill/iconSkill_74.png", 0.93, "Effects/status_incline/skill_15.bmp"], 
    "forbegerCharging":[ "iconSkill/iconSkill_74.png", 0.97, "Effects/20200815/forbegerCharging.bmp"], 
    "criticalHit":     [ "iconSkill/iconSkill_75.png", 0.9, ""]

        }

# メモリに effect file を読み込む
def prepare_skill():
    global map_skill2icon
    debug = False
    for skill in map_skill2icon: 
        if debug:
            print(skill, end="")
        #file = map_skill2icon[skill][1]
        file = skill2effectFile(skill) 
        if file == "":
            pass
        else:
            if debug:
                print(file)
            img = cv2.imread(file)
            map_skill2icon[skill].append( img )  


def skill2icon(skill_name):
    global map_skill2icon
    #return map_skill2icon[skill_name]
    return map_skill2icon[skill_name][0]

def skill2thres(skill_name):
    global map_skill2icon
    return map_skill2icon[skill_name][1]

def skill2effectFile(skill_name):
    global map_skill2icon
    #return map_skill2icon[skill_name]
    return map_skill2icon[skill_name][2]

def skill2image(skill_name):
    global map_skill2icon
    return map_skill2icon[skill_name][3]



def reset_wizard_skill_slot():
    #focusRS()
    # click F4, open skill 
    PressKey( DIK_F4 ) 

    skill2slot = { 

        # 左サイド
        "fireBolt":         (24,527),   # enemy 左クリック
        # "fireEnchantment":  ( 38,576),  # 味方  左クリック
                                

        # 中央上段

        "meteoShower":      (102,541),  # Q
        #"heist":            (138,541),  # W
        "haste":            (138,541),  # W
        "charging":         (175,541),  # E
        "doubleCharging":   (210,541),  # R
        "turkeyCharging":   (246,541),  # T

        # 中央下段

        "fireEnchantment":  (102,579 ), # A
        "mysticFog":        (138,579 ), # S
        "fountainBarrier":  (175,579 ), # D
        "iceStaglamite":    (210,579 ), # F
        "forbegerCharging": (246,579 ), # G




        #"flameStorm":       (  ), 
        #"waterCannon":      (  ), 
        #"levitate":         (  ), 
        #"teleportation":    (  ), 
        #"tornadoShield":    (  ), 
        #"lightningThunder": (  ), 
        #"rockBounding":     (  ), 
        #"gravityAmplifier": (  ), 
        #"earthQuake":       (  ), 
        #"stoneTouch":       (  ), 

        #"doubleCharging":   (  ), 
        #"turkeyCharging":   (  ), 
        #"forbegerCharging": (  ), 
        #"criticalHit":      (  ), 

        # 右サイド
        "chillingTouch":    (775,527),       # enemy 右クリック
        "earthHeal":        (760,575 ), # 味方 右クリック

        }  

    for skill_name in skill2slot:
        print(skill_name)
        icon = skill2icon( skill_name ) 
        destination = skill2slot[ skill_name ]

        # scroll up skill list
        click(790,50)
        click(790,50)
        click(790,50)
        click(790,50)

        # find corresponding icon in the list
        pos = None
        for i in range(4):
            pos = pyautogui.locateCenterOnScreen( icon ) 
            if pos is None: 
                click(790,466)  # scroll down 1time
            else:
                break

        print(pos)
        if pos is None:
            continue

        # found skill icon

        MoveMouse(pos.x, pos.y ) 
        time.sleep(0.1)
        MoveMouse(pos.x, pos.y, M_LEFTDOWN)
        time.sleep(0.1)
        # drag icon
        
        MoveMouse(pos.x, pos.y ) 
        time.sleep(0.1)
        MoveMouse( destination[0], destination[1],  M_LEFTUP)
        time.sleep(0.1)


    # close skill tab 
    PressKey( DIK_ESCAPE ) 

################


def hasteMe():
    
    clickCenter(0.01) 
    #time.sleep(0.1)
    x = eval( "DIK_W" ) 
    PressKey(x)
    time.sleep(0.01)
    ReleaseKey(x)
    # time.sleep(0.1)

def healMe():
    global center_pos
    x,y = center_pos
    clickRightButton( x,y ) 

################

# 各種スキルの効果中か判定する

def check_enchanted(imageFile, skillname, method = cv2.TM_CCORR_NORMED):
    effectFile= skill2effectFile(skillname)
    return check_enchanted_file(imageFile, effectFile, method )

def check_enchanted_file(imageFile, effectFile, method = cv2.TM_CCORR_NORMED):
    img = cv2.imread(imageFile) 
    effect = cv2.imread(effectFile) 
    return check_enchanted_status(img, effect, method) 

def check_enchanted_status(img_arg, template_arg, method = cv2.TM_CCORR_NORMED):
    debug = False
    #debug = True

    img      = img_arg.copy()
    template = template_arg.copy()
    mask     = template_arg.copy() 

    #w, h = template.shape[:2]
    h, w = template.shape[:2]
    if debug:
        print( "w,h=", w, h)

    #method =  cv2.TM_CCORR_NORMED
    if method ==  cv2.TM_CCORR_NORMED:
        res = cv2.matchTemplate(img,template,method, mask=mask )
    else:
        res = cv2.matchTemplate(img,template,method) 

    '''
    threshold = 0.85
    loc = np.where( res >= threshold)
    print("loc=", loc)
    if np.any(res  > threshold ) :
        print("found")
    else:
        print("not found")
    '''

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if debug:
        print("max_val=", max_val)

    if debug:
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc


        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.figure(figsize=(40,20), dpi=50)
        #plt.subplot(121),plt.imshow(res,cmap = 'gray')
        #plt.subplot(121),plt.imshow( template,cmap = 'gray')
        #plt.subplot(121),plt.imshow( template)
        #template_rgb = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        plt.subplot(121),plt.imshow( template_arg )

        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title( 'Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle( method )

        plt.show()

    '''
    if max_val > 0.9:
        return True
    else:
        return False
    '''
    return max_val


def update_enchanted_status():

    start = datetime.datetime.now()

    global center_pos
    global status
    #debug = True
    debug = False
    cx = center_pos[0]
    cy = center_pos[1]
    sc1 = pyautogui.screenshot( region=( cx-100, cy-100, 200,200 ) ) 
    rgb = np.array(sc1)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    if debug:
        cv2.imwrite("surroundings.png", bgr)


    global map_skill2icon
    for skill in map_skill2icon: 
        # print("checking1 ", skill, len(map_skill2icon[skill]) )
        if len( map_skill2icon[skill]) == 4: # memory image 有り
            #effect = map_skill2icon[skill][2]
            #effect = map_skill2icon[skill][3]
            effect = skill2image(skill) 
            thres  = skill2thres(skill) 

            # print("checking2 ", skill )
            val = check_enchanted_status( bgr,  effect )
            if val > thres:
                status["enchanted"][skill] = [ True, val] 
            else:
                status["enchanted"][skill] = [ False, val] 


    end = datetime.datetime.now()
    elapse = end - start
    print("update_enchanted_status\t", elapse )
