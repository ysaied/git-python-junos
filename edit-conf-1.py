
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config

dev = Device(host="10.117.97.39", user="ysaied")
conf = Config(dev)

config = """
system {
    name-server {
        8.8.5.5;
        8.8.3.3;
    }
}
"""

dev.open()
conf.lock()

conf.load(config, format="text")

if ( conf.commit_check() & (conf.diff() is not None) ):
   print ("Configuration is valid and applied")
   conf.pdiff()
   conf.commit()
elif ( conf.commit_check() & (conf.diff() is None) ):
   print ("Configuration is already thier, nothing to be added!")
else:
   print ("Configuration is NOT valid and rollback issued")
   conf.rollback()

conf.unlock()
dev.close()

