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
import json
from optparse import OptionParser
from threading import Timer
import _thread as thread
try:
	from jeedom.jeedom import *
except ImportError as ex:
	print("Error: importing module from jeedom folder")
	print(ex)
	sys.exit(1)

try:
    import queue
except ImportError:
	import Queue as queue

class SonyBravia:
	import globals
	def __init__(self):
		logging.debug("SONYBRAVIA------INIT CONNECTION")
		if(globals.cookie == '1') or (globals.cookie == 'true'):
			from braviarc import BraviaRC
			logging.debug("SONYBRAVIA------COOKIE MODE")
			globals.SONYBRAVIA_COM = BraviaRC(globals.tvip, globals.mac)
			if globals.SONYBRAVIA_COM.connect(globals.psk, 'Jeedom', 'Jeedom') == False:
				print ("SONYBRAVIA------PAS D AUTHENTIFICATION RECUPERATION DU PIN")
				sys.exit()
		else:
			from bravia import BraviaRC
			logging.debug("SONYBRAVIA------PSK MODE")
			globals.SONYBRAVIA_COM = BraviaRC(globals.tvip, globals.psk, globals.mac)

	def run(self):
		logging.debug("SONYBRAVIA------RUN")
		Donnees = {}
		_Donnees = {}
		_RAZ = datetime.now()
		Sources = {}
		Apps = {}
		_RazCalcul = 0
		_Separateur = "&"
		tvstatus = ""
		try:
			Sources = globals.SONYBRAVIA_COM.load_source_list()
			Apps = globals.SONYBRAVIA_COM.load_app_list()
			_tmp = ""
			for cle, valeur in Sources.items():
				_tmp += cle.replace(' ' , '\x20')
				_tmp += "|"
			Donnees["sources"] = _tmp
			_tmp = ""
			for cle, valeur in Apps.items():
				_tmp += cle.replace(' ' , '\x20') + "|"
				#_tmp = _tmp.replace('&', '%26')
				#_tmp = _tmp.replace('\'', '%27')
			Donnees["apps"] = _tmp
		except Exception:
					errorCom = "Connection error"
					logging.error(errorCom)
		while(1):
			_RazCalcul = datetime.now() - _RAZ
			if(_RazCalcul.seconds > 8):
				_RAZ = datetime.now()
				del Donnees
				del _Donnees
				Donnees = {}
				_Donnees = {}
			try:
				tvstatus = globals.SONYBRAVIA_COM.get_power_status()
				logging.debug('SONYBRAVIA------TVSTATUS : ' + tvstatus)
				Donnees["status"] = tvstatus
			except KeyError:
				print('TV not found')
				sys.exit()
			if tvstatus == 'active':
				try:
					tvinfo = globals.SONYBRAVIA_COM.get_system_info()
					logging.debug('SONYBRAVIA------TVINFO : ' + tvinfo['name'] + ' ' + tvinfo['model'])
					Donnees["model"] = tvinfo['model']
				except:
					print('Model not found')
				try:
					vol = globals.SONYBRAVIA_COM.get_volume_info()
					Donnees["volume"] = str(vol['volume'])
				except:
					print('Volume not found')
				try:
					tvPlaying = globals.SONYBRAVIA_COM.get_playing_info()
					#logging.debug('SONYBRAVIA------PLAYINGINFO : ' + tvPlaying)
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
								Donnees["chaine"] = tvPlaying['dispNum'].replace('\'','%27').replace(' ','\x20').replace('é','\xe9')
						except:
							print('num chaine not found')
						try:
							if tvPlaying['programTitle'] is not None :
								Donnees["program"] = tvPlaying['programTitle'].replace(' ','\x20').replace('é','\xe9').replace('\'','%27')
						except:
							print('program info not found')
						try:
							if tvPlaying['title'] is not None :
								Donnees["nom_chaine"] = tvPlaying['title'].replace(' ','\x20').replace('\'','%27').replace('é','\xe9')
						except:
							print('nom chaine not found')
						try:
							if tvPlaying['startDateTime'] is not None :
								if tvPlaying['startDateTime'] != '':
									Donnees["debut"] = tvPlaying['startDateTime']
									_tmp = globals.SONYBRAVIA_COM.playing_time(tvPlaying['startDateTime'],tvPlaying['durationSec'])
									Donnees["debut_p"] = _tmp[0]
									Donnees["fin_p"] = _tmp[1]
									Donnees["pourcent_p"] = _tmp[2]
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
			_SendData = {}
			PENDING_CHANGES = False
			for cle, valeur in Donnees.items():
				if(cle in _Donnees):
					if (Donnees[cle] != _Donnees[cle]):
						_SendData[cle] = valeur
						_Donnees[cle] = valeur
						PENDING_CHANGES = True
				else:
					_SendData[cle] = valeur
					_Donnees[cle] = valeur
					PENDING_CHANGES = True
			try:
				if PENDING_CHANGES :
					_SendData["device"] = globals.mac
					globals.JEEDOM_COM.add_changes('device::'+globals.mac,_SendData)
			except Exception:
				errorCom = "Connection error"
				logging.error(errorCom)
			time.sleep(globals.sommeil)

	def exit_handler(self, *args):
		logging.debug("terminate")
		#self.terminate()

# -------------------------------
# main method to manage actions
# -------------------------------
def action_handler(message):
	try:
		if message['device'] == globals.mac:
			if message['command'] == 'turn_on':
				globals.SONYBRAVIA_COM.turn_on()
			if message['command'] == 'turn_off':
				globals.SONYBRAVIA_COM.turn_off()
			if message['command'] == 'select_source':
				globals.SONYBRAVIA_COM.select_source(message['commandparam'])
			if message['command'] == 'set_volume':
				globals.SONYBRAVIA_COM.set_volume_level(message['commandparam'])
			if message['command'] == 'start_app':
				globals.SONYBRAVIA_COM.start_app(message['commandparam'])
			if message['command'] == 'volume_up':
				globals.SONYBRAVIA_COM.volume_up()
			if message['command'] == 'volume_down':
				globals.SONYBRAVIA_COM.volume_down()
			if message['command'] == 'mute_volume':
				globals.SONYBRAVIA_COM.mute_volume(message['commandparam'])
			if message['command'] == 'play_content':
				globals.SONYBRAVIA_COM.play_content(message['commandparam'])
			if message['command'] == 'media_play':
				globals.SONYBRAVIA_COM.media_play()
			if message['command'] == 'media_pause':
				globals.SONYBRAVIA_COM.media_pause()
			if message['command'] == 'media_previous_track':
				globals.SONYBRAVIA_COM.media_previous_track()
			if message['command'] == 'media_next_track':
				globals.SONYBRAVIA_COM.media_next_track()
			if message['command'] == 'start_app':
				globals.SONYBRAVIA_COM.start_app(message['commandparam'])
			if message['command'] == 'ircc':
				cmdlist=message['commandparam'].split(";")
				for cmdircc in cmdlist :
					globals.SONYBRAVIA_COM.send_req_ircc(cmdircc)
					time.sleep(0.25)
	except KeyError:
		print('TV not found')


def read_socket(cycle):
	while True :
		try:
			global JEEDOM_SOCKET_MESSAGE
			if not JEEDOM_SOCKET_MESSAGE.empty():
				logging.debug("SOCKET-READ------Message received in socket JEEDOM_SOCKET_MESSAGE")
				message = json.loads(JEEDOM_SOCKET_MESSAGE.get())
				if message['apikey'] != globals.apikey:
					logging.error("SOCKET-READ------Invalid apikey from socket : " + str(message))
					return
				logging.info('SOCKET-READ------Received command from jeedom : '+str(message['cmd']))
				if message['cmd'] == 'action':
					logging.debug('SOCKET-READ------Attempt an action on a device')
					thread.start_new_thread( action_handler, (message,))
					logging.debug('SOCKET-READ------Action Thread Launched')
				elif message['cmd'] == 'logdebug':
					logging.info('SOCKET-READ------Passage du demon en mode debug force')
					log = logging.getLogger()
					for hdlr in log.handlers[:]:
						log.removeHandler(hdlr)
					jeedom_utils.set_log_level('debug')
					logging.debug('SOCKET-READ------<----- La preuve ;)')
				elif message['cmd'] == 'lognormal':
					logging.info('SOCKET-READ------Passage du demon en mode de log normal')
					log = logging.getLogger()
					for hdlr in log.handlers[:]:
						log.removeHandler(hdlr)
					jeedom_utils.set_log_level('error')
		except Exception as e:
			logging.error("SOCKET-READ------Exception on socket : %s" % str(e))
			logging.debug(traceback.format_exc())
		time.sleep(cycle)

def log_starting(cycle):
	time.sleep(120)
	logging.info('GLOBAL------Passage des logs en normal')
	log = logging.getLogger()
	for hdlr in log.handlers[:]:
		log.removeHandler(hdlr)
	jeedom_utils.set_log_level('error')

def listen():
	globals.PENDING_ACTION=False
	jeedom_socket.open()
	logging.info("GLOBAL------Start listening...")
	globals.SONYBRAVIA = SonyBravia()
	logging.info("GLOBAL------Preparing SonyBravia...")
	#globals.JEEDOM_COM.send_change_immediate({'learn_mode' : 0,'source' : globals.daemonname});
	thread.start_new_thread( read_socket, (globals.cycle,))
	logging.debug('GLOBAL------Read Socket Thread Launched')
	logging.info('GLOBAL------Logs en debug pour 2 minutes, passage en info ensuite.')
	while 1:
		try:
			thread.start_new_thread( log_starting, (globals.cycle,))
			globals.SONYBRAVIA.run()
		except Exception as e:
			shutdown()

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	log = logging.getLogger()
	for hdlr in log.handlers[:]:
		log.removeHandler(hdlr)
	jeedom_utils.set_log_level('debug')
	logging.info("GLOBAL------Shutdown")
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
globals.cycle = 2;

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
parser.add_argument("--cookie", help="Authentification Method", type=str)
parser.add_argument("--sommeil", help="Waiting time between check", type=str)
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
if args.cookie:
	globals.cookie = args.cookie
if args.sommeil:
	globals.sommeil = float(args.sommeil)

globals.socketport = int(globals.socketport)
globals.cycle = float(globals.cycle)

jeedom_utils.set_log_level(globals.log_level)
logging.info('GLOBAL------Start sonyd')
logging.info('GLOBAL------Log level : '+str(globals.log_level))
logging.info('GLOBAL------Socket port : '+str(globals.socketport))
logging.info('GLOBAL------Socket host : '+str(globals.sockethost))
logging.info('GLOBAL------Callback : '+str(globals.callback))
logging.info('GLOBAL------Sommeil : '+str(globals.sommeil))
logging.info('GLOBAL------Apikey : '+str(globals.apikey))
logging.info('GLOBAL------Cookie : '+str(globals.cookie))
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
