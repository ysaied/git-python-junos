
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

def check_reachabilitily(node_name, node_ip): 
   rpc_ping = dev.rpc.ping(host=node_ip, count="10", rapid=True)
   if ( rpc_ping.find('.//ping-success') is not None):
      print ("Destination %s is Reachable!" % node_name )
   else:
      print ("Destination %s is NOT Reachable!" % node_name )

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   
   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)
   
   for dst_node, loopback_ip in dev_loopback.items():
      check_reachabilitily(dst_node, loopback_ip)   
   
   
   print ("="*(44+len(src_node)) + "\n")
   
   dev.close()
