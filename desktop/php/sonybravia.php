<?php
if (!isConnect('admin')) {
    	throw new Exception('{{401 - Accès non autorisé}}');
}
$plugin = plugin::byId('sonybravia');
sendVarToJS('eqType', $plugin->getId());
$eqLogics = eqLogic::byType($plugin->getId());
?>

<div class="row row-overflow">
    <div class="col-lg-2 col-md-3 col-sm-4">
        <div class="bs-sidebar">
            <ul id="ul_eqLogic" class="nav nav-list bs-sidenav">
                <a class="btn btn-default eqLogicAction" style="width : 100%;margin-top : 5px;margin-bottom: 5px;" data-action="add"><i class="fa fa-plus-circle"></i> {{Ajouter un équipement}}</a>
                <li class="filter" style="margin-bottom: 5px;"><input class="filter form-control input-sm" placeholder="{{Rechercher}}" style="width: 100%"/></li>
                <?php
foreach ($eqLogics as $eqLogic) {
	$opacity = ($eqLogic->getIsEnable()) ? '' : jeedom::getConfiguration('eqLogic:style:noactive');
	echo '<li class="cursor li_eqLogic" data-eqLogic_id="' . $eqLogic->getId() . '" style="' . $opacity . '"><a>' . $eqLogic->getHumanName(true) . '</a></li>';
}
?>
           </ul>
       </div>
   </div>

   <div class="col-lg-10 col-md-9 col-sm-8 eqLogicThumbnailDisplay" style="border-left: solid 1px #EEE; padding-left: 25px;">
    <legend><i class="icon techno-tv"></i> {{Mes TV}}
    </legend>
    <div class="eqLogicThumbnailContainer">
      <div class="cursor eqLogicAction" data-action="add" style="text-align: center; background-color : #ffffff; height : 200px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >
            <i class="fa fa-plus-circle" style="font-size : 7em;color:#94ca02;"></i>
        <br>
        <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#94ca02">Ajouter</span>
    </div>
    <?php
foreach ($eqLogics as $eqLogic) {
	$opacity = ($eqLogic->getIsEnable()) ? '' : jeedom::getConfiguration('eqLogic:style:noactive');
	echo '<div class="eqLogicDisplayCard cursor" data-eqLogic_id="' . $eqLogic->getId() . '" style="text-align: center; background-color : #ffffff; height : 200px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;' . $opacity . '" >';
	echo '<img src="' . $plugin->getPathImgIcon() . '" height="105" width="95" />';
	echo "<br>";
	echo '<span style="font-size : 1.1em;position:relative; top : 15px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;">' . $eqLogic->getHumanName(true, true) . '</span>';
	echo '</div>';
}
?>
</div>
</div>

<div class="col-lg-10 col-md-9 col-sm-8 eqLogic" style="border-left: solid 1px #EEE; padding-left: 25px;display: none;">
   <a class="btn btn-success eqLogicAction pull-right" data-action="save"><i class="fa fa-check-circle"></i> {{Sauvegarder}}</a>
  <a class="btn btn-danger eqLogicAction pull-right" data-action="remove"><i class="fa fa-minus-circle"></i> {{Supprimer}}</a>
  <a class="btn btn-default eqLogicAction pull-right" data-action="configure"><i class="fa fa-cogs"></i> {{Configuration avancée}}</a>
  <!--<a class="btn btn-default eqLogicAction pull-right" data-action="copy"><i class="fa fa-files-o"></i> {{Dupliquer}}</a>-->
  <!--<a class="btn btn-default pull-right" id="bt_importEqLogic"><i class="fa fa-share"></i> {{Importer équipement}}</a>-->
  <ul class="nav nav-tabs" role="tablist">
    <li role="presentation"><a href="#" class="eqLogicAction" aria-controls="home" role="tab" data-toggle="tab" data-action="returnToThumbnailDisplay"><i class="fa fa-arrow-circle-left"></i></a></li>
    <li role="presentation" class="active"><a href="#eqlogictab" aria-controls="home" role="tab" data-toggle="tab"><i class="fa fa-tachometer"></i> {{Equipement}}</a></li>
    <li role="presentation"><a href="#commandtab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fa fa-list-alt"></i> {{Commandes}}</a></li>
  </ul>
  <div class="tab-content" style="height:calc(100% - 50px);overflow:auto;overflow-x: hidden;">
    <div role="tabpanel" class="tab-pane active" id="eqlogictab">
      <br/>
        <form class="form-horizontal">
            <fieldset>
                <div class="form-group">
                    <label class="col-sm-2 control-label">{{Nom de l'équipement SonyBravia}}</label>
                    <div class="col-sm-3">
                        <input type="text" class="eqLogicAttr form-control" data-l1key="id" style="display : none;" />
                        <input type="text" class="eqLogicAttr form-control" data-l1key="name" placeholder="{{Nom de l'équipement virtuel}}"/>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-2 control-label" >{{Objet parent}}</label>
                    <div class="col-sm-3">
                        <select class="form-control eqLogicAttr" data-l1key="object_id">
                            <option value="">{{Aucun}}</option>
                            <?php
foreach (object::all() as $object) {
	echo '<option value="' . $object->getId() . '">' . $object->getName() . '</option>';
}
?>
                       </select>
                   </div>
               </div>
               <div class="form-group">
                <label class="col-sm-2 control-label">{{Catégorie}}</label>
                <div class="col-sm-8">
                    <?php
foreach (jeedom::getConfiguration('eqLogic:category') as $key => $value) {
	echo '<label class="checkbox-inline">';
	echo '<input type="checkbox" class="eqLogicAttr" data-l1key="category" data-l2key="' . $key . '" />' . $value['name'];
	echo '</label>';
}
?>
               </div>
			</div>
			<div class="form-group">
				<label class="col-sm-2 control-label"></label>
				<div class="col-sm-9">
					<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isEnable" checked/>{{Activer}}</label>
					<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isVisible" checked/>{{Visible}}</label>
				</div>
			</div>
			<div class="form-group">
				<label class="col-sm-2 control-label">{{Adresse IP}}</label>
				<div class="col-sm-2">
					<input type="text" class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="ipadress" placeholder="{{192.168.1.1}}"/>
				</div>
			</div>
			<div class="form-group">
				<label class="col-sm-2 control-label">{{Adresse MAC}}</label>
				<div class="col-sm-2">
					<input type="text" class="eqLogicAttr form-control" data-l1key="logicalId" placeholder="{{00:00:00:00:00:00}}"/>
				</div>
			</div>
			<div class="form-group">
				<label class="col-sm-2 control-label">{{Clé TV}}</label>
				<div class="col-sm-2">
					<input type="text" class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="psk" placeholder="{{}}"/>
				</div>
                                
			</div>
			
			<div class="form-group">
				<label class="col-sm-2 control-label">{{Configuration}}</label>
				<div class="col-sm-8"><br/>
				1 - Activer l'accès distant sur votre TV : [Paramètres] => [Réseaux] => [Configuration Réseau domestique] => [Contrôle IP] => [On]<br/>
				2 - Activer l'accès par clé partagée : [Paramètres] => [Réseaux] => [Configuration Réseau domestique] => [Contrôle IP] => [Authentification] => [Normal et clé pré-partagée]<br/>
				3 - Choisir la clé et la renseigner ci-dessus : [Paramètres] => [Réseaux] => [Configuration Réseau domestique] => [Contrôle IP] => [Clé pré-partagée] => sony<br/>
				<br/>
				Renseigner les informations sur l'équipement puis sauvegarder.<br/>
                                
                                <a class="btn btn-default eqLogicAction" onclick="window.open('plugins/sonybravia/doc/images/config.png')"><i class="fa fa-question-circle"></i>{{ Plus d'infos}}</a>
				</div>
			</div>
                
                        <div class="form-group">
                            <label class="col-sm-2 control-label"></label>
                            <div style="margin-top:10px" class="col-sm-2">
                                Si ce mode ne fonctionne pas, passer au mode PIN : <br/>
                                <input type="checkbox" id="checkbox_psk" class="eqLogicAttr" data-l1key="configuration" data-l2key="pin" placeholder="{{}}"/> Mode PIN
                            </div>
                        </div>
			
			<div class="form-group">
				<label class="col-sm-2 control-label"></label>
				<!--<div class="col-sm-1">
					<span class="label deamoninfo" title="Cliquer pour mettre à jour" style="font-size:1em;position:relative;top:7px;"><i class="fa fa-refresh"></i> Etat</span>
				</div>-->
				<div class="col-sm-1">
					<a class="btn btn-success gettvpin"><i class="fa fa-cogs"></i> 1. {{Récupérer le PIN}}</a>
					<script>
					$('.gettvpin').on('click', function () {
						$.ajax({// fonction permettant de faire de l'ajax
							type: "POST", // methode de transmission des données au fichier php
							url: "plugins/sonybravia/core/ajax/sonybravia.ajax.php", // url du fichier php
							data: {
								action: "startdeamon_recuppin",
								ip : $( "input[data-l2key='ipadress']" ).value(),
								mac : $( "input[data-l1key='logicalId']" ).value(),
								psk : $( "input[data-l2key='psk']" ).value(),
                                                                cookie : 'true'
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
                                            bootbox.alert("Veuillez passer à l\'étape 2");
					});
					</script>
				</div>
                                <!--<div class="col-sm-1">
                                <a class="btn btn-success eqLogicAction pull-right" data-action="save"><i class="fa fa-check-circle"></i>{{Etape 3}}</a>
                                </div>-->
			</div>
			<div class="form-group">
				<label class="col-sm-2 control-label"></label>
                                 <div class="col-sm-1">
					<a class="btn btn-success startdeamontv"><i class="fa fa-cogs"></i>{{ 2. Confirmer le PIN}}</a>
					<script>
                                        $('.startdeamontv').on('click', function () {
                                            bootbox.prompt("{{Veuillez indiquer le code affiché sur la TV}}", function (result) {
                                                if(result != null){
                                                    $.ajax({// fonction permettant de faire de l'ajax
							type: "POST", // methode de transmission des données au fichier php
							url: "plugins/sonybravia/core/ajax/sonybravia.ajax.php", // url du fichier php
							data: {
								action: "startdeamon",
								ip : $( "input[data-l2key='ipadress']" ).value(),
								mac : $( "input[data-l1key='logicalId']" ).value(),
								psk : result,
                                                                cookie : 'true'
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
                                                                $('input[data-l2key="psk"]').value(result);
								$('#div_alert').showAlert({message: "{{Réussie, n'oubliez pas de sauvegarder}}", level: "success"});
                                                                //bootbox.alert("Succès, veuillez renseigner le code dans la zone Clé TV / Code PIN puis passer à l\'étape 3.");
							}
                                                    });
                                                }
                                            });
                                        });
                    
                    
                    
						
					</script>
				</div>
                                <div class="col-sm-1">
                                
                                </div>
			</div>
			
    </fieldset>
</form>

</div>
<div role="tabpanel" class="tab-pane" id="commandtab">
    <a class="btn btn-default btn-sm pull-right" id="bt_addsonybraviaInfo" style="margin-top:5px;"><i class="fa fa-plus-circle"></i> {{Ajouter une info}}</a>
    <a class="btn btn-default btn-sm  pull-right" id="bt_addsonybraviaAction" style="margin-top:5px;"><i class="fa fa-plus-circle"></i> {{Ajouter une commande}}</a><br/><br/>
    <table id="table_cmd" class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th style="width: 50px;">#</th>
                <th style="width: 230px;">{{Nom}}</th>
                <th style="width: 110px;">{{Sous-Type}}</th>
                <th>{{Information / Commande}}</th>
                <!--<th style="width: 100px;">{{}}</th>-->
                <th style="width: 300px;">{{Paramètres}}</th>
                <th style="width: 150px;"></th>
                <th style="width: 150px;"></th>
            </tr>
        </thead>
        <tbody>

        </tbody>
    </table>

</div>
</div>

</div>
</div>

<?php include_file('desktop', 'sonybravia', 'js', 'sonybravia');?>
<?php include_file('core', 'plugin.template', 'js');?>