
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.scp import SCP
from datetime import datetime

# dev_mgmt = { "vMX_RR-21" : "87.201.172.205" } 
dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36", 
   "Partner" : "10.117.97.39"
   } 

login_username = "ysaied"

time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
today = datetime.now().strftime("%d-%h-%Y")

for src_node, mgmt_ip in dev_mgmt.items():

   file_output = open(src_node+"_"+today+"_outputs.txt", "w")
   print ("open file for %s" % src_node)
   
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()

### collect show configuration  

   print ("\t progressing show configuration")
   print >> file_output, ("\n" + "="*5 + " "*2 + "show configuration" + " @ " + src_node + " "*2 + "="*5)      
   print >> file_output, etree.tostring(dev.rpc.get_config(options={'format':'text', 'inherit':'inherit'}), encoding='unicode', pretty_print=True)
   
   print >> file_output, ("\n" + "="*(44+len(src_node)+len(time_now)) + "\n")   
   dev.close()
   file_output.close()
   print ("closing file for %s" % src_node)