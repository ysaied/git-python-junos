
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.scp import SCP
from datetime import datetime

dev_mgmt = { "vMX_RR-21" : "87.201.172.205" } 

login_username = "ysaied"



show_a = list()
show_a0 = "show chassis hardware"
show_a1 = "show chassis hardware clei-models"
show_a2 = "show chassis fpc detail"
show_a3 = "show chassis fpc errors"
show_a4 = "show chassis fpc pic-status"
show_a5 = "show chassis alarms"
show_a6 = "show system alarms"
show_a7 = "show version invoke-on all-routing-engines"
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
show_b5 = "show route protocol ospf"
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

for n in range(101,106):
  show_c.append(show_c0 % n)
for n in range(111,116):
  show_c.append(show_c1 % n)
for c in range(2,6):
  show_cmd = vars()[("show_c%d" % c)]
  show_c.append(show_cmd)



time_now = datetime.now().strftime("%A__%d-%h-%Y__%I:%M %p")
show_all = show_a + show_b + show_c


for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   
   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + time_now + "="*20)
   
   for show in show_all:
      print (show)
      output = dev.rpc.cli(show, format='text')
      if type(output) is bool:
         print ("NO Output Available !!!!")
      else:
         print (output.text)

   print ("="*(44+len(src_node)+len(time_now)) + "\n")
   
   dev.close()
