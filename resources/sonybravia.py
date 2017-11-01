#!/usr/bin/env python3
#
#   Sony Bravia - Domoticz Python plugin
#   G3rard
#
#   With thanks to Frank Fesevur for localtest
#
try:
    import Domoticz
except ImportError:
    import fakeDomoticz as Domoticz

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
ip = '192.168.1.36'
psk = 'sony'
mac = '90:CD:B6:41:F5:2F'
apikey = ''
jeedomadress = '192.168.1.2'

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
		_RazCalcul = 0
		_Separateur = "&"
		_SendData = ""
		def target():
			self.process = None
			#logger.debug("Thread started, timeout = " + str(timeout)+", command : "+str(self.cmd))
			self.process = subprocess.Popen(self.cmd + _SendData, shell=True)
			#print(self.cmd)
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
				#print('Status TV:', tvstatus)
			except KeyError:
				print('TV not found')
				sys.exit()
			
			if tvstatus == 'active':
			#print(json.dumps(test, indent=2))
				tvinfo = self._braviainstance.get_system_info()
				#print('TV model:', tvinfo['model'])
				Donnees["model"] = tvinfo['model']
				vol = self._braviainstance.get_volume_info()
				Donnees["volume"] = str(vol['volume'])
				#print('Volume:', vol['volume'])
				tvPlaying = self._braviainstance.get_playing_info()
				#print(self._braviainstance.get_playing_info())
				if not tvPlaying:
					#print("Netflix")
					Donnees["source"] = "Netflix"
				else:
					if(tvPlaying['source'] == "tv:analog"):
						Donnees["source"] = ("TV").upper()
						Donnees["chaine"] = tvPlaying['dispNum']
						Donnees["program"] = tvPlaying['title']
					else:
						Donnees["source"] = ((tvPlaying['source'])[-4:]).upper() + (tvPlaying['uri'])[-1:]
			#else:
				#print('TV status:', tvstatus) #status is standby net na het uitzetten, daarna niet meer bereikbaar
			self.cmd = "curl -L -s -G --max-time 15 " + self._jeedomadress + " -d 'apikey=" + self._apikey + "&mac=" + self._macadress
			#self.cmd = "curl -L -s -G --max-time 15 " + self._jeedomadress + " -d 'apikey=" + self._apikey + "&mac=" + self._macadress + "&model=" + tvinfo['model'] + "&status=" + tvstatus + "&vol=" + vol + "'"
			#self.cmd = "curl -L -s -G --max-time 15 " + self._jeedomadress +"/plugins/sonybravia/core/php/jeesonybravia.php -d 'apikey=" + self._apikey + "&status=" + tvstatus + "'"
			#cmd = 'nice -n 19 timeout 15 /usr/bin/php /var/www/html/plugins/sonybravia/core/class/../php/jeesonybravia.php api=' + self._apikey + " status=" + tvstatus
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
		#self._log.info("[exit_handler]")


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