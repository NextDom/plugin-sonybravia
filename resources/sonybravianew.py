#!/usr/bin/env python3
#
#
import os
import sys
import time
import threading
import logging
import argparse
import datetime
import signal
import subprocess
import signal
import globals
from optparse import OptionParser
from braviarc import BraviaRC
from threading import Timer
import thread
try:
	from jeedom.jeedom import *
except ImportError:
	print "Error: importing module from jeedom folder"
sys.exit(1)

try:
    import queue
except ImportError:
import Queue as queue

### Enter the IP address, PSK and MAC address of the TV below
ip = ''
psk = ''
mac = ''
apikey = ''
jeedomadress = ''

class SonyBravia:
	import globals
	def __init__(self):
		self._braviainstance = BraviaRC(globals.tvip, globals.psk, globals.mac)

	
	def run(self):
		Donnees = {}
		_Donnees = {}
		_RAZ = datetime.now()
		Sources = {}
		Apps = {}
		_RazCalcul = 0
		_Separateur = "&"
		_SendData = ""
		def target():
			self.process = None
			self.process = subprocess.Popen(self.cmd + _SendData, shell=True)
			self.process.communicate()
			self.timer.cancel()

		def timer_callback():
			#logger.debug("Thread timeout, terminate it")
			if self.process.poll() is None:
				try:
					self.process.kill()
				except OSError as error:
					#logger.error("Error: %s " % error)
					self._log.error("Error: %s " % error)
				self._log.warning("Thread terminated")
			else:
				self._log.warning("Thread not alive")
		tvstatus = ""
		try:
			Sources = self._braviainstance.load_source_list()
			Apps = self._braviainstance.load_app_list()
			_tmp = ""
			for cle, valeur in Sources.items():
				_tmp += cle.replace(' ' , '%20')
				_tmp += "|"
			Donnees["sources"] = _tmp
			_tmp = ""
			for cle, valeur in Apps.items():
				_tmp += cle.replace(' ' , '%20') + "|"
				_tmp = _tmp.replace('&', '%26')
				_tmp = _tmp.replace('\'', '%27')
			Donnees["apps"] = _tmp
		except Exception:
					errorCom = "Connection error"
		while(1):
			_RazCalcul = datetime.now() - _RAZ
			if(_RazCalcul.seconds > 8):
				_RAZ = datetime.now()
				del Donnees
				del _Donnees
				Donnees = {}
				_Donnees = {}
			_SendData = ""
			try:
				tvstatus = self._braviainstance.get_power_status()
				Donnees["status"] = tvstatus
			except KeyError:
				print('TV not found')
				sys.exit()
			if tvstatus == 'active':
				try:
					tvinfo = self._braviainstance.get_system_info()
					Donnees["model"] = tvinfo['model']
				except:
					print('Model not found')
				try:
					vol = self._braviainstance.get_volume_info()
					Donnees["volume"] = str(vol['volume'])
				except:
					print('Volume not found')
				try:
					tvPlaying = self._braviainstance.get_playing_info()
					#print (tvPlaying)
					if not tvPlaying:
						Donnees["source"] = "Application"
						Donnees["program"] = ""
						Donnees["nom_chaine"] = ""
						Donnees["debut"] = ""
						Donnees["debut_p"] = ''
						Donnees["fin_p"] = ''
						Donnees["pourcent_p"] = '0'
						Donnees["duree"] = ""
						Donnees["chaine"] = ""
					else:
						Donnees["source"] = ((tvPlaying['source'])[-4:]).upper() + (tvPlaying['uri'])[-1:]
						try:
							if tvPlaying['dispNum'] is not None :
								Donnees["chaine"] = tvPlaying['dispNum'].replace('\'','%27').replace(' ','%20').replace('é','%C3%A9')
						except:
							print('num chaine not found')
						try:
							if tvPlaying['programTitle'] is not None :
								Donnees["program"] = tvPlaying['programTitle'].replace(' ','%20').replace('é','%C3%A9').replace('\'','%27')
						except:
							print('program info not found')
						try:
							if tvPlaying['title'] is not None :
								Donnees["nom_chaine"] = tvPlaying['title'].replace(' ','%20').replace('\'','%27').replace('é','%C3%A9')
						except:
							print('nom chaine not found')
						try:
							if tvPlaying['startDateTime'] is not None :
								if tvPlaying['startDateTime'] != '':
									Donnees["debut"] = tvPlaying['startDateTime']
									_tmp = self._braviainstance.playing_time(tvPlaying['startDateTime'],tvPlaying['durationSec'])
									Donnees["debut_p"], Donnees["pourcent_p"],Donnees["fin_p"] = _tmp['start_time'], str(_tmp['media_position_perc']), _tmp['end_time']
								else:
									Donnees["debut_p"] = ''
									Donnees["fin_p"] = ''
									Donnees["pourcent_p"] = '0'
						except:
							print('start date not found')
						try:
							if tvPlaying['durationSec'] is not None :
								if tvPlaying['durationSec'] != '':
									Donnees["duree"] = str(tvPlaying['durationSec'])
								else:
									Donnees["duree"] = '0'
						except:
							print('duration not found')
				except:
					print('Playing Info not found')
			else:
				try:
					Donnees["source"] = ""
					Donnees["program"] = ""
					Donnees["nom_chaine"] = ""
					Donnees["debut"] = ""
					Donnees["debut_p"] = ''
					Donnees["fin_p"] = ''
					Donnees["pourcent_p"] = '0'
					Donnees["duree"] = ""
					Donnees["chaine"] = ""
					Donnees["volume"] = ""
				except:
					print('Cannot reset Playing Info')
			#self.cmd = "curl -L -s -G --max-time 15 " + self._jeedomadress + " -d 'apikey=" + self._apikey + "&mac=" + self._macadress
			for cle, valeur in Donnees.items():
				if(cle in _Donnees):
					if (Donnees[cle] != _Donnees[cle]):
						_SendData += _Separateur + cle +'='+ valeur
						_Donnees[cle] = valeur
				else:
					_SendData += _Separateur + cle +'='+ valeur
					_Donnees[cle] = valeur
			_SendData += "'"
			if _SendData != "'":
				try:
					globals.JEEDOM_COM.add_changes('devices::'_SendData)
				except Exception:
					errorCom = "Connection error"
			time.sleep(2)

	def exit_handler(self, *args):
		self.terminate()

def listen():
	globals.PENDING_ACTION=False
	jeedom_socket.open()
	logging.info("GLOBAL------Start listening...")
	globals.SONYBRAVIA = SonyBravia()
	logging.info("GLOBAL------Preparing SonyBravia...")
	#globals.JEEDOM_COM.send_change_immediate({'learn_mode' : 0,'source' : globals.daemonname});
	thread.start_new_thread( read_socket, ('socket',))
	logging.debug('GLOBAL------Read Socket Thread Launched')
	try:
		while 1:
			try:
				globals.SONYBRAVIA.run()
			except Exception, e:
				shutdown()

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("GLOBAL------Shutdown")
	signal.signal(signal.SIGTERM, globals.SONYBRAVIA.exit_handler)
	logging.debug("Shutdown")
	logging.debug("Removing PID file " + str(globals.pidfile))
	try:
		os.remove(globals.pidfile)
	except:
		pass
	try:
		jeedom_socket.close()
	except:
		pass
	logging.debug("Exit 0")
	sys.stdout.flush()
	os._exit(0)

globals.log_level = "error"
globals.socketport = 55052
globals.sockethost = '127.0.0.1'
globals.apikey = ''
globals.callback = ''
globals.cycle = 0.05;

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
jeedom_socket = jeedom_socket(port=globals.socketport,address=globals.sockethost)
listen()
sys.exit()