from threading import Thread
from datetime import datetime
import pyshark
import threading


# Console colors
W = '\033[0m'  # white
R = '\033[31m' # red
G = '\033[32m' # green

class SniffingThread(Thread):
    # This is the thread we will use for sniffing traffic

    def __init__(self, interface):
        super(SniffingThread, self).__init__()
        self._stop = threading.Event()
        self.stash = {}
        self.interface = interface

    def stop(self):
        self._stop.set()

    def stopped(self):
	return self._stop.isSet()

    def get_reset(self):
        data = self.stash.copy()
        self.stash = {}
        return data

    def run(self):
        # Packet sniffing code
    	capture = pyshark.LiveCapture(interface=self.interface, display_filter='wlan.fc.type_subtype eq 4')
    	#capture.set_debug()


    	for packet in capture.sniff_continuously():
            if self.stopped():
                break
    	    self.stash[packet.wlan.ta_resolved] = (packet.radiotap.dbm_antsignal, datetime.now().isoformat())
