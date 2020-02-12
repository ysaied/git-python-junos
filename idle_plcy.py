
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config

# define "dev" object from class "Device"
dev = Device(host="10.117.97.39", user="ysaied")

# apply method "open" to object "dev"
dev.open()
# apply method rpc.get_config to object "dev" after connection got established
config = dev.rpc.get_config()
# apply method "close" to object "dev"
dev.close()

plcys = config.findall('policy-options/policy-statement/name')
print (etree.tostring(config, encoding='unicode', pretty_print=True))
#for plcy in plcys:
#   print (plcy.text)
