
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json


dev_dic = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36", 
   "Partner" : "10.117.97.39" 
   }  

login_username = "ysaied"

for node, ip in dev_dic.items():
   dev = Device(host= ip, user= login_username)
   dev.open()
   ping_mgmt_gw = dev.rpc.ping(host="10.117.97.1", count="10", rapid=True)
   print (etree.tostring(ping_mgmt_gw, encoding='unicode', pretty_print=True))
   dev.close()
