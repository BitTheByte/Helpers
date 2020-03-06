from collections import namedtuple
import threading
import time
import signal
import sys
import types
import sys

class Channel(object):
    def __init__(self,name='default'):
        self.name = name
        self.__stop = False
        self.__items = []
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self,sig,frame):
        self.__stop = True
        sys.exit(0)

    def append(self,item):
        self.__items.append(item)

    def pop(self):
        if len(self.__items) > 0:
            return True, self.__items.pop(0)
        return False, None

    def __str__(self):
        return str(self.__items)

    def __len__(self):
        return len(self.__items)

    def open(self):
        return not self.__stop

    def wait(self):
        while len(self.__items)  > 0:
            time.sleep(0.1)

    def close(self):
        self.__stop = True


result = namedtuple("Result","func ret args channel wid")

def _worker(wid,target,channel,callback=None):
    while( channel.open() ):
            ok, args = channel.pop()
            if not ok: time.sleep(0.50); continue

            if type(callback) == types.FunctionType:
                callback(result(wid= wid, channel= channel,
                            func    = target,
                            args    = args,
                            ret     = target(args),
                        ))

def workers(target,channel,count=5,callback=None):
    for _id in range(1,count+1):
        threading.Thread(target=_worker,args=(_id,target,channel,callback,)).start()


# Example 
mychannel = Channel() # Channel for sending function arguments 

def hello_world(num):
    time.sleep(2)
    return num * 5

def on_finish(result):
    ret = result.ret
    arg = result.args
    print("Hello(%s) returned: %s\n" % (arg,ret),end='')

mychannel.append(10)       # channels could be initialized before workers
mychannel.append(20)       # channels could be initialized before workers                                                                  
                                                                  
workers(                                                                  
    target   = hello_world,    # function pointer
    channel  = mychannel,      # array which contains arguments                                           
    count    = 2,              # number of simultaneous runs of the target function
    callback = on_finish       # callback funtion which get executed on every target function finished                                               
)        
                                                                  
mychannel.append(30)      # channels could be populated while the workers are running
mychannel.append(40)      # channels could be populated while the workers are running

mychannel.wait()         # waiting workers to finish everything
mychannel.close()        # channel signal to shutdown workers 
