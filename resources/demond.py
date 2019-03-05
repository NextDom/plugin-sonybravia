# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.

import logging
import string
import sys
import os
import time
import datetime
import re
import signal
import argparse
import globals
from optparse import OptionParser
from os.path import join
import json

try:
	from jeedom.jeedom import *
except ImportError:
	print "Error: importing module jeedom.jeedom"
	sys.exit(1)

def read_socket():
	global JEEDOM_SOCKET_MESSAGE
	if not JEEDOM_SOCKET_MESSAGE.empty():
		logging.debug("Message received in socket JEEDOM_SOCKET_MESSAGE")
		message = json.loads(jeedom_utils.stripped(JEEDOM_SOCKET_MESSAGE.get()))
		if message['apikey'] != _apikey:
			logging.error("Invalid apikey from socket : " + str(message))
			return
		try:
			print 'read'
		except Exception, e:
			logging.error('Send command to demon error : '+str(e))

def listen():
	jeedom_socket.open()
	try:
		while 1:
			time.sleep(0.5)
			read_socket()
	except KeyboardInterrupt:
		shutdown()

# ----------------------------------------------------------------------------

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("Shutdown")
	logging.debug("Removing PID file " + str(_pidfile))
	try:
		os.remove(_pidfile)
	except:
		pass
	try:
		jeedom_socket.close()
	except:
		pass
	try:
		jeedom_serial.close()
	except:
		pass
	logging.debug("Exit 0")
	sys.stdout.flush()
	os._exit(0)

# ----------------------------------------------------------------------------

_log_level = "error"
_socket_port = 55009
_socket_host = 'localhost'
_device = 'auto'
_pidfile = '/tmp/demond.pid'
_apikey = ''
_callback = ''

parser = argparse.ArgumentParser(description='Sony Daemon for Jeedom plugin')
parser.add_argument("--tvip", help="IP TV", type=str)
parser.add_argument("--mac", help="MAC TV", type=str)
parser.add_argument("--psk", help="Cle partage", type=str)
parser.add_argument("--apikey", help="Value to write", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--callback", help="Value to write", type=str)
parser.add_argument("--socketport", help="Socket Port", type=str)
parser.add_argument("--sockethost", help="Socket Host", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
args = parser.parse_args()

if args.tvip:
	globals.tvip = args.tvip
if args.mac:
	globals.mac = args.mac
if args.psk:
	globals.psk = args.psk
if args.loglevel:
	globals.log_level = args.loglevel
if args.apikey:
	globals.apikey = args.apikey
if args.callback:
	globals.callback = args.callback
if args.cycle:
	globals.cycle = float(args.cycle)
if args.socketport:
	globals.socketport = args.socketport
if args.sockethost:
	globals.sockethost = args.sockethost

globals.socketport = int(globals.socketport)
globals.cycle = float(globals.cycle)

jeedom_utils.set_log_level(globals.log_level)
logging.info('GLOBAL------Start sonyd')
logging.info('GLOBAL------Log level : '+str(globals.log_level))
logging.info('GLOBAL------Socket port : '+str(globals.socketport))
logging.info('GLOBAL------Socket host : '+str(globals.sockethost))
logging.info('GLOBAL------Apikey : '+str(globals.apikey))
logging.info('GLOBAL------Callback : '+str(globals.callback))
logging.info('GLOBAL------Cycle : '+str(globals.cycle))
logging.info('GLOBAL------IPTV : '+str(globals.tvip))
logging.info('GLOBAL------MAC : '+str(globals.mac))
logging.info('GLOBAL------PSK : '+str(globals.psk))
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
tmpmac = globals.mac.replace(":","")
globals.pidfile = "/tmp/jeedom/sonybravia/sonybravia_"+tmpmac+".pid"
jeedom_utils.write_pid(str(globals.pidfile))
globals.JEEDOM_COM = jeedom_com(apikey = globals.apikey,url = globals.callback,cycle=globals.cycle)
if not globals.JEEDOM_COM.test():
	logging.error('GLOBAL------Network communication issues. Please fix your Jeedom network configuration.')
	shutdown()
try:
	jeedom_socket = jeedom_socket(port=globals.socketport,address=globals.sockethost)
	listen()
except Exception,e:
	logging.error('Fatal error : '+str(e))
	shutdown()
