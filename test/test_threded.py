# coding = utf-8
import threading
import time
from werkzeug.local import Local

my_obj = Local()
my_obj.b = 1


def worker():
    my_obj.b = 2
    print('in new thread b is:' + str(my_obj.b))


new_thread = threading.Thread(target=worker)
new_thread.start()
time.sleep(3)
print('in main threaded b is:' + str(my_obj.b))
