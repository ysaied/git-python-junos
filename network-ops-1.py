
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



show_a = list()
show_a0 = "show chassis hardware"
show_a1 = "show chassis hardware clei-models"
show_a2 = "show chassis fpc detail"
show_a3 = ""
show_a4 = "show chassis fpc pic-status"
show_a5 = "show chassis alarms"
show_a6 = "show system alarms"
show_a7 = 'show version invoke-on all-routing-engines | except "JUNOS "'
show_a8 = "show chassis routing-engine"

for a in range(9):
  show_cmd = vars()[("show_a%d" % a)]
  show_a.append(show_cmd)

show_b = list()
show_b0 = "show interfaces terse" 
show_b1 = "show ospf interface"
show_b2 = "show ospf neighbor"
show_b3 = "show ospf database"
show_b4 = "show ted database"
show_b5 = 'show route 1.0.0.0/24'
show_b6 = "show mpls interface"
show_b7 = "show ldp interface"
show_b8 = "show ldp neighbor "
show_b9 = "show route table inet.3 protocol ldp"
show_b10 = "show rsvp interface"
show_b11 = "show rsvp neighbor"
show_b12 = "show rsvp session"
show_b13 = "show route table inet.3 protocol rsvp"
show_b14 = "show mpls lsp ingress"
show_b15 = "show bgp summary"

for b in range(16):
  show_cmd = vars()[("show_b%d" % b)]
  show_b.append(show_cmd)

show_c = list()
show_c0 = "show route table l3vpn-option_a-%d"
show_c1 = "show route table l3vpn-option_c-%d"
show_c2 = "show l2vpn connections"
show_c3 = "show l2circuit connections"
show_c4 = "show vpls connections"
show_c5 = "show vpls mac-table"
show_c6 = "show route protocol bgp table bgp.l3vpn.0"
show_c7 = "show route protocol bgp table bgp.l2vpn.0"
show_c8 = "show route protocol bgp table bgp.rtarget.0"
show_c9 = "show route summary"
show_c10 = "show ldp database inet"
show_c11 = "show ldp database l2circuit"

for n in range(101,106):
  show_c.append(show_c0 % n)
for n in range(111,116):
  show_c.append(show_c1 % n)
for c in range(2,12):
  show_cmd = vars()[("show_c%d" % c)]
  show_c.append(show_cmd)

time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
today = datetime.now().strftime("%d-%h-%Y")

show_all = show_a + show_b + show_c

#file_output = open("junos-output.txt", "w")

for src_node, mgmt_ip in dev_mgmt.items():
   
   file_output = open(src_node+"_"+today+"_outputs.txt", "w")
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
   
### collect show configuration  

   print ("\t progressing show configuration")
   print >> file_output, ("\n" + "="*5 + " "*2 + "show configuration" + " @ " + src_node + " "*2 + "="*5)      
   print >> file_output, etree.tostring(dev.rpc.get_config(options={'format':'text', 'inherit':'inherit'}), encoding='unicode', pretty_print=True)
   
   print >> file_output, ("\n" + "="*(44+len(src_node)+len(time_now)) + "\n")   
   dev.close()
   file_output.close()
   print ("closing file for %s" % src_node)

