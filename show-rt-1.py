
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree

dev = Device(host="10.117.97.55", user="ysaied")

dev.open()

#show_rt = dev.rpc.get_route_information()
show_rt = dev.rpc.get_route_information(table="inet.0")
#show_rt = dev.rpc.get_route_information(table="inet.0",protocol="direct")

dev.close()

#print (etree.tostring(show_rt, encoding='unicode', pretty_print=True))

dest_rts = show_rt.findall('.//rt')

for dest_rt in dest_rts:
   print ("Destination \"{}\" via Protocol \"{}\" is active for \"{}\"".format(dest_rt.find('rt-destination').text,dest_rt.find('rt-entry/protocol-name').text,dest_rt.find('rt-entry/age').text))