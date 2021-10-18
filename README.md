# TG Count  
- This script generates a PHP file with stats for the most used TG and the most seen callsings.  
- It works with FreeDMR logbook and also with 'lastheard.log' from HBMonV2, if you are running in separate servers.  
- It includes two templates located inside the templates file, you can choose wich of them you want to use in the configuration section of tgcount.py.  
  - tgcount.php works with [HBMonv2](https://github.com/sp2ong/HBMonv2).  
  - stand_alone.php is the standalone version.  
- It needs a log level of INFO at least.  
- It has been tested on Debian 10.  
- This is a Beta release.  

**Installation**
```
cd /opt    
sudo git clone https://github.com/yuvelq/TG_Count.git
cd TG_Count
sudo cp config.sample.py config.py
```
Modify the configuration in **config.py** to match your system configuration, you can use the editor of your preference.  
```
sudo nano config.py
``` 
If you have the download files enabled on the FreeDMR server, set the DOWNLOAD_FILES to False.  
>DOWNLOAD_FILES = False
```
sudo cp systemd/tgcount.service /lib/systemd/system  
```
If you want to start tgcount automatically after restart the system.
```
sudo systemctl enable tgcount.service 
```
You can start, stop or restart tgcount with the next commands:
```
Start:  
sudo systemctl start tgcount.service

Stop:  
sudo systemctl stop tgcount.service

Restart:  
sudo systemctl restart tgcount.service
```
The last step is to add the tgcount button in HBMonv2, this step is no necessary if you will use the standalone template only.  

Modify the buttons.html, usually it's located inside /var/www/html:  
```
sudo nano buttons.html
```
Add this after the last button configured:  
```
&nbsp;
<a href="count.php"><button class="button link">&nbsp;Most Used TG&nbsp;</button></a>
&nbsp;
```
Now the installation is completed, thank you for install this script any feedback is welcome.  
73! 
<br/><br/><br/><br/>
# TG Count
- Este script genera un archivo PHP con estadisticas de los TG mas utilizados y los indicativos mas vistos. 
- El script funciona con el logbook del servidor FreeDMR y también con 'lastheard.log' de HBMon esto es útil cuando funcionan es servidores distintos.  
- Se incluyen dos plantillas que estan ubicadas en la carpeta templates, se puede seleccionar cual utilizar en la sección de configuracion de tgcount.py. 
  - tgcount.php trabaja con [HBMonv2](https://github.com/sp2ong/HBMonv2).
  - stand_alone.php trabaja independientemente.  
- Se necesita tener un nivel the logbook de por lo menos INFO.  
- Este script ha sido probado en Debian 10. 
- Esta es una version Beta. 

**Instalación**
```
cd /opt    
sudo git clone https://github.com/yuvelq/TG_Count.git  
cd TG_Count
cp config.sample.py config.py
```
Modifica la sección de configuración al inicio de **config.py** para que se adapte a tu sistema, puedes utilizar un editor de texto de tu preferencia.  
```
sudo nano config.py
``` 
Si tienes activada la opción de descarga en el servidor FreeDMR, cambia la opción DOWNLOAD_FILES a False.
>DOWNLOAD_FILES = False
```
sudo cp systemd/tgcount.service /lib/systemd/system  
```
Si quieres que tgcount inicie automáticamente después de reiniciar el sistema.
```
sudo systemctl enable tgcount.service 
```
Puedes iniciar, detener y reiniciar tgcount con los siguientes comandos:
```
Iniciar:
sudo systemctl start tgcount.service

Detener:
sudo systemctl stop tgcount.service

Reiniciar:
sudo systemctl restart tgcount.service
```
El último paso es agregar el botón de tgcount a HBMonv2, este paso no es necesario si solo vas a utilizar la plantilla independiente. 

Modificamos el archivo buttons.html, usualmente lo puedes localizar en /var/www/html:  
```
sudo nano buttons.html
```
Agregamos las siguientes líneas al final de los botones ya configurados: 
```
&nbsp;
<a href="count.php"><button class="button link">&nbsp;Most Used TG&nbsp;</button></a>
&nbsp;
```
Con eso finalizamos la instalación, gracias por utilizar este script, cualquier comentario es bienvenido.  
73!  
