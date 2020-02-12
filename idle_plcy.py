
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config
from pprint import pprint

# define "dev" object from class "Device"
dev = Device(host="10.117.97.39", user="ysaied")

# apply method "open" to object "dev"
dev.open()
# apply method rpc.get_config to object "dev" after connection got established
config = dev.rpc.get_config()
# apply method "close" to object "dev"
dev.close()

conf_plcys = config.findall('.//policy-options/policy-statement')
used_plcys = config.findall('.//protocols//export') + config.findall('.//protocols//import')

conf_plcys_set = set()
used_plcys_set = set()

#print (etree.tostring(plcys, encoding='unicode', pretty_print=True))
for conf_plcy in conf_plcys:
   conf_plcys_set.add(conf_plcy.find('.//name').text)
#   print ("Policy \"%s\" is configured" % conf_plcy.find('.//name').text)
   
for used_plcy in used_plcys:
   used_plcys_set.add(used_plcy.text)
#   print ("Policy \"%s\" is used" % used_plcy.text)

unsed_plcys_set = conf_plcys_set - used_plcys_set

print ("There are %s unsed policies" % len(unsed_plcys_set))

for unsed_plcy in unsed_plcys_set:
   print ("Policy \"%s\" is unsed" % unsed_plcy)


#print (conf_plcys_set)
#print (used_plcys_set)
#print (unsed_plcys)