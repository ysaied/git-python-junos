
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
from jnpr.junos.utils.scp import SCP
import datetime

dev_mgmt = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36" 
   } 
dev_loopback = { "KIF_VPN" : "1.0.0.11", 
   "HRZ_VPN" : "1.0.0.12", 
   "AMS_VPN" : "1.0.0.13", 
   "LON_VPN" : "1.0.0.14",
   "Partner" : "1.0.0.15"
   }  

login_username = "ysaied"

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

for src_node, mgmt_ip in dev_mgmt.items():
   dev = Device(host= mgmt_ip, user= login_username)

   dev.open()
   
   print ("\n" + "="*20 + " "*2 + src_node + " "*2 + "="*20)
   
   for dst_node, loopback_ip in dev_loopback.items():
      if ( dst_node != src_node ):
         print (dst_node)
         check_reachabilitily(dst_node, loopback_ip)
         hop_count(dst_node, loopback_ip)
         check_ospf_route(dst_node, loopback_ip)
         check_isis_route(dst_node, loopback_ip)   
         check_bgp_neighbor(dst_node, loopback_ip)
         check_ldp_binding(dst_node, loopback_ip)
         check_rsvp_lsp(dst_node, loopback_ip)
         check_mpls_active(dst_node, loopback_ip)

   time_now = datetime.datetime.now()
   time_format = str (time_now.day + "-" + time_now.month +  "-" + time_now.year +  "_" + time_now.hour +  "-" + time_now.minute)
   print (time_format)
   with SCP(dev, progress=True) as file:
      file.get("/config/juniper.conf.gz", "config-backup-18Feb2020")

   print ("="*(44+len(src_node)) + "\n")
   
   
   dev.close()
