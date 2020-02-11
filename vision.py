

import scipy.signal
import time
#import pprint
import pyautogui
import cv2
import numpy as np

from globals import *
from basics import *
#from include import *

# player が移動しているので上記の 静止画像からの moving object tectecton は
# そのままでは利用できない。
# frame差分を取る前に並行移動量を調べて compensate する。
# python - How to detect a shift between images - Stack Overflow https://stackoverflow.com/questions/24768222/how-to-detect-a-shift-between-images



def cross_image(im1, im2):
    # get rid of the color channels by performing a grayscale transform
    # the type cast into 'float' is to avoid overflows
    #im1_gray = np.sum(im1.astype('float'), axis=2)
    #im2_gray = np.sum(im2.astype('float'), axis=2)
    im1_gray = im1.astype('float')
    im2_gray = im2.astype('float')

    # get rid of the averages, otherwise the results are not good
    im1_gray -= np.mean(im1_gray)
    im2_gray -= np.mean(im2_gray)
 
    #print(im1_gray)
    #print(im2_gray)
    # calculate the correlation image; note the flipping of onw of the images
    #return scipy.signal.fftconvolve(im1_gray, im2_gray[::-1,::-1], mode='same')
    corr_img = scipy.signal.fftconvolve(im1_gray, im2_gray[::-1,::-1], mode='same')
     
    shift = np.unravel_index(np.argmax(corr_img), corr_img.shape)
    print(shift)
    



# フレーム差分の計算
def frame_sub(img1, img2, img3, th):

    #chat_area = [1,467, 149-1,490-467]
    #player_area = [360,146,444-360,292-146 ]
    # フレームの絶対差分
    diff1 = cv2.absdiff(img1, img2)
    diff2 = cv2.absdiff(img2, img3)

    # 2つの差分画像の論理積
    # diff = cv2.bitwise_and(diff1, diff2)
    diff = cv2.bitwise_or(diff1, diff2)

    # 二値化処理
    diff[diff < th] = 0
    diff[diff >= th] = 255
    
    # メディアンフィルタ処理（ゴマ塩ノイズ除去）
    mask = cv2.medianBlur(diff, 3)

    return  mask

def find_moving_objects():

    # カメラのキャプチャ

    sc1 = pyautogui.screenshot( region=(0,0,800, 495) )
    frame1 = cv2.cvtColor(np.array(sc1), cv2.COLOR_RGB2GRAY)
    time.sleep(0.01)
    sc2 = pyautogui.screenshot( region=(0,0,800, 495) )
    src = np.array(sc2)
    frame2 = cv2.cvtColor(np.array(sc2), cv2.COLOR_RGB2GRAY)
    time.sleep(0.01)
    sc3 = pyautogui.screenshot( region=(0,0,800, 495) )
    frame3 = cv2.cvtColor(np.array(sc3), cv2.COLOR_RGB2GRAY)

    detect_count = 0
    moving_objects = []

    for t in range(100):


        #print(t, flush=True)
        # フレーム間差分を計算
        #mask = frame_sub(frame1, frame2, frame3, th=30)
        #mask = frame_sub(frame1, frame2, frame3, th=10)
        #mask = frame_sub(frame1, frame2, frame3, th=5)
        mask = frame_sub(frame1, frame2, frame3, th=3)

        cross_image(frame1, frame2)
        cross_image(frame2, frame3)
        ############

        # 輪郭を抽出
        #   contours : [領域][Point No][0][x=0, y=1]
        #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
        #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
        #contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        # 矩形検出された数（デフォルトで0を指定）
        detect_count = 0
        moving_objects = []

        # 各輪郭に対する処理
        for i in range(0, len(contours)):
                            
            # 輪郭の領域を計算
            area = cv2.contourArea(contours[i])
           
            # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
            #if area < 1e2 or 1e5 < area: # 1e2 = 100, 1e5 = 100000
            #if area < 1e2:
            #if area < 50:
            if area < 200:
                continue
            if 1e5 < area:
                continue
           
            # 外接矩形
            if len(contours[i]) > 0:
                rect = contours[i]
                x, y, w, h = cv2.boundingRect(rect)
            
                global chat_area
                global player_area
                if is_inside( chat_area, [x,y,w,h ]) or is_inside( player_area, [x,y,w,h ] ):
                    continue
                moving_objects.append( [x,y,w,h ] ) 
                cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
               
                # 外接矩形毎に画像を保存
                # cv2.imwrite('{ファイルパス}' + str(detect_count) + '.jpg', src[y:y + h, x:x + w])
               
                detect_count = detect_count + 1

        # 外接矩形された画像を表示
        cv2.imshow('output', src)
        cv2.moveWindow("output", 900,20)
        cv2.waitKey(100)

        print( "detect %d moving object" % (detect_count ), flush=True )

        '''
        if 100 < detect_count :
            # maybe plyaer is moving
            # clickCenter()   # player を静止させる
            # time.sleep(1.0)

            print("too many moving objects: maybe player is moving") 

        else:
            if 0 < detect_count :
                return moving_objects
        '''



        # 3枚のフレームを更新
        frame1 = frame2
        frame2 = frame3
        sc = pyautogui.screenshot( region=(0,0,800, 495) )
        src = np.array(sc)
        frame3 = cv2.cvtColor(np.array(sc), cv2.COLOR_RGB2GRAY)
            
'''
【Python/OpenCV】フレーム間差分法で移動物体の検出 | 技術雑記 https://algorithm.joho.info/programming/python/opencv-frame-difference-py/

Basic motion detection and tracking with Python and OpenCV - PyImageSearch https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

PythonとOpenCVを使って物体検出をやってみた - Qiita https://qiita.com/neriai/items/448a36992e308f4cabe2

'''

