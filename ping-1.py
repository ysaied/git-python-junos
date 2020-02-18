
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
      print ("    ----> PING --> OK!")
   else:
      print ("    ----> PING --> BAD!")

def check_ospf_route(node_name, node_ip): 
   rpc_ospf_rt = dev.rpc.get_route_information(protocol="ospf", table="inet.0", destination=node_ip)
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
   rpc_bgp_ngbr = dev.rpc.get_bgp_neighbor_information(neighbor-address=node_ip)
   if ( rpc_bgp_ngbr.find('.//peer-address') is not None):
      if ( rpc_bgp_ngbr.find('.//peer-state').text == "Established" ):
         print ("    ----> BGP Session --> OK!")
      else:
         print ("    ----> BGP Session --> BAD!")
   else:
      print ("    ----> BGP Session --> BAD!")

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)
   dev.open()
   
   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)
   
   for dst_node, loopback_ip in dev_loopback.items():
      if ( dst_node != src_node ):
         print (dst_node)
         check_reachabilitily(dst_node, loopback_ip)
         check_ospf_route(dst_node, loopback_ip)
         check_isis_route(dst_node, loopback_ip)   
         


   print ("="*(44+len(src_node)) + "\n")
   
   dev.close()
