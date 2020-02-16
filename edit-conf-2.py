
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *


line_start = """
======================================================="""
line_end = """=======================================================
"""


dev = Device(host="10.117.97.39", user="ysaied")
conf = Config(dev)

config = """
set protocols bgp export policy-4
"""

dev.open()
conf.lock()

conf.load(config, format="set")

try :
   conf.commit_check()
   if ( conf.commit_check() & (conf.diff() is not None) ):
      print ("Configuration is valid and applied")
      conf.pdiff()
      conf.commit()
   elif ( conf.commit_check() & (conf.diff() is None) ):
      print ("Configuration is already thier, nothing to be added!")
   else:
      print ("Configuration is NOT valid and rollback issued")
      conf.rollback()
except CommitError as error:
   print ("Configuration is NOT valid and rollback issued, below error raised by the router")
   print (line_start) 
   print (str(error))
   conf.rollback()
   print (line_end)
finally:
   conf.unlock()
   dev.close()

