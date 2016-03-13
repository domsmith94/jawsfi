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
auth_token = '3bd44669-0290-4f3a-991f-84187f5fc02a'

# Set result data template
result_data = {'auth': auth_token}

# Console colors
W = '\033[0m'  # white
R = '\033[31m' # red
G = '\033[32m' # green

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
	hop_thread.stop()
	sniff_thread.stop()
	disable_monitor(interface)
	sys.exit('['+R+'-'+W+'] Shutting down jawsfi...')

def register_request(name):
	try:
		response = requests.post(server_url + '/register', json = {'auth': auth_token, 'name': name})
		return response.status_code == requests.codes.ok
	except requests.exceptions.RequestException as e:
		return False

def register():
	print '['+G+'+'+W+'] Regeristing device...'

	parser = argparse.ArgumentParser(
			description='Register device with server')

	parser.add_argument("-n",
				"--name",
				help="Specify device name.",
				required=True)

	args = parser.parse_args(sys.argv[2:])

	if register_request(args.name):
		print '['+G+'+'+W+'] Sucessfully registered device.'
	else:
		print '['+R+'!'+W+'] Failed to register device.'

def sniff():
	global hop_thread, sniff_thread, interface
	if os.geteuid():
		sys.exit('['+R+'!'+W+'] Run using sudo for sniffing traffic.')

	parser = argparse.ArgumentParser(
			description='Sniff packets and send to server')
	parser.add_argument("-i",
				"--interface",
			help="Choose monitor mode interface. \
			Example: -i mon5",
			required=True)

	parser.add_argument("-c",
			"--channel",
			help="Listen for probe requests only on the specified channel. \
			Example: -c 6")

	args = parser.parse_args(sys.argv[2:])

	interface = args.interface

	stashes = []
	# Start the interface
	enable_monitor(interface)

	# Start channel hopping thread
	hop_thread = HoppingThread(args)
	hop_thread.start()

	sniff_thread = SniffingThread(interface)
	sniff_thread.start()
	print '['+G+'+'+W+'] Capturing probe requests from: '+G+interface+W
	signal(SIGINT, stop)
	while 1:
		time.sleep(15)# every 10 minutes
		send_results()

	stop(None, None)

# Set commands
commands = {'register': register, 'sniff': sniff}

# Run
if __name__ == "__main__":
	print '['+G+'+'+W+'] Using server: ' + server_url

	parser = argparse.ArgumentParser(
		usage='''jawsfi <command> [<args>]

	 register    Register a device with jawsfi server
	 sniff       Sniff and send traffic
	''')
	parser.add_argument('command', help='Subcommand to run')
	args = parser.parse_args(sys.argv[1:2])

	if (not args.command) or (args.command not in commands):
		print 'Unrecognised command'
		parser.print_help()
	else:
		commands[args.command]()
