
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.fs import FS
from datetime import datetime


dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36", 
   "Partner" : "10.117.97.39"
   } 

login_username = "ysaied"

#time_now = datetime.now().strftime("%d%b%Y_%I:%M_%p")
backup_conf_filename = str("./" + "config-backup-" + datetime.now().strftime("%d%b%Y_%I:%M_%p") + ".gz")

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   try:
      file_copy = dev.rpc.file_copy(source="/config/juniper.conf.gz", destination=backup_conf_filename)
      print ("Running-configuration Saved!")
   except:
      print ("Running-configuration NOT Saved!")

   dev.close()
