
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


def loop_vision(status_shared):
    print( "loop_vision cpu id:", multiprocessing.current_process().name ) 
    while True: 
        find_moving_objects_while_moving()


def loop_update_enchanted_status(status_shared, obj ):
    print( "loop_update_enchanted_status cpu id:", multiprocessing.current_process().name ) 
    # status = status_shared
    #status_enchanted = pickle.loads(obj) 
    global status
    status['enchanted'] = pickle.loads(obj) 

    prepare_skill()

    while True:
        update_enchanted_status()
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

        # haste 状態でなければ自分にhaste する
        if status["enchanted"]["haste"][0]:
            pass
        else:
            hasteMe()
        time.sleep(1.0) 

def loop_goto_object(status_shared):
    print( "loop_goto_object cpu id:", multiprocessing.current_process().name ) 
    while True:
        goto_object("洞窟狼")
        goto_object("シンク")

if __name__ == "__main__":

    initialize()
    # multiprocessing.set_start_method(method)
    manager = Manager()
    status_shared = manager.dict()
    # status2 = manager.dict()

    # global status
    for key, value in status.items():
        status_shared[key] = value

    update_enchanted_status()
    obj = pickle.dumps( status['enchanted'] ) 

    Process(target=loop_vision,                 args=(status_shared,)).start()
    Process(target=loop_update_enchanted_status,args=(status_shared, obj,)).start()
    #Process(target=loop_goto_object,            args=(status_shared,)).start()

    print( "parent cpu id:", multiprocessing.current_process().name ) 
    #goto_object("洞窟狼")
    goto_object("シンク")
    #goto_object( "エルフ戦士長") 

    '''
    while True:
        #print('\033[2J') # clear the screen
        print(status)
        time.sleep(1.0)
    '''
