
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config
from pprint import pprint

# define "dev" object from class "Device"
dev = Device(host="172.16.67.21", user="ysaied")

# apply method "open" to object "dev"
dev.open()
# apply method rpc.get_config to object "dev" after connection got established
config = dev.rpc.get_config()
# apply method "close" to object "dev"
dev.close()

### Groups XPATH
junos_groups = config.findall('.//groups')
### look for re0 group
### ./group[name=re0]
for group in junos_groups:
   print (group.find('./name').text)
   if group.find('./[name = "re0"]') is not None:
       if group.find('./system/host-name') is not None:
          print (group.find('./system/host-name').text)


