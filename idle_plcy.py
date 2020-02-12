
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree

dev = Device(host="10.117.97.39", user="ysaied")
dev.open()
config = dev.rpc.get_config
dev.close()
plcys = config.findall('policy-options/policy-statement/name')
#print (etree.tostring(config, encoding='unicode', pretty_print=True))
for plcy in plcys:
   print (plcys.find('.//name').text)
