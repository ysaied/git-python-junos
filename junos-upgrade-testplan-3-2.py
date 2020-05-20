
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



test_3_2 = list()
test_3_2_1 = "show interfaces terse"
test_3_2_2 = "show ospf interface"
test_3_2_3 = "show ospf neighbor"
test_3_2_4 = "show ospf database"
test_3_2_5 = "show ted database"
test_3_2_6 = "show route protocol ospf"
test_3_2_7 = "show mpls interface"
test_3_2_8 = "show ldp interface"
test_3_2_9 = "show ldp neighbor"
test_3_2_10 = "show route table inet.3 protocol ldp"
test_3_2_11 = "show rsvp interface"
test_3_2_12 = "show rsvp neighbor"
test_3_2_13 = "show rsvp session"
test_3_2_14 = "show route table inet.3 protocol rsvp"
test_3_2_15 = "show mpls lsp ingress"
test_3_2_16 = "show bgp summary"

for a in range(1,17):
  show_cmd = vars()[("test_3_2_%d" % a)]
  test_3_2.append(show_cmd)

time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
today = datetime.now().strftime("%d-%h-%Y")

show_all = test_3_2

for src_node, mgmt_ip in dev_mgmt.items():
      
   file_name = src_node+"_"+"JUNOS-18_4R3-Upgrade-TestPlan-3_2_"+today+"_outputs.txt"
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

