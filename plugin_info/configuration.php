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
include_file('core', 'authentification', 'php');
if (!isConnect()) {
    include_file('desktop', '404', 'php');
    die();
}

$core_version = '1.1.1';
if (!file_exists(dirname(__FILE__) . '/info.json')) {
    log::add('sonybravia','warning','Pas de fichier info.json');
}
$data = json_decode(file_get_contents(dirname(__FILE__) . '/info.json'), true);
if (!is_array($data)) {
    log::add('sonybravia','warning','Impossible de décoder le fichier info.json');
}
try {
    $core_version = $data['pluginVersion'];
} catch (\Exception $e) {
    log::add('sonybravia','warning','Impossible de récupérer la version.');
}

?>

<form class="form-horizontal">
    <fieldset>
    <legend><i class="icon loisir-pacman1"></i> {{Version}}</legend>
        <div class="form-group">
            <label class="col-lg-4 control-label">Core <sup><i class="fa fa-question-circle tooltips" title="{{C'est la version du moteur du plugin}}" style="font-size : 1em;color:grey;"></i></sup></label>
            <span style="top:6px;" class="col-lg-4"><?php echo $core_version; ?></span>
        </div>
    </fieldset>
    <fieldset>
    <legend><i class="icon loisir-darth"></i>&nbsp; {{Démon}}</legend>
    <div class="form-group">
	    <label class="col-lg-4 control-label">{{Port socket interne (modification dangereuse)}}</label>
	    <div class="col-lg-2">
	        <input class="configKey form-control" data-l1key="socketport" placeholder="{{55052}}" />
	    </div>
    </div>
    <div class="form-group">
			<label class="col-sm-4 control-label">{{Cycle (s)}}</label>
			<div class="col-sm-2">
				<input class="configKey form-control" data-l1key="cycle" placeholder="{{0.3}}"/>
			</div>
	</div>
    <div class="form-group">
			<label class="col-sm-4 control-label">{{Sommeil (s)}}</label>
			<div class="col-sm-2">
				<input class="configKey form-control" data-l1key="sommeil" placeholder="{{1}}"/>
			</div>
	</div>
    <div class="form-group">
        <label class="col-sm-4 control-label"></label>
        <div class="col-sm-4">
    		<a class="btn btn-warning changeLogLive" data-log="logdebug"><i class="fa fa-cogs"></i> {{Mode debug forcé temporaire}}</a>
    		<a class="btn btn-success changeLogLive" data-log="lognormal"><i class="fa fa-paperclip"></i> {{Remettre niveau de log local}}</a>
    	</div>
    </div>
</form>
<script>
 $('.changeLogLive').on('click', function () {
	 $.ajax({// fonction permettant de faire de l'ajax
            type: "POST", // methode de transmission des données au fichier php
            url: "plugins/sonybravia/core/ajax/sonybravia.ajax.php", // url du fichier php
            data: {
                action: "changeLogLive",
				level : $(this).attr('data-log')
            },
            dataType: 'json',
            error: function (request, status, error) {
                handleAjaxError(request, status, error);
            },
            success: function (data) { // si l'appel a bien fonctionné
                if (data.state != 'ok') {
                    $('#div_alert').showAlert({message: data.result, level: 'danger'});
                    return;
                }
                $('#div_alert').showAlert({message: '{{Réussie}}', level: 'success'});
            }
        });
});
</script>
