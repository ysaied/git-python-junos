
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
import requests


line_start = """
======================================================="""
line_end = """=======================================================
"""

dev_dic = { "KIF_VPN" : "10.117.97.56", 
   "HRZ_VPN" : "10.117.97.55", 
   "AMS_VPN" : "10.117.97.37", 
   "LON_VPN" : "10.117.97.36", 
   "Partner" : "10.117.97.39" 
   }   



show_config = """
<get-config>
  <source>
    <running/>
  </source>
  <filter type="subtree">
    <configuration>
      <system>
        <services/>
      </system>
    </configuration>
  </filter>
</get-config>
"""
rest_url = "http://{}:9080/rpc/"
rest_auth = requests.auth.HTTPBasicAuth("jnpr", "jnpr123")
rest_headers = {"Content-Type" : "application/xml", "Accept" : "text/plain"}

for node, ip in dev_dic.items():
   rest_responce = requests.post(
      rest_url.format(ip), 
      data=show_config,
      auth=rest_auth,
      headers= rest_headers
      )
   rest_responce_xml = etree.fromstring(rest_responce.content)
   telnet_conf = rest_responce_xml.find('.//telnet')
   ftp_conf = rest_responce_xml.find('.//ftp')
   print ("\n" + "="*20 + " "*2 + node + " "*2 + "="*20)
   if (telnet_conf is not None):
      print ("Telnet is configured!")
   else:
      print ("Telnet is NOT configured!")
   if (ftp_conf is not None):
      print ("FTP is configured")
   else:
      print ("FTP is NOT configured!")
   print ("="*51 + "\n")
