
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
import json
import requests

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
      if ("inactive" in telnet_conf.attrib.keys()):
         print ("Telnet is Configured but Inactive!")
      else:
         print ("Telnet is Configured & Enabled!")
   else:
      print ("Telnet is NOT Configured!")

   if (ftp_conf is not None):
      if ("inactive" in ftp_conf.attrib.keys()):
         print ("FTP is Configured but Inactive!")
      else:
         print ("FTP is Configured & Enabled!")
   else:
      print ("FTP is NOT Configured!") 

   print ("="*51 + "\n")
