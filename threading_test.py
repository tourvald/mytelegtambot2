import time
import threading

def get_data():
    for i in range(1,20):
        print(time.time())
        time.sleep(1)
print ("active thread:", threading .active_count ())
threading.Thread(target=get_data).start()
print ("active thread:", threading .active_count ())
print ('Работает в фоне')