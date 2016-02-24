from threading import Thread
import threading
import time

class HoppingThread(Thread):
    # This is the thread we will use for channel HoppingThread

    def __init__(self):
        super(HoppingThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):

        channelNum = 0
        maxChan = 11
        err = None

        while not self.stopped():

            if args.channel:
                with lock:
                   channelNum = args.channel
            else:
                channelNum +=1
                if channelNum > maxChan:
                    channelNum = 1

                try:
                    proc = Popen(['iw', 'dev', args.interface, 'set', 'channel', str(channelNum)], stdout=DN, stderr=PIPE)
                except OSError:
                    print '['+R+'-'+W+'] Could not execute "iw"'
                    os.kill(os.getpid(),SIGINT)
                    sys.exit(1)
                for line in proc.communicate()[1].split('\n'):
                    if len(line) > 2: # iw dev shouldnt display output unless there's an error
                        err = '['+R+'-'+W+'] Channel hopping failed: '+R+line+W
            
            if err:
                print err
        if args.channel:
                time.sleep(.05)