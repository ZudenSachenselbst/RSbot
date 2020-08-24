import sys
from include import *
from vision import *

import pickle 
import time
from multiprocessing import Process, Manager, Value
import multiprocessing

#from pprint import pprint

import colorama
from colorama import Fore, Back, Style
colorama.init(convert=True)


def loop_vision(moving_objects_shared):
    print( "loop_vision cpu id:", multiprocessing.current_process().name ) 
    global moving_objects
    while True: 
        find_moving_objects_while_moving()

        # print("global moving objects:", moving_objects ) 

        #moving_objects_shared = moving_objects
        # moving_objects_shared.clear()     # error
        moving_objects_shared[:] = []
        for item in moving_objects:
            moving_objects_shared.append(item) 


#def loop_update_enchanted_status(status_shared, obj ):
def loop_update_status(status_shared, obj ):
    print( "loop_update_status cpu id:", multiprocessing.current_process().name ) 
    # status = status_shared
    #status_enchanted = pickle.loads(obj) 
    global status
    status['enchanted'] = pickle.loads(obj) 

    prepare_skill()

    while True:
        if( status_shared["where"] == "gate" or 
            status_shared["where"] == "initializing" ):
            print("loop_update_status: sleep ")
            time.sleep(5.0) 

        # 状態更新
        update_enchanted_status()
        getCPNew()
        getHP()
        for key, value in status.items():
            status_shared[key] = value

    
        '''
        print('\033[2J') # clear the screen
        for skill in map_skill2icon: 
            if skill in status["enchanted"]:
                flag = status["enchanted"][skill][0]
                val  = status["enchanted"][skill][1]

                if flag:
                    print( Fore.RED + skill + "\t" + str(val) + "\ton" ) 
                    #print(Style.RESET_ALL)
                else:
                    print( Fore.WHITE + skill + "\t" + str(val) + "\toff" ) 
            # print( Fore.WHITE ) 
        '''

        # haste 状態でなければ自分にhaste する
        if status["enchanted"]["haste"][0]:
            pass
        else:
            hasteMe()

        # HP が半分以下なら heal する
        if ( 0 < status["currentHP"] and 
             0 < status["fullHP"] and 
             status["currentHP"] / status["fullHP"]  < 0.5 ):
            healMe()

        time.sleep(1.0) 

def loop_goto_object(status_shared):
    print( "loop_goto_object cpu id:", multiprocessing.current_process().name ) 
    global status
    status = status_shared
    status["where"] = "initializing"
    initialize()
    status["where"] = ""
    #while True:
    goto_object("洞窟狼")
    #goto_object("シンク")
    #goto_object( "エルフ戦士長") 
    #goto_object( 'ナイルローニ' )

def loop_attack(status_shared, moving_objects_shared):
    print( "loop_attack cpu id:", multiprocessing.current_process().name ) 
    setCursorNormal()
    # while True:
    for i in range(10000):
        print(">>>attacking")
        found_enemy = False
        last_found_enemy_iter = 0 
        for item in moving_objects_shared:
            print("loop_attack: checking ", item)
            bx, by = object_center(item) 
            #(orgX, orgY) = getMousePos()
            MoveMouse(bx, by) 
            #time.sleep(0.1)
            time.sleep(0.1)
            result = is_enemy()
            #MoveMouse(orgX, orgY)   # マウス位置を元に戻す。
            #if is_enemy():
            if result:
                found_enemy = True
                last_found_enemy_iter = i 
                print("loop_attack: found enemy!")
                # attack 
                click(bx,by)
                time.sleep(0.1)
        time.sleep(1.0)
        if ( not found_enemy ) and (i - last_found_enemy_iter > 5 ) :
            break

    print(">>> end of loop_attack")

if __name__ == "__main__":

    print("start main")
    # initialize()
    # multiprocessing.set_start_method(method)
    manager = Manager()
    status_shared = manager.dict()
    # status2 = manager.dict()
    moving_objects_shared = manager.list()

    # global status
    for key, value in status.items():
        status_shared[key] = value

    update_enchanted_status()
    obj = pickle.dumps( status['enchanted'] ) 

    setCursorNormal()

    #Process(target=loop_vision,                 args=(moving_objects_shared,)).start()
    #Process(target=loop_update_enchanted_status,args=(status_shared, obj,)).start()
    #Process(target=loop_goto_object,            args=(status_shared,)).start()

    p_loop_vision        = Process(target=loop_vision,         args=(moving_objects_shared,))
    p_loop_update_status = Process(target=loop_update_status,  args=(status_shared, obj,))
    p_loop_goto_object   = Process(target=loop_goto_object,    args=(status_shared,))
    p_loop_attack        = Process(target=loop_attack,         args=(status_shared, moving_objects_shared,))

    p_loop_goto_object.start() 
    # 初期化の邪魔をしないよう他の処理の開始を遅らせる。
    time.sleep(10.0) 
    p_loop_vision.start()
    p_loop_update_status.start() 


    print( "parent cpu id:", multiprocessing.current_process().name ) 

    while True:
        # 状態表示
        #print('\033[2J') # clear the screen
        print("status:", status_shared)
        print("moving objects:", moving_objects_shared )
        # enchanted 状態の表示
        for skill in map_skill2icon: 
            if skill in status["enchanted"]:
                flag = status["enchanted"][skill][0]
                val  = status["enchanted"][skill][1]

                if flag:
                    print( Fore.RED + skill + "\t" + str(val) + "\ton" ) 
                    #print(Style.RESET_ALL)
                else:
                    print( Fore.WHITE + skill + "\t" + str(val) + "\toff" ) 
            # print( Fore.WHITE ) 

        # if p_loop_attack.is_alive() or p_loop_goto_object.is_alive():  
        #    pass

        if (not p_loop_attack.is_alive()) and (not  p_loop_goto_object.is_alive()):  
            #p_loop_goto_object.start()     # cannot start a process twice 
            p_loop_goto_object   = Process(target=loop_goto_object,    args=(status_shared,))
            p_loop_goto_object.start() 
            # 初期化の邪魔をしないよう他の処理の開始を遅らせる。
            time.sleep(10.0)

        if( status_shared["where"] == "gate" or 
            status_shared["where"] == "initializing" ):
            print("parent : sleep ")
            time.sleep(5.0) 


        # check enemy 
        #if not p_loop_attack.is_alive() and p_loop_goto_object.is_alive():  
        if p_loop_goto_object.is_alive():  
            for item in moving_objects_shared:
                bx, by = object_center(item) 
                #(orgX, orgY) = getMousePos()
                MoveMouse(bx, by) 
                time.sleep(0.1)
                result = is_enemy()
                #MoveMouse(orgX, orgY)   # マウス位置を元に戻す。

                #if is_enemy():
                if result: 
                    print("parent: found enemy!")
                    # attack 
                    p_loop_goto_object.terminate()
                    p_loop_attack = Process(
                            target=loop_attack,         
                            args=(status_shared, moving_objects_shared,))
                    p_loop_attack.start() 

        time.sleep(1.0)

