
#!/usr/bin/python
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.utils.config import Config



dev = Device(host="10.117.97.39", user="ysaied")
conf = Config(dev)

config = """

system {
    name-server {
        8.8.8.8;
        8.8.4.4;
    }
}   
"""

dev.open()
conf.lock()

conf.load(config, format="text")

# below is show compare
conf.pdiff()

# below is commit check
print (conf.commit_check())

# below is rollback
conf.rollback()

conf.unlock()
dev.close() 


