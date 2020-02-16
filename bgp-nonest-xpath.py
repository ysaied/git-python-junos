
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config
from pprint import pprint

# define "dev" object from class "Device"
dev = Device(host="10.117.97.36", user="ysaied")

# apply method "open" to object "dev"
dev.open()
# apply method rpc.get_config to object "dev" after connection got established
bgp_summary = dev.rpc.get_bgp_summary_information()
# apply method "close" to object "dev"
dev.close()

bgp_peers = config.xpath('bgp-information/bgp-peer')
#bgp_summary = config.xpath('.//protocols//export') + config.findall('.//protocols//import')

#bgp_peers_set = set()
#used_plcys_set = set()

#print (etree.tostring(plcys, encoding='unicode', pretty_print=True))
for bgp_peer in bgp_peers_set:
#   bgp_peers_set.add(bgp_peers.find('.//peer-address').text)
   print ("BGP Peer IP \"%s\" is configured" % bgp_peers.find('.//peer-address').text)
   
#for used_plcy in used_plcys:
#   used_plcys_set.add(used_plcy.text)
#   print ("Policy \"%s\" is used" % used_plcy.text)

#unsed_plcys_set = conf_plcys_set - used_plcys_set

#print ("There are %s unsed policies" % len(unsed_plcys_set))

#for unsed_plcy in unsed_plcys_set:
#   print ("Policy \"%s\" is unsed" % unsed_plcy)
