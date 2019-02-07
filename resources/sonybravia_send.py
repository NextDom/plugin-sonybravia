#!/usr/bin/env python3
#
#
import os
from braviarc import BraviaRC
from optparse import OptionParser
from time import sleep
import sys

### Enter the IP address, PSK and MAC address of the TV below
ip = ''
psk = ''
mac = ''
command_type = ''
command_param = ''
###

usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-t", "--tvip", dest="ip", help="IP de la tv")
parser.add_option("-m", "--mac", dest="mac", help="Mac de la tv")
parser.add_option("-s", "--psk", dest="psk", help="Cle")
parser.add_option("-c", "--command", dest="command_type", help="commande")
parser.add_option("-p", "--commandparam", dest="command_param", help="parametres", default="1")
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
if options.command_type:
	try:
		command_type = options.command_type
	except:
		print('Erreur de commande')
if options.command_param:
	try:
		command_param = options.command_param
	except:
		print('Erreur de parametres')

_braviainstance = BraviaRC(ip, None, mac)
_braviainstance.connect(psk, 'Jeedom', 'Jeedom')

try:
	if command_type == 'turn_on':
		_braviainstance.turn_on()
	if command_type == 'turn_off':
		_braviainstance.turn_off()
	if command_type == 'select_source':
		_braviainstance.select_source(command_param)
	if command_type == 'set_volume':
		_braviainstance.set_volume_level(command_param)
	if command_type == 'start_app':
		_braviainstance.start_app(command_param)
	if command_type == 'volume_up':
		_braviainstance.volume_up()
	if command_type == 'volume_down':
		_braviainstance.volume_down()
	if command_type == 'mute_volume':
		_braviainstance.mute_volume(command_param)
	if command_type == 'play_content':
		_braviainstance.play_content(command_param)
	if command_type == 'media_play':
		_braviainstance.media_play()
	if command_type == 'media_pause':
		_braviainstance.media_pause()
	if command_type == 'media_previous_track':
		_braviainstance.media_previous_track()
	if command_type == 'media_next_track':
		_braviainstance.media_next_track()
	if command_type == 'start_app':
		_braviainstance.start_app(command_param)
	if command_type == 'ircc':
		cmdlist=command_param.split(";")
		for cmdircc in cmdlist :
			_braviainstance.send_req_ircc(cmdircc)
			sleep(0.25)
	sys.exit()
except KeyError:
    print('TV not found')
    sys.exit()