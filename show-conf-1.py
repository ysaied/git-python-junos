
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json


dev = Device(host="10.117.97.39", user="ysaied")

# below XML filter
#show_interfaces = etree.XML("<configuration><interfaces/></configuration>")
# below XPATH filter
show_interfaces = ('interfaces/interface[name = "fxp0"]')

dev.open()
#below to show output in XML format
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces)

#below to show output in JUNOS Text format
show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'text', 'inherit':'inherit'})

#below to show output in XML format with explicit definition
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'xml'})

#below to show output in JSON format - need below JSON format printing 
#show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces, options={'format':'json'})

dev.close()


print (etree.tostring(show_conf_intf, encoding='unicode', pretty_print=True))

#use below to print JSON in human readable format
#show_conf_intf_json = json.dumps(show_conf_intf, indent=2)
#print (show_conf_intf_json)