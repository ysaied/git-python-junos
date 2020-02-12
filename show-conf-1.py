
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree


dev = Device(host="10.117.97.39", user="ysaied")

show_interfaces = etree.XML("<configuration><interfaces/></configuration>")

dev.open()
show_conf_intf = dev.rpc.get_config(filter_xml=show_interfaces)
dev.close()

print (etree.tostring(show_conf_intf, encoding='unicode', pretty_print=True))

