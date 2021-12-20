from include import *


def main():
    # adjustRSWindow()
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
    MoveMouse(656,363, M_LEFTDOWN)
    time.sleep(0.1)
    MoveMouse(656,363, M_LEFTUP)
    time.sleep(0.1)

    # erase existing chars
    for i in range(10):
        PressKey( DIK_RIGHT ) 
        time.sleep(0.1)
    for i in range(10):
        PressKey( DIK_BACK ) 
        time.sleep(0.1)

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
    


main()

