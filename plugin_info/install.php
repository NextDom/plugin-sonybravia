<?php

/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';

function sonybravia_install() {
	if (jeedom::isCapable('sudo')) {
		exec(system::getCmdSudo() . ' chmod a+x ' . dirname(__FILE__) . '/../resources/install_apt.sh ' .' 2>&1 &');
	}
	else{
		message::add('sonybravia', 'Erreur : Veuillez donner les droits sudo à Jeedom', null, null);
	}
}

function sonybravia_update() {
    $coreVersion = '1.0.0';
    if (!file_exists(dirname(__FILE__) . '/info.json')) {
        log::add('sonybravia','warning','Pas de fichier info.json');
        goto step2;
    }
    $data = json_decode(file_get_contents(dirname(__FILE__) . '/info.json'), true);
    if (!is_array($data)) {
        log::add('sonybravia','warning','Impossible de décoder le fichier info.json');
        goto step2;
    }
    try {
        $coreVersion = $data['pluginVersion'];
    } catch (\Exception $e) {
        log::add('sonybravia','warning','Pas de version de plugin');
    }
    step2:
    log::add('sonybravia','info','*******************************************************');
    log::add('sonybravia','info','*********** Mise à jour du plugin sonybravia **********');
    log::add('sonybravia','info','*******************************************************');
    log::add('sonybravia','info','**        Core version    : '. $coreVersion. '                    **');
    log::add('sonybravia','info','*******************************************************');
	message::add('sonybravia', 'Mise à jour en cours...', null, null);
	if (jeedom::isCapable('sudo')) {
		exec(system::getCmdSudo() . ' chmod a+x ' . dirname(__FILE__) . '/../resources/install_apt.sh ' .' 2>&1 &');
		exec(system::getCmdSudo() . ' chmod a+x ' . dirname(__FILE__) . '/../resources/install_dependancy.sh ' .' 2>&1 &');
	}
	else{
		message::add('sonybravia', 'Erreur : Veuillez donner les droits sudo à Jeedom', null, null);
	}
	message::removeAll('sonybravia');
    message::add('sonybravia', 'Mise à jour terminée, vous êtes en version ' . $coreVersion . '.', null, null);
}

function sonybravia_remove() {

}

?>
