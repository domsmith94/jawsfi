#!/usr/bin/env python

from threading import Thread, Lock
from subprocess import Popen, PIPE
from signal import SIGINT, signal
import argparse
import os
import sys
import time

# Console colors
W = '\033[0m'  # white
R = '\033[31m' # red
G = '\033[32m' # green

# Get arguments
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
    			"--interface",
                        help="Choose monitor mode interface. \
                                Example: -i mon5",
    			required=True)

    parser.add_argument("-c",
                        "--channel",
                        help="Listen for probe requests only on the specified channel. \
                                Example: -c 6")
    return parser.parse_args()

'''
Adapted from wifijammer.py
'''
# Hop channel loop
def channel_hop(args):

    channelNum = 0
    maxChan = 11
    err = None

    while 1:
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

def enable_monitor(interface):
    print '['+G+'+'+W+'] Starting monitor mode for '+G+interface+W
    try:
        os.system('ifconfig %s down' % interface)
        os.system('iwconfig %s mode monitor' % interface)
        os.system('ifconfig %s up' % interface)
    except Exception:
        sys.exit('['+R+'-'+W+'] Could not start monitor mode')

def disable_monitor(interface):
    print '['+R+'+'+W+'] Stopping monitor mode for '+R+interface+W
    try:
        os.system('ifconfig %s down' % interface)
        os.system('iwconfig %s mode managed' % interface)
        os.system('ifconfig %s up' % interface)
    except Exception:
        sys.exit('['+R+'-'+W+'] Could not disable monitor mode')

# Shutdown jawsfi
def stop(signal, frame):
    disable_monitor(interface)
    sys.exit('Closing')

# Run
if __name__ == "__main__":
    if os.geteuid():
        sys.exit('['+R+'-'+W+'] Run using sudo.')
    args = parse_args()
    interface = args.interface
    DN = open(os.devnull, 'w')
    
    # Start the interface
    enable_monitor(interface)

    # Start channel hopping thread
    hop = Thread(target=channel_hop, args=(args,))
    hop.daemon = True
    hop.start()

    signal(SIGINT, stop)
    
    # Packet sniffing code
    while 1:
        continue
