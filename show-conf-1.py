
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json


dev = Device(host="10.117.97.39", user="ysaied")

show_interfaces = etree.XML("<configuration><interfaces/></configuration>")

dev.open()
#below to show output in XML format
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces)
#below to show output in JUNOS Text format
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'text'})
#below to show output in XML format with explicit defination
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'xml'})

show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'json'})
show_conf_intf_json = json.loads(show_conf_intf)

dev.close()

print (show_conf_intf_json)
#print (etree.tostring(show_conf_intf, encoding='unicode', pretty_print=True))

