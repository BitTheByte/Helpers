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

	def __wait(self):
		while len(threading.enumerate()) > 1:
			pass

	def on_waiting(self):
		return self.q.qsize()


	def pop(self):
		return self.q.queue.pop()

	def finish_all(self):
		for _ in xrange(self.q.qsize()): self.__t()
		self.__wait()


	def put(self,target,args):

		if self.q.qsize() < self.pool_size:
			self.q.put(threading.Thread(target=target,args=tuple(args)))

		if self.q.qsize() >= self.pool_size:
			for _ in xrange(self.q.qsize()): self.__t()
			self.__wait()
