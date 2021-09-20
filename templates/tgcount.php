<?php
$progname = basename($_SERVER['SCRIPT_FILENAME'],".php");
include_once 'include/config.php';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" lang="en">
<head>
<meta charset="UTF-8">
<title>Most Used Talk Groups</title>
<script type="text/javascript" src="scripts/hbmon.js"></script>
<link rel="stylesheet" type="text/css" href="css/styles.php" />
<meta name="description" content="Copyright (c) 2016-21.The Regents of the K0USY Group. All rights reserved. Version SP2ONG 2019-2021 (v2021)" />
<meta http-equiv="refresh" content="60">
</head>
<body style="background-color: #d0d0d0;font: 10pt arial, sans-serif;">
<center><div style="width:1250px; text-align: center; margin-top:5px;">
<img src="img/freedmr.jpg?random=323527528432525.24234" alt="" />
</div>
<div style="width: 1100px;">
<p style="text-align:center;"><span style="color:#000;font-size: 18px; font-weight:bold;"><?php echo REPORT_NAME;?></span></p>
<p></p>
</div>
<?php include_once 'buttons.html'; ?>
<!-- TG table -->
<div style="width: 1100px; margin-left:0px;">
<fieldset style="box-shadow:0 0 10px #999;background-color:#e0e0e0e0; width:1050px;margin-left:15px;margin-right:15px;font-size:14px;border-top-left-radius: 10px; border-top-right-radius: 10px;border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;">
<legend><b><font color="#000">&nbsp;.: Most Used TGs :.&nbsp;</font></b></legend>
<table style="margin-top:5px; table-layout:fixed; font: 10pt arial, sans-serif;background-color: #f9f9f9f9;">
    <tr class="theme_color" style=" height: 32px;font: 10pt arial, sans-serif;border:0;">
        <th style='width: 90px;'>TG Number</th>
        <th style='width: 350px;'>Talk Group Name</th>
        <th style='width: 120px;'>Number of QSO</th>
        <th style='width: 120px;'>Total QSO Time</th>
        <th style='width: 320px;'>Most Seen Callsign</th>
    </tr>

</table>
<br>
<B><span style="text-align: center;">This information is updated every 3 minutes, QSO time in minutes.</B><br> 
Only takes into account a QSO of the current day that lasts more than 5 seconds.<br>
Single Callsign or FreeDMR with high QSO is a Bridge.<br></span>
</fieldset></div><br>

<p style="text-align: center;"><span style="text-align: center;">
Copyright (c) 2016-2021<br>The Regents of the <a href=http://k0usy.mystrikingly.com/>K0USY Group</a>. All rights reserved.<br><a href=https://github.com/sp2ong/HBMonv2>Version SP2ONG 2019-2021</a><br><br></span>
    <!-- THIS COPYRIGHT NOTICE MUST BE DISPLAYED AS A CONDITION OF THE LICENCE GRANT FOR THIS SOFTWARE. ALL DERIVATEIVES WORKS MUST CARRY THIS NOTICE -->
    <!-- This is version of HBMonitor SP2ONG 2019-2021 (v2021) -->
</p>
</center>
</body>
</html>
