
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.scp import SCP
from datetime import datetime


dev_mgmt = { "KIF_VPN" : "10.117.97.56"
   } 

login_username = "ysaied"


test_3_6 = list()
test_3_6_1 = "show services ipsec-vpn ike security-associations"
test_3_6_2 = "show services ipsec-vpn ipsec security-associations"
test_3_6_3 = "show services ipsec-vpn ipsec statistics"


for a in range(1,4):
  show_cmd = vars()[("test_3_6_%d" % a)]
  test_3_6.append(show_cmd)

time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
today = datetime.now().strftime("%d-%h-%Y")

show_all = test_3_6

for src_node, mgmt_ip in dev_mgmt.items():
      
   file_name = src_node+"-"+"JUNOS-18_4R3-Upgrade_TestPlan_3_6-Date_"+today+"_outputs.txt"
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

