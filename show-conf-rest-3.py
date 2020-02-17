
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
      <interfaces>
        <interface>
          <name>lo0</name>
            <unit>
              <name>0</name>
            </unit>
        </interface>
      </interfaces>
    </configuration>
  </filter>
</get-config>
"""
rest_url = "http://{}:9080/rpc/"
rest_auth = requests.auth.HTTPBasicAuth("jnpr", "jnpr123")
rest_headers = {"Content-Type" : "application/xml", "Accept" : "text/plain"}

def check_conf_xpath(my_feature, my_xpath):
   if (my_xpath is not None):
      if ("inactive" in my_xpath.attrib.keys()):
         print ("%s is Configured but Inactive!" % my_feature)
      else:
         print ("%s is Configured & Enabled!" % my_feature)
   else:
      print ("%s is NOT Configured!" % my_feature)

for node, ip in dev_dic.items():
   rest_responce = requests.post(
      rest_url.format(ip), 
      data=show_config,
      auth=rest_auth,
      headers= rest_headers
      )
   rest_responce_xml = etree.fromstring(rest_responce.content)
   telnet_conf = rest_responce_xml.find('.//system/service/telnet')
   ftp_conf = rest_responce_xml.find('.//system/service/ftp')
   print ("\n" + "="*20 + " "*2 + node + " "*2 + "="*20)

   check_conf_xpath("Telnet", telnet_conf)
   check_conf_xpath("FTP", ftp_conf)

   print ("="*51 + "\n")
