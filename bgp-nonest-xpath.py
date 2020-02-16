
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config
from pprint import pprint

dev = Device(host="10.117.97.36", user="ysaied")
unestablished_peers = 0

dev.open()
bgp_summary = dev.rpc.get_bgp_summary_information()
dev.close()

bgp_peers = bgp_summary.findall('bgp-peer')


for bgp_peer in bgp_peers:
   if ( bgp_peer.find('peer-state').text != "Established"):
      print ("BGP Peer IP \"{}\" in \"{}\" state".format(bgp_peer.find('peer-address').text,bgp_peer.find('peer-state').text))
      unestablished_peers += 1


print ("There are %s peers configured but connections are NOT Established!" % unestablished_peers)
