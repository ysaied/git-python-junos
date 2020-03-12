
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
show_b6 = "show mpls interfaces"
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


print (show_a)
print (show_b)


show_c0 = "show route table l3vpn-option_a-%d"
show_c1 = "show route table l3vpn-option_c-%d"
show_c2 = "show l2vpn connections"
show_c3 = "show l2circuit connections"
show_c4 = "show vpls connections"
show_c5 = "show vpls mac-table"

for n in range(101,106):
  print (show_c0 % n)



def check_reachabilitily(node_name, node_ip): 
   rpc_ping = dev.rpc.ping(host=node_ip, count="3", rapid=True)
   if ( rpc_ping.find('.//ping-success') is not None):
      print ("    ----> PING --> OK!")
   else:
      print ("    ----> PING --> BAD!")

def hop_count(node_name, node_ip): 
   rpc_ping = dev.rpc.ping(host=node_ip, count="3", rapid=True)
   if ( rpc_ping.find('.//ping-success') is not None ): 
      rpc_trace = dev.rpc.traceroute(host=node_ip, no_resolve=True, wait="1")
      trace_ttl = len(rpc_trace.findall('.//ttl-value'))
      print ("    ----> Traceroute No. of Hops --> %s" % trace_ttl)
   else:
      print ("    ----> Traceroute No. of Hops --> BAD!")

def check_ospf_route(node_name, node_ip): 
   rpc_ospf_rt = dev.rpc.get_route_information(protocol="ospf", table="inet.0", destination=node_ip)
   if ( rpc_ospf_rt.find('.//rt-destination') is not None):
      if ( rpc_ospf_rt.find('.//rt-destination').text == (node_ip + "/32") ):
         print ("    ----> OSPF route to Loopback --> OK!")
      else:
         print ("    ----> OSPF route to Loopback --> BAD!")

def check_isis_route(node_name, node_ip): 
   rpc_isis_rt = dev.rpc.get_route_information(protocol="isis", table="inet.0", destination=node_ip)
   if ( rpc_isis_rt.find('.//rt-destination') is not None):
      if ( rpc_isis_rt.find('.//rt-destination').text == (node_ip + "/32") ):
         print ("    ----> ISIS route to Loopback --> OK!")
      else:
         print ("    ----> ISIS route to Loopback --> BAD!")
   else:
      print ("    ----> ISIS route to Loopback --> BAD!")

def check_bgp_neighbor(node_name, node_ip): 
   rpc_bgp_ngbr = dev.rpc.get_bgp_neighbor_information(neighbor_address=node_ip)
   if ( rpc_bgp_ngbr.find('.//peer-address') is not None):
      if ( rpc_bgp_ngbr.find('.//peer-state').text == "Established" ):
         print ("    ----> BGP Session --> OK!")
      else:
         print ("    ----> BGP Session --> BAD!")
   else:
      print ("    ----> BGP Session --> BAD!")

def check_ldp_binding(node_name, node_ip): 
   rpc_ldp_rt = dev.rpc.get_route_information(protocol="ldp", table="inet.3", destination=node_ip)
   if ( rpc_ldp_rt.find('.//rt-destination') is not None):
      if ( rpc_ldp_rt.find('.//rt-destination').text == (node_ip + "/32") ):
         print ("    ----> LDP Binding to Loopback --> OK!")
      else:
         print ("    ----> LDP Binding to Loopback --> BAD!")
   else:
      print ("    ----> LDP Binding to Loopback --> BAD!")

def check_rsvp_lsp(node_name, node_ip): 
   rpc_rsvp_in_lsp = dev.rpc.get_mpls_lsp_information(ingress=True, up=True)
   lsp_dst_list = rpc_rsvp_in_lsp.findall('.//destination-address')
   lsp_dst_list_ip = list()
   if ( lsp_dst_list is not None):
      for lsp_dst_ip in lsp_dst_list:
         lsp_dst_list_ip.append(lsp_dst_ip.text)
      if ( node_ip in lsp_dst_list_ip):
         print ("    ----> RSVP LSP --> OK!")
      else:
         print ("    ----> RSVP LSP --> BAD!")
   else:
      print ("    ----> RSVP LSP --> BAD!")

def check_mpls_active(node_name, node_ip): 
   rpc_mpls_rt = dev.rpc.get_route_information(active_path=True, table="inet.3", destination=node_ip)
   if ( rpc_mpls_rt.find('.//rt-destination') is not None):
      mpls_active_protocol = rpc_mpls_rt.find('.//rt-entry/protocol-name').text
      print ("    ----> Active MPLS Path via --> %s!" % mpls_active_protocol)
   else:
      print ("    ----> Active MPLS Path --> BAD!")
      


def test_3_1(): 
   rpc_chassis_hardware = dev.rpc.get_chassis_inventory({ "format" : "text" })
   rpc_chassis_models = dev.rpc.get_chassis_inventory(clei_models=True)
   rpc_fpc_info = dev.rpc.get_fpc_information(detail=True)
   rpc_fpc_err = dev.rpc.get_fpc_error_information()
   rpc_pic_info = dev.rpc.get_pic_information()
   rpc_chassis_alarms = dev.rpc.get_alarm_information()
   rpc_sys_alarms = dev.rpc.get_system_alarm_information()
   rpc_version = dev.rpc.get_software_information()
   rpc_re_info = dev.rpc.get_route_engine_information()
   
   print (etree.tostring(rpc_chassis_hardware, encoding='unicode', pretty_print=True))


for src_node, mgmt_ip in dev_mgmt.items():

   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   
   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)
   
#   test_3_1()
   
   print ("="*(44+len(src_node)) + "\n")
   
   
   dev.close()
