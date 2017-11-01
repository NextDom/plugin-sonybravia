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
try {
	require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
	include_file('core', 'authentification', 'php');
	if (!isConnect('admin')) {
		throw new Exception('401 Unauthorized');
	}
	ajax::init();

	if (init('action') == 'startdeamon') {
		sonybravia::tv_deamon_start(init('ip'), init('mac'), init('psk'));
		ajax::success();
	}
	
	if (init('action') == 'stopdeamon') {
		sonybravia::tv_deamon_stop(init('mac'));
		ajax::success();
	}
	
	if (init('action') == 'deamon_info') {
		$return = array();
		$resultat = sonybravia::tv_deamon_info(init('mac'));
		ajax::success($return['result'] = $resultat);
	}
	
	throw new Exception('Aucune methode correspondante');
	/*     * *********Catch exeption*************** */
} catch (Exception $e) {
	ajax::error(displayExeption($e), $e->getCode());
}
?>