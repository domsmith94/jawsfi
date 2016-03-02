from threading import Thread
from datetime import datetime
import pyshark

class SniffingThread(Thread):
    # This is the thread we will use for sniffing traffic

    def __init__(self):
        super(SniffingThread, self).__init__()
        self._stop = threading.Event()
		self.stash = {}

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
    	capture = pyshark.LiveCapture(interface=interface, display_filter='wlan.fc.type_subtype eq 4')
    	#capture.set_debug()

    	print '['+G+'+'+W+'] Capturing probe requests from '+G+interface+W

    	for packet in capture.sniff_continuously():
            if self.stopped():
                break
    		print 'Device: ', packet.wlan.ta_resolved, ' Signal: ', packet.radiotap.dbm_antsignal ,'db'
    		stash[packet.wlan.ta_resolved] = (packet.radiotap.dbm_antsignal, datetime.now().isoformat())
