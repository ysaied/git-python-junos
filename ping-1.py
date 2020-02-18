
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json


dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36" 
   } 
dev_loopback = { "KIF_VPN" : "1.0.0.11", 
   "HRZ_VPN" : "1.0.0.12", 
   "AMS_VPN" : "1.0.0.13", 
   "LON_VPN" : "1.0.0.14"
   }  

login_username = "ysaied"

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   for dst_node, loopback_ip in dev_loopback.items():
      ping_dst_loopback = dev.rpc.ping(host=loopback_ip, count="10", rapid=True)
      if ( ping_dst_loopback.find('.//ping-success') is not None):
         print ("Destination %s is Reachable!" % dst_node )
      else:
         print ("Destination %s is NOT Reachable!" % dst_node )
   dev.close()
