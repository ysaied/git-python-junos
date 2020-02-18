
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.fs import FS
from datetime import datetime

dev_mgmt = { "KIF_VPN" : "10.117.97.39" }


login_username = "ysaied"

time_now = datetime.now().strftime("%d%b%Y_%I:%M_%p")
backup_conf_filename = str("config-backup-" + time_now)
print (backup_conf_filename)

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)

   dev.open()
   file_copy = dev.rpc.file_copy(source="/config/juniper.conf.gz", destination="/var/home/ysaied/%s" % backup_conf_filename)   
#   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)


#   print ("="*(44+len(src_node)) + "\n")
   
   
   dev.close()
