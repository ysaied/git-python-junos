
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
   "LON_VPN" : "10.117.97.36"
   } 

login_username = "ysaied"

ce_ifd = { "KIF_VPN" : "xe-2/0/0", 
   "HRZ_VPN" : "xe-0/3/0", 
   "AMS_VPN" : "ge-0/2/9", 
   "LON_VPN" : "ge-3/1/7"
   } 


test_3_4 = list()
test_3_4_1 = "show configuration class-of-service interfaces"


for a in range(1,2):
  show_cmd = vars()[("test_3_4_%d" % a)]
  test_3_4.append(show_cmd)

time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
today = datetime.now().strftime("%d-%h-%Y")

show_all = test_3_4

for src_node, mgmt_ip in dev_mgmt.items():
      
   file_name = src_node+"-"+"JUNOS-18_4R3-Upgrade_TestPlan_3_4-Date_"+today+"_outputs.txt"
   file_output = open(file_name, "w")
   print ("open file for %s" % src_node)
   
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()

   print >> file_output, ("#"*(len(src_node) + len(time_now) + 46))
   print >> file_output, ("\n" + "="*20 + " "*2 + src_node + " "*2 + time_now + " "*2 + "="*20)
   
   for show in show_all:
      print >> file_output, ("\n" + "="*5 + " "*2 + show + " @ " + src_node + " "*2 + "="*5)          
      try :
         output = dev.rpc.cli(show, format='text')
         if type(output) is bool:
            print >> file_output, ("NO Output Available !!!!")
         else:
            print >> file_output, (output.text)
            print ("\t progressing %s" % show)
      except:
         print >> file_output, ("NOT Supported command !!!!")
   
   print >> file_output, ("\n" + "="*(44+len(src_node)+len(time_now)) + "\n")   
   dev.close()
   file_output.close()
   print ("closing file for %s" % src_node)

