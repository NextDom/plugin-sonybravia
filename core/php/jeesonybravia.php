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
header('Content-type: application/json');
require_once __DIR__ . "/../../../../core/php/core.inc.php";

if (!jeedom::apiAccess(init('apikey'), 'sonybravia')) {
    echo __('Clef API non valide, vous n\'êtes pas autorisé à effectuer cette action (sonybravia)', __FILE__);
    die();
}

if (init('test') != '') {
	echo 'OK';
	die();
}

$result = json_decode(file_get_contents("php://input"), true);
if (!is_array($result)) {
	die();
}

$var_to_log = '';

if (isset($result['device'])) {
    foreach ($result['device'] as $key => $data) {
            log::add('sonybravia','debug','This is a message from sonybravia program ' . $key);
    		$eqlogic = sonybravia::byLogicalId($data['device'], 'sonybravia');
    		if (is_object($eqlogic)) {
                $flattenResults = array_flatten($data);
                foreach ($eqlogic->getCmd('info') as $cmd) {
                    $logicalId = $cmd->getLogicalId();
                    if ( isset($flattenResults[$logicalId]) ) {
                        $cmd->event($flattenResults[$logicalId]);
                    }
                }
            }
            log::add('sonybravia','debug',$var_to_log);
        }
    }

function array_flatten($array) {
    global $var_to_log;
    $return = array();
    foreach ($array as $key => $value) {
        $var_to_log = $var_to_log . $key . '=' . $value . '|';
        if (is_array($value))
            $return = array_merge($return, array_flatten($value));
        else
            $return[$key] = $value;
    }
    return $return;
}
