#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.fs import FS
from datetime import datetime
from pprint import pprint

dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36", 
   "Partner" : "10.117.97.39"
   } 

login_username = "ysaied"


for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   dev_info = dev.facts
#   pprint (dev_info)
   print ( "version {} model {}".format(dev.facts["version_RE1"],dev.facts["model"]))
#   for key, value in dev_info.items():
#      print ("{} ----> {}".format(key, value))
   print ("="*50)
   dev.close()
