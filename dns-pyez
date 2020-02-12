
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config

dev = Device(host="10.117.97.39", user="ysaied")
dev.open()
filter = etree.XML('<configuration><system><name-server/></system></configuration>')
config = dev.rpc.get_config(filter_xml=filter)
#dev.close()
dns_servers = config.findall('system/name-server')
#print (etree.tostring(config, encoding='unicode', pretty_print=True))
for dns in dns_servers:
   print (dns.find('.//name').text)

dns_delete = '<configuration><system><name-server operation="delete"/></system></configuration>'

#dev.rpc.load_config(dns_delete)
#dev.rpc.commit_config

dev.close() 
