import queue
import threading

class Threader:
	def __init__(self,pool_size=1):
		self.q = queue.Queue()
		self.pool_size = pool_size

	def __t(self):
		thread = self.q.get()
		thread.daemon=True
		thread.start()

	def __name(self):
		return "CUSTOM+THREAD"

	def __wait(self):
		while 1:
			running = threading.enumerate()
			remain = [x.name for x in running if self.__name() in x.name]
			if not remain:
				break


	def on_waiting(self):
		return self.q.qsize()


	def pop(self):
		return self.q.queue.pop()

	def finish_all(self):
		for _ in xrange(self.q.qsize()): self.__t()
		self.__wait()


	def put(self,target,args):
		if self.q.qsize() < self.pool_size:
			self.q.put(threading.Thread(target=target,name=self.__name(),args=tuple(args)))

		if self.q.qsize() >= self.pool_size:
			for _ in xrange(self.q.qsize()): self.__t()
			self.__wait()


""" USAGE EXAMPLE

import time
from random import randint

def worker(x):
	time.sleep(randint(1,3))
	print "worker({0}) finished\n".format(x),


t = Threader(3)
print "starting workers 1"
t.put(worker,["1"])
t.put(worker,["2"])
t.put(worker,["3"])

trint "starting workers 2"
t.put(worker,["4"])
t.put(worker,["5"])
t.put(worker,["6"])

"""
