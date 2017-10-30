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

	/*$cron = cron::byClassAndFunction('sony-bravia', 'cron');
    if (!is_object($cron)) {
        $cron = new cron();
        $cron->setClass('sony-bravia');
        $cron->setFunction('CalculateOtherStats');
        $cron->setEnable(1);
        $cron->setDeamon(0);
        $cron->setSchedule('05 00 * * *');
        $cron->save();
    }*/
}

function sonybravia_update() {
	message::add('sonybravia', 'Mise à jour en cours...', null, null);

	/*$cron = cron::byClassAndFunction('sony-bravia', 'CalculateOtherStats');
    if (!is_object($cron)) {
        $cron = new cron();
        $cron->setClass('sony-bravia');
        $cron->setFunction('cron');
        $cron->setEnable(1);
        $cron->setDeamon(0);
        $cron->setSchedule('05 00 * * *');
        $cron->save();
    }
	else{
		$cron->setSchedule('05 00 * * *');
        $cron->save();
	}
    $cron->stop();
	*/
	message::removeAll('sony-bravia');		
	message::add('sonybravia', 'Mise à jour terminée', null, null);
}

function sonybravia_remove() {

	/*$cron = cron::byClassAndFunction('sony-bravia', 'CalculateOtherStats');
    if (is_object($cron)) {
        $cron->remove();
    }*/
}

?>
