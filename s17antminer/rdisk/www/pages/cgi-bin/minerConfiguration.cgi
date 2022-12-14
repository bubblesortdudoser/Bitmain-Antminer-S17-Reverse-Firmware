#!/bin/sh -e

create_default_conf_file()
{
(
cat <<'EOF'
{
	"pools" : [
		{
			"url" : "http://stratum.antpool.com:3333",
			"user" : "antminer_1",
			"pass" : "123"
		},
		{
			"url" : "http://stratum.antpool.com:443",
			"user" : "antminer_1",
			"pass" : "123"
		},
		{
			"url" : "http://stratum.antpool.com:25",
			"user" : "antminer_1",
			"pass" : "123"
		}
	],
	"api-listen" : "true",
	"api-network" : "true",
	"api-allow" : "W:0/0",
	"multi-version" : "4",
	"bitmain-freq": "275",
	"bitmain-voltage": "1730"
}

EOF
) > /config/cgminer.conf
}

if [ ! -f /config/cgminer.conf ] ; then
    if [ -f /config/cgminer.conf.factory ] ; then
        cp /config/cgminer.conf.factory /config/cgminer.conf
    else
        create_default_conf_file
    fi
fi

ant_result=`cat /config/cgminer.conf`

# CGI output must start with at least empty line (or headers)
printf "Content-type: text/html\r\n\r\n"

cat <<-EOH
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="cache-control" content="no-cache" />
<link rel="stylesheet" type="text/css" media="screen" href="/css/cascade.css" />
<!--[if IE 6]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie6.css" /><![endif]-->
<!--[if IE 7]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie7.css" /><![endif]-->
<!--[if IE 8]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie8.css" /><![endif]-->
<script type="text/javascript" src="/js/xhr.js"></script>
<script type="text/javascript" src="/js/jquery-1.10.2.js"></script>
<script type="text/javascript" src="/js/json2.min.js"></script>
<script>
EOH

echo "ant_data = ${ant_result};"
echo 'miner_type = {"value":"S17+"};'

cat <<EOT
function f_get_miner_conf() {
    try
    {
        for(var i = 0; i < ant_data.pools.length; i++) {
            switch(i) {
            case 0:
                jQuery("#ant_pool1url").val(ant_data.pools[i].url);
                jQuery("#ant_pool1user").val(ant_data.pools[i].user);
                jQuery("#ant_pool1pw").val(ant_data.pools[i].pass);
                break;
            case 1:
                jQuery("#ant_pool2url").val(ant_data.pools[i].url);
                jQuery("#ant_pool2user").val(ant_data.pools[i].user);
                jQuery("#ant_pool2pw").val(ant_data.pools[i].pass);
                break;
            case 2:
                jQuery("#ant_pool3url").val(ant_data.pools[i].url);
                jQuery("#ant_pool3user").val(ant_data.pools[i].user);
                jQuery("#ant_pool3pw").val(ant_data.pools[i].pass);
                break;
            }
        }
        if(ant_data["bitmain-nobeeper"]) {
            document.getElementById("ant_beeper").checked = false;
        } else {
            document.getElementById("ant_beeper").checked = true;
        }
        if(ant_data["bitmain-notempoverctrl"]) {
            document.getElementById("ant_tempoverctrl").checked = false;
        } else {
            document.getElementById("ant_tempoverctrl").checked = true;
        }
        if(ant_data["bitmain-fan-ctrl"]) {
            document.getElementById("ant_fan_customize_switch").checked = true;
        
        } else {
            document.getElementById("ant_fan_customize_switch").checked = false;
        }
		
    if(miner_type["value"] == "S17+") {
        if(ant_data["bitmain-work-mode"] == 0) {
            document.getElementById("ant_work_mode_0").checked = true;
        } else if(ant_data["bitmain-work-mode"] == 0xfe){
			document.getElementById("ant_work_mode_sleep").checked = true;
		}
    }
		
        document.getElementById("ant_voltage").value=ant_data["bitmain-voltage"];
        document.getElementById("ant_freq").value=ant_data["bitmain-freq"];
        
        jQuery("#ant_fan_customize_value").val(ant_data["bitmain-fan-pwm"]);

    }
    catch(err)
    {
        alert('Invalid Miner configuration file. Edit manually or reset to default.');
    }
}
function f_submit_miner_conf() {
    _ant_freq = "18:218.75:1106";
    _ant_voltage = "0725";
    try
    {
        _ant_freq = ant_data["bitmain-freq"];
        _ant_voltage = ant_data["bitmain-voltage"];
    }
    catch(err)
    {
        alert('Invalid Miner configuration file. Edit manually or reset to default.');
    }
    
    _ant_pool1url = jQuery("#ant_pool1url").val();
    _ant_pool1user = jQuery("#ant_pool1user").val();
    _ant_pool1pw = jQuery("#ant_pool1pw").val();
    _ant_pool2url = jQuery("#ant_pool2url").val();
    _ant_pool2user = jQuery("#ant_pool2user").val();
    _ant_pool2pw = jQuery("#ant_pool2pw").val();
    _ant_pool3url = jQuery("#ant_pool3url").val();
    _ant_pool3user = jQuery("#ant_pool3user").val();
    _ant_pool3pw = jQuery("#ant_pool3pw").val();
    _ant_nobeeper = "false";
    _ant_notempoverctrl = "false";
    _ant_fan_customize_switch = "false";
    _ant_fan_customize_value = jQuery("#ant_fan_customize_value").val();
    
    if(document.getElementById("ant_beeper").checked) {
        _ant_nobeeper = "false";
    } else {
        _ant_nobeeper = "true";
    }
    if(document.getElementById("ant_tempoverctrl").checked) {
        _ant_notempoverctrl = "false";
    } else {
        _ant_notempoverctrl = "true";
    }

    if(document.getElementById("ant_fan_customize_switch").checked) {
        _ant_fan_customize_switch= "true";
        
    } else {
        _ant_fan_customize_switch= "false";
    }

    if(miner_type["value"] == "S17+") {
		if(document.getElementById("ant_work_mode_0").checked) {
	    	_ant_work_mode = 0;
	   } else if (document.getElementById("ant_work_mode_sleep").checked){
			_ant_work_mode = 0xfe;
	   }
	}
	
    _ant_voltage=jQuery("#ant_voltage").val();
    _ant_freq=jQuery("#ant_freq").val();
    jQuery("#cbi_apply_bmminer_fieldset").show();
    
    jQuery.ajax({
        url: '/cgi-bin/set_miner_conf.cgi',
        type: 'POST',
        dataType: 'json',
        timeout: 30000,
        cache: false,
        data: {_ant_pool1url:_ant_pool1url, _ant_pool1user:_ant_pool1user, _ant_pool1pw:_ant_pool1pw,_ant_pool2url:_ant_pool2url, _ant_pool2user:_ant_pool2user, _ant_pool2pw:_ant_pool2pw,_ant_pool3url:_ant_pool3url, _ant_pool3user:_ant_pool3user, _ant_pool3pw:_ant_pool3pw, _ant_nobeeper:_ant_nobeeper, _ant_notempoverctrl:_ant_notempoverctrl,_ant_fan_customize_switch:_ant_fan_customize_switch,_ant_fan_customize_value:_ant_fan_customize_value, _ant_freq:_ant_freq, _ant_voltage:_ant_voltage, _ant_work_mode:_ant_work_mode},
        success: function(data) {
            window.location.reload();
        },
        error: function() {
            window.location.reload();
        }
    });
}

function f_reset_miner_conf() {
     jQuery("#cbi_apply_bmminer_fieldset").show();
     jQuery.ajax({
        url: '/cgi-bin/reset_miner_conf.cgi',
        type: 'POST',
        dataType: 'json',
        timeout: 30000,
        cache: false,
        data: {},
        success: function(data) {
            window.location.reload();
        },
        error: function() {
            window.location.reload();
        }
    });
}


jQuery(document).ready(function() {
    f_get_miner_conf();
});
</script>
<title>Ant Miner</title>
</head>
<body class="lang_en">
   <p class="skiplink">
      <span id="skiplink1"><a href="#navigation">Skip to navigation</a></span>
      <span id="skiplink2"><a href="#content">Skip to content</a></span>
   </p>
   <div id="menubar">
      <h2 class="navigation"><a id="navigation" name="navigation">Navigation</a></h2>
      <div class="clear"></div>
   </div>
   <div id="menubar" style="background-color: #0a2b40;">
      <div class="hostinfo" style="float: left; with: 500px;">
         <img src="/images/antminer_logo.png" width="92" height="50" alt="" title="" border="0" />
      </div>
      <div class="clear"></div>
   </div>
   <div id="maincontainer">
      <div id="tabmenu">
         <div class="tabmenu1">
            <ul class="tabmenu l1">
               <li class="tabmenu-item-status"><a href="/index.html">System</a></li>
               <li class="tabmenu-item-system active"><a href="/cgi-bin/minerConfiguration.cgi">Miner Configuration</a></li>
               <li class="tabmenu-item-network"><a href="/cgi-bin/minerStatus.cgi">Miner Status</a></li>
               <li class="tabmenu-item-system"><a href="/network.html">Network</a></li>
            </ul>
            <br style="clear: both" />
			<!--
            <div class="tabmenu2">
               <ul class="tabmenu l2">
                  <li class="tabmenu-item-system active"><a href="/cgi-bin/minerConfiguration.cgi">General Settings</a></li>
                  <li class="tabmenu-item-system"><a href="/cgi-bin/minerAdvanced.cgi">Advanced Settings</a></li>
               </ul>
               <br style="clear: both" />
            </div>
			-->
         </div>
      </div>
      <div id="maincontent">
         <noscript>
            <div class="errorbox">
               <strong>Java Script required!</strong><br /> You must enable Java Script in your browser or LuCI will not work properly.
            </div>
         </noscript>
         <h2 style="padding-bottom:10px;"><a id="content" name="content">Miner General Configuration</a></h2>
         <div class="cbi-map" id="cbi-cgminer">
            <fieldset class="cbi-section" id="cbi_msg_bmminer_fieldset" style="display:none">
               <span id="cbi_msg_bmminer" style="color:red;"></span>
            </fieldset>
            <fieldset class="cbi-section" id="cbi_apply_bmminer_fieldset" style="display:none">
               <img src="/resources/icons/loading.gif" alt="Loading" style="vertical-align:middle" />
               <span id="cbi-apply-cgminer-status">Waiting for changes to be applied...</span>
            </fieldset>
            <fieldset class="cbi-section" id="cbi-cgminer-cgminer">
               <div class="cbi-section-descr"></div>
               <fieldset class="cbi-section" id="cbi-cgminer-default">
                  <legend>Pool 1</legend>
                  <div class="cbi-value" id="cbi-cgminer-default-pool1url">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool1url">URL</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool1url" id="ant_pool1url" value="" />
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-cgminer-default-pool1user">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool1user">Worker</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool1user" id="ant_pool1user" value="" />
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-cgminer-default-pool1pw">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool1pw">Password</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool1pw" id="ant_pool1pw" value="" />
                     </div>
                  </div>
               </fieldset>
               <fieldset class="cbi-section" id="cbi-cgminer-default">
                  <legend>Pool 2</legend>
                  <div class="cbi-value" id="cbi-cgminer-default-pool2url">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool2url">URL</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool2url" id="ant_pool2url" value="" />
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-cgminer-default-pool2user">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool2user">Worker</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool2user" id="ant_pool2user" value="" />
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-cgminer-default-pool2pw">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool2pw">Password</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool2pw" id="ant_pool2pw" value="" />
                     </div>
                  </div>
               </fieldset>
               <fieldset class="cbi-section" id="cbi-cgminer-default">
                  <legend>Pool 3</legend>
                  <div class="cbi-value" id="cbi-cgminer-default-pool3url">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool3url">URL</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool3url" id="ant_pool3url" value="" />
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-cgminer-default-pool3user">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool3user">Worker</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool3user" id="ant_pool3user" value="" />
                     </div>
                  </div>
                  <div class="cbi-value cbi-value-last"
                     id="cbi-cgminer-default-pool3pw">
                     <label class="cbi-value-title" for="cbid.cgminer.default.pool3pw">Password</label>
                     <div class="cbi-value-field">
                        <input type="text" class="cbi-input-text" name="cbid.cgminer.default.pool3pw" id="ant_pool3pw" value="" />
                     </div>
                  </div>
               </fieldset>
               <fieldset class="cbi-section" id="cbi-cgminer-default" style="display">
                  <legend>Setup</legend>
                  <div class="cbi-value" id="beep" style="display:none">
                     <label class="cbi-value-title" for="keep">Beeper ringing</label>
                     <div class="cbi-value-field">
                        <input type="checkbox" name="ant_beeper" id="ant_beeper" checked />
                     </div>
                  </div>
                  <div class="cbi-value" id="temp_over" style="display:none">
                     <label class="cbi-value-title" for="keep">Stop running when temprerature is over 80&#8451; </label>
                     <div class="cbi-value-field">
                        <input type="checkbox" name="ant_tempoverctrl" id="ant_tempoverctrl" checked />
                     </div>
                  </div>
                  <div class="cbi-value" id="fan_ctrl" style="display:none">
                     <label class="cbi-value-title" for="keep">Customize the fan speed percentage</label>
                     <div class="cbi-value-field">
                        <input type="checkbox" name="ant_fan_customize_check" id="ant_fan_customize_switch" />
                        <input type="text" class="cbi-input-text" style="width:30px;" name="ant_fan_customize_box" id="ant_fan_customize_value" value="" />%
                     </div>
                  </div>
				  <div class="cbi-value">
					 <label class="cbi-value-title" for="keep">Work Mode</label>
					 <div class="cbi-value-field" id="miner_work_mode">
					 </div>
				  </div>				  
                  <div class="cbi-value" id="cbi-bmminer-default-voltage"  style="display:none">
                     <label class="cbi-value-title" for="cbid.bmminer.default.voltage">Set Voltage:(CAUTION: This setting may damage the miner, please test smaller value first!)</label>
                     <div class="cbi-value-field">
                        <select id="ant_voltage" class="cbi-input-text">
                           <option value="1700"> 17.00V </option>
                           <option value="1710"> 17.10V </option>
                           <option value="1720"> 17.20V </option>
                           <option value="1730"> 17.30V </option>
                           <option value="1740"> 17.40V </option>
                           <option value="1750"> 17.50V </option>
                           <option value="1760"> 17.60V </option>
                           <option value="1770"> 17.70V </option>
                           <option value="1780"> 17.80V </option>
                           <option value="1790"> 17.90V </option>
                           <option value="1800"> 18.00V </option>
                           <option value="1810"> 18.10V </option>
                           <option value="1820"> 18.20V </option>
                           <option value="1830"> 18.30V </option>
                           <option value="1840"> 18.40V </option>
                           <option value="1850"> 18.50V </option>
                           <option value="1860"> 18.60V </option>
                           <option value="1870"> 18.70V </option>
                           <option value="1880"> 18.80V </option>
                           <option value="1890"> 18.90V </option>
                           <option value="1900"> 19.00V </option>
                           <option value="1910"> 19.10V </option>
                           <option value="1920"> 19.20V </option>
                           <option value="1930"> 19.30V </option> 
                           <option value="1940"> 19.40V </option>
                           <option value="1950"> 19.50V </option>
                           <option value="1960"> 19.60V </option>
                           <option value="1970"> 19.70V </option>
                           <option value="1980"> 19.80V </option>
                           <option value="1990"> 19.90V </option>
                           <option value="2000"> 20.00V </option>
                        </select>
                     </div>
                  </div>
                  <div class="cbi-value" id="cbi-bmminer-default-freq"  style="display:none">
                     <label class="cbi-value-title" for="cbid.bmminer.default.freq">Set Frequency:</label>
                     <div class="cbi-value-field">
                        <select id="ant_freq" class="cbi-input-text">
                           <option value="200"> 200.00M </option>
                           <option value="225"> 225.00M </option>
                           <option value="250"> 250.00M </option>
                           <option value="275"> 275.00M </option>
                           <option value="300"> 300.00M </option>
                           <option value="325"> 325.00M </option>
                           <option value="350"> 350.00M </option>
                           <option value="375"> 375.00M </option>
                           <option value="400"> 400.00M </option>
                           <option value="425"> 425.00M </option>
                           <option value="450"> 450.00M </option>
                           <option value="475"> 475.00M </option>
                           <option value="500"> 500.00M </option>
                           <option value="525"> 525.00M </option>
                           <option value="550"> 550.00M </option>
                           <option value="575"> 575.00M </option>
                           <option value="600"> 600.00M </option>
                           <option value="625"> 625.00M </option>
                           <option value="650"> 650.00M </option>
                           <option value="675"> 675.00M </option>
                           <option value="700"> 700.00M </option>
                           <option value="725"> 725.00M </option>
                           <option value="750"> 750.00M </option>
                           <option value="775"> 775.00M </option>
                           <option value="800"> 800.00M </option>
                        </select>
                     </div>
                  </div>
               </fieldset>
               <br />
            </fieldset>
            <br />
         </div>
         <div class="cbi-page-actions">
            <input class="cbi-button cbi-button-save right" type="button" onclick="f_submit_miner_conf();" value="Save&Apply" />
            <input class="cbi-button cbi-button-reset right" type="button" onclick="f_get_miner_conf();" value="Reset" />
         </div>
         <div class="clear"></div>
      </div>
   </div>
   <div class="clear"></div>
   <div style="text-align: center; bottom: 0; left: 0; height: 1.5em; font-size: 80%; margin: 0; padding: 5px 0px 2px 8px; background-color: #918ca0; width: 100%;">
      <font style="color:#fff;">Copyright &copy; 2013-2014, Bitmain Technologies</font>
   </div>
</body>
                  <script type="text/javascript">
                      var div = document.getElementById("miner_work_mode");
                      if(miner_type["value"] == "S17+")
                          div.innerHTML = ' <input type="radio" id="ant_work_mode_sleep" name="ant_work_mode" value="0xfe" checked /> Sleep Mode <br> <input type="radio" id="ant_work_mode_0" name="ant_work_mode" value="0" /> Normal';
                  </script>
</html>
EOT
