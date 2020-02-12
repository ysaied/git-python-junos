
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree

dev = Device(host="10.117.97.39", user="ysaied")

dev.open()
show_rt = dev.rpc.get_route_information(table="inet.0")
dev.close()

#print (etree.tostring(show_rt, encoding='unicode', pretty_print=True))

dest_rts = show_rt.findall('.//rt')

for dest_rt in dest_rts:
   print ("Destination subnet \"%s\" is available" % dest_rt.find('.//rt-destination').text)
   print ("Destination subnet \"%s\" is available" % dest_rt.find('.//via').text)
