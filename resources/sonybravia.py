#!/usr/bin/env python3
#
#
import os
from bravia import BraviaRC
import sys
import time
import threading
from optparse import OptionParser
from datetime import datetime
import signal
import subprocess

### Enter the IP address, PSK and MAC address of the TV below
ip = ''
psk = ''
mac = ''
apikey = ''
jeedomadress = ''

class SonyBravia:
	""" Fetch teleinformation datas and call user callback
	each time all data are collected
	"""
 
	def __init__(self, ipadress, macadress, psk, apikey, jeedomadress):
		self._ipadress = ipadress
		self._macadress = macadress
		self._psk = psk
		self._apikey = apikey
		self._jeedomadress = jeedomadress
		self._braviainstance = BraviaRC(self._ipadress, self._psk, self._macadress)

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
			#logger.debug("Thread started, timeout = " + str(timeout)+", command : "+str(self.cmd))
			self.process = subprocess.Popen(self.cmd + _SendData, shell=True)
			#print(self.cmd + _SendData)
			self.process.communicate()
			#logger.debug("Return code: " + str(self.process.returncode))
			#logger.debug("Thread finished")
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
			for cle, valeur in Sources.items():
				_tmp += cle.replace(' ' , '%20')
				_tmp += "|"
			#print (_tmp)
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
									Donnees["debut_p"], Donnees["fin_p"], Donnees["pourcent_p"] = self._braviainstance.playing_time(tvPlaying['startDateTime'],tvPlaying['durationSec'])
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
			self.cmd = "curl -L -s -G --max-time 15 " + self._jeedomadress + " -d 'apikey=" + self._apikey + "&mac=" + self._macadress
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
					thread = threading.Thread(target=target)
					self.timer = threading.Timer(int(5), timer_callback)
					self.timer.start()
					thread.start()
				except Exception:
					errorCom = "Connection error"
			time.sleep(2)

	def exit_handler(self, *args):
		self.terminate()


if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("-t", "--tvip", dest="ip", help="IP de la tv")
	parser.add_option("-m", "--mac", dest="mac", help="IP de la tv")
	parser.add_option("-s", "--psk", dest="psk", help="Cle")
	parser.add_option("-k", "--apikey", dest="apikey", help="IP de la tv")
	parser.add_option("-a", "--jeedomadress", dest="jeedomadress", help="IP de la tv")
	(options, args) = parser.parse_args()
	if options.ip:
		try:
			ip = options.ip
		except:
			print('Erreur d ip de la tv')
	if options.mac:
		try:
			mac = options.mac
		except:
			print('Erreur mac de la tv')
	if options.psk:
		try:
			psk = options.psk
		except:
			print('Erreur psk de la tv')
	if options.apikey:
		try:
			apikey = options.apikey
		except:
			print('Erreur apikey de jeedom')
	if options.jeedomadress:
		try:
			jeedomadress = options.jeedomadress
		except:
			print('Erreur adresse de jeedom')
	pid = str(os.getpid())
	tmpmac = mac.replace(":","")
	file = open("/tmp/jeedom/sonybravia/sonybravia_"+tmpmac+".pid", "w")
	file.write("%s\n" % pid) 
	file.close()
	sonybravia = SonyBravia(ip, mac, psk, apikey, jeedomadress)
	signal.signal(signal.SIGTERM, SonyBravia.exit_handler)
	sonybravia.run()
	sys.exit()
