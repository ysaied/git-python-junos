#!/usr/bin/python

intf_list = [ 'ge-0/0/0', 'xe-1/0/0', 'lt-0/0/10' ]

for intf in intf_list:
  if intf.startswith('ge'):
    print ("%s is 1GE interface!" % intf)
  elif intf.startswith('xe'):
    print ("%s is 10GE interface!" % intf)
  else:
    print ("%s is NOT recognized!" % intf)
print ("Thanks for using the script!")
