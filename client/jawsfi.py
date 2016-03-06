#!/usr/bin/env python

from threading import Thread, Lock
from signal import SIGINT, signal
from hop import HoppingThread
from sniff import SniffingThread
import argparse
import os
import sys
import time
import json
import pprint
import requests

# Server URL
server_url = 'https://jawsfi-soton.appspot.com' #os.environ.get['JAWSFI_SERVER'] or 'localhost:5000'

# Set auth token
result_data = {'auth': '3bd44669-0290-4f3a-991f-84187f5fc02a'}

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

def enable_monitor(interface):
	print '['+G+'+'+W+'] Starting monitor mode for '+G+interface+W
	try:
		os.system('ifconfig %s down' % interface)
		os.system('iwconfig %s mode monitor' % interface)
		os.system('ifconfig %s up' % interface)
	except Exception:
		sys.exit('['+R+'-'+W+'] Could not start monitor mode')

def disable_monitor(interface):
	print '['+R+'-'+W+'] Stopping monitor mode for '+R+interface+W
	try:
		os.system('ifconfig %s down' % interface)
		os.system('iwconfig %s mode managed' % interface)
		os.system('ifconfig %s up' % interface)
	except Exception:
		sys.exit('['+R+'-'+W+'] Could not disable monitor mode')

def send_result(stash):
	result_data.update(stash)
        try:
	    response = requests.post(server_url + '/send-data', json = result_data)
	    return response.status_code == requests.codes.ok
        except requests.exceptions.RequestException as e:
            return False

def send_results():
	# add the current stash to list of unsent stashes
	stashes.append(sniff.get_reset())
	# attempt to send all unsent stashes, if not recieved keep in unsent
	# to attempt later
	stashes[:] = [stash for stash in stashes if not send_result(stash)]

# Shutdown jawsfi
def stop(signal, frame):
    hop.stop()
    sniff.stop()
    disable_monitor(interface)
    sys.exit('['+R+'-'+W+'] Shutting down jawsfi...')

# Run
if __name__ == "__main__":
	if os.geteuid():
		sys.exit('['+R+'!'+W+'] Run using sudo.')
	args = parse_args()
	interface = args.interface
	stashes = []
	# Start the interface
	enable_monitor(interface)

	# Start channel hopping thread
	hop = HoppingThread(args)
	hop.start()

	sniff = SniffingThread(interface)
	sniff.start()
        print '['+G+'+'+W+'] Using server: ' + server_url
        print '['+G+'+'+W+'] Capturing probe requests from: '+G+interface+W
	signal(SIGINT, stop)
	while 1:
		time.sleep(15)# every 10 minutes
		send_results()

	stop(None, None)
