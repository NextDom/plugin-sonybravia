#!/usr/bin/env python3
#
#
import os
from braviarc import BraviaRC
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
		self._braviainstance = BraviaRC(self._ipadress, None, self._macadress)
		if self._braviainstance.connect(psk, 'Jeedom', 'Jeedom') == False:
			print ("Récupération du pin")
			sys.exit()

	def run(self):
		Donnees = {}
		_Donnees = {}
		Sources = {}
		Apps = {}
		_RAZ = datetime.now()
		_RAZ2 = datetime.now()
		_RazCalcul = 0
		_Separateur = "&"
		_tmp = ""
		_SendData = ""
		def target():
			self.process = None
			#print (self.cmd + _SendData)
			self.process = subprocess.Popen(self.cmd + _SendData, shell=True)
			self.process.communicate()
			self.timer.cancel()

		def timer_callback():
			if self.process.poll() is None:
				try:
					self.process.kill()
				except OSError as error:
					print ("Error: %s " % error)
				print("Thread terminated")
			else:
				print ("Thread not alive")
		tvstatus = ""
		while(1):
			_RazCalcul = datetime.now() - _RAZ
			_RazCalcul2 = datetime.now() - _RAZ2
			if(_RazCalcul.seconds > 8):
				_RAZ = datetime.now()
				del Donnees
				del _Donnees
				Donnees = {}
				_Donnees = {}
			_SendData = ""
			if(_RazCalcul2.seconds > 60):
				_RAZ2 = datetime.now()
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
						_tmp += cle.replace('\'' , '%27') + "|"
					_tmp = _tmp.replace('&', '%26')
					_tmp = _tmp.replace(' ', '%20')
					Donnees["apps"] = _tmp
				except Exception:
							errorCom = "Connection error"
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
						Donnees["debut_p"] = ""
						Donnees["fin_p"] = ''
						Donnees["pourcent_p"] = '0'
						Donnees["duree"] = ""
						Donnees["chaine"] = ""
					else:
						Donnees["source"] = ((tvPlaying['source'])[-4:]).upper() + (tvPlaying['uri'])[-1:]
						try:
							if tvPlaying['dispNum'] is not None :
								Donnees["chaine"] = tvPlaying['dispNum'].replace(' ','%20').replace('\'','%27').replace('é','%C3%A9')
						except:
							print('not found')
						try:
							if tvPlaying['programTitle'] is not None :
								Donnees["program"] = tvPlaying['programTitle'].replace(' ','%20').replace('é','%C3%A9').replace('\'','%27')
						except:
							print('program not found')
						try:
							if tvPlaying['title'] is not None :
								Donnees["nom_chaine"] = tvPlaying['title'].replace(' ','%20').replace('\'','%27').replace('é','%C3%A9')
						except:
							print('not found')
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
				except:
					errorCom = "Connection error"
			time.sleep(2)

	def exit_handler(self, *args):
		self.terminate()


if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("-t", "--tvip", dest="ip", help="IP de la tv")
	parser.add_option("-m", "--mac", dest="mac", help="Mac de la tv")
	parser.add_option("-s", "--psk", dest="psk", help="Cle")
	parser.add_option("-k", "--apikey", dest="apikey", help="Cle jeedom")
	parser.add_option("-a", "--jeedomadress", dest="jeedomadress", help="IP Jeedom")
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
