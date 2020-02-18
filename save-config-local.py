
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.scp import SCP
from datetime import datetime

dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36" 
   } 


login_username = "ysaied"

time_now = datetime.now().strftime("%d%b%Y_%I:%M_%p")
backup_conf_filename = str("config-backup-" + time_now)
print (backup_conf_filename)

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)

#   dev.open()
   
#   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)

   with SCP(dev, progress=True) as file:
      file.get("/config/juniper.conf.gz", remote_path=backup_conf_filename)

#   print ("="*(44+len(src_node)) + "\n")
   
   
#   dev.close()
