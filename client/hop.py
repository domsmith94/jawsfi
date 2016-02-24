from threading import Thread
from subprocess import Popen, PIPE
from signal import SIGINT
import time
import threading
import os
import sys

class HoppingThread(Thread):
	# This is the thread we will use for channel HoppingThread

	def __init__(self, args):
		super(HoppingThread, self).__init__()
		self._stop = threading.Event()
	        self.args = args
		self.DN = open(os.devnull, 'w')
	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

	def run(self):

		channelNum = 0
		maxChan = 11
		err = None

		while not self.stopped():

			if self.args.channel:
				with lock:
			                channelNum = self.args.channel
			else:
				channelNum +=1
				if channelNum > maxChan:
					channelNum = 1

				try:
					if not self.stopped():
				                proc = Popen(['iw', 'dev', self.args.interface, 'set', 'channel', str(channelNum)], stdout=self.DN, stderr=PIPE)
				except OSError:
					print '['+R+'-'+W+'] Could not execute "iw"'
					os.kill(os.getpid(),SIGINT)
					sys.exit(1)
				for line in proc.communicate()[1].split('\n'):
					if len(line) > 2: # iw dev shouldnt display output unless there's an error
						err = '['+R+'-'+W+'] Channel hopping failed: '+R+line+W

			if err:
				print err
			time.sleep(5)
