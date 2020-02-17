
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
import requests

KIF-VPN = "10.117.97.56"
HRZ-VPN = "10.117.97.55"
AMS-VPN = "10.117.97.37"
LON-VPN = "10.117.97.36"
Partner = "10.117.97.39"

dev_list = [ KIF-VPN, HRZ-VPN, AMS-VPN, LON-VPN, Partner]

show_config = """
<get-config>
  <source>
    <running/>
  </source>
</get-config>
"""


for dev in dev_list:
   config = requests.post("http://{}:9080/rpc/".format(dev), 
      data=show_config,
      auth=requests.auth.HTTPBasicAuth(jnpr, jnpr123),
      header={"Content-Type: application/xml", "Accept: application/xml"}
      )
   print (config)      
