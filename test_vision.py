
import time
from include import *
from vision import *

#focusRS()
# global status
def main():
    initialize()
    #for i in range(100): 
    #for i in range(20): 
    while True: 

        find_moving_objects_while_moving()
        # time.sleep(0.1)

if __name__ == '__main__':
    main()

