#!/usr/bin/python3

from argparse import ArgumentParser
import ipaddress
import sys


# {0} -- IPSec IKE Pre-shared key, type string (default = l2tp@ipsec)
# {1} -- L2TP PPP Username
# {2} -- L2TP PPP Password
# {3} -- LAN Interface name, e.g. g1
# {4} -- WAN Interface name, e.g. g2

def get_args():
  parser = ArgumentParser()
  parser.add_argument('-psk', '--ipsec-pks', metavar='\b', dest='psk', default="psk@ipsec", action='store', help='IPSec Pre-shared Key')
  parser.add_argument('-u', '--ppp-username', metavar='\b', dest='ppp_uname', default="user1@ppp", action='store', help='PPP Username')
  parser.add_argument('-p', '--ppp-password', metavar='\b', dest='ppp_password', default="pass123@ppp", action='store', help='PPP Password')
  parser.add_argument('-l', '--lan-interface', metavar='\b', dest='lan_ifd', required=True, action='store', help='LAN Interface')
  parser.add_argument('-w', '--wan-interface', metavar='\b', dest='wan_ifd', required=True, action='store', help='WAN Interface')
  args = parser.parse_args()
  return args

args = get_args()
#print(args.psk, args.ppp_uname, args.ppp_password, args.lan_ifd, args.wan_ifd)

config = """

clear ip nat translation * 
conf t


interface {4}
 no ip nat outside
 no crypto map ipsec-vpn
interface {3}
 no ip nat outside
no interface Virtual-Template1
no interface Loopback0

no aaa authentication ppp default local none
no vpdn-group 1
no vpdn enable


no crypto ipsec security-association replay window-size 128
no crypto ipsec df-bit clear
no crypto isakmp keepalive

no crypto map ipsec-vpn
no crypto dynamic-map ipsec-dmap
no crypto ipsec transform-set ipsec-proposal
no crypto keyring ipesc-psk
no crypto isakmp policy 10


no route-map internet
no route-map lab
no access-list 10
no ip local pool ipsec-pool
no ip nat inside source route-map internet interface {4} overload
no ip nat inside source route-map lab interface {3} overload


crypto keyring ipesc-psk
  pre-shared-key address 0.0.0.0 0.0.0.0 key {0}

crypto isakmp policy 10
 encr aes 256
 authentication pre-share
 group 14
 lifetime 3600
 
crypto isakmp keepalive 10 3 periodic
crypto ipsec security-association replay window-size 128
crypto ipsec df-bit clear
!
crypto ipsec transform-set ipsec-proposal esp-aes 256 esp-sha-hmac 
 mode transport

crypto dynamic-map ipsec-dmap 10
 set nat demux
 set transform-set ipsec-proposal 

crypto map ipsec-vpn 10 ipsec-isakmp dynamic ipsec-dmap 

interface {4}
 crypto map ipsec-vpn

aaa new-model
aaa authentication ppp default local none

vpdn enable

vpdn-group 1
 accept-dialin
  protocol any
  virtual-template 1
 no l2tp tunnel authentication

ip local pool ipsec-pool 10.200.200.1 10.200.200.250
username {1} password {2}

interface Loopback0
 ip address 10.200.200.0 255.255.255.255

interface Virtual-Template1
 ip unnumbered Loopback0
 ip nat inside
 ip tcp adjust-mss 1387
 peer default ip address pool ipsec-pool
 ppp authentication ms-chap ms-chap-v2 chap pap callin
 ppp ipcp dns 8.8.8.8 8.8.4.4
 ip virtual-reassembly
 ip virtual-reassembly-out

interface {3}
 ip nat outside

interface {4}
 ip nat outside


ip nat inside source route-map internet interface {4} overload
ip nat inside source route-map lab interface {3} overload
access-list 10 permit 10.200.200.0 0.0.0.255

route-map internet permit 10 
 match ip address 10
 match interface {4}

route-map lab permit 10 
 match ip address 10
 match interface {3}

exit
exit
write
"""   

print (config.format(args.psk, args.ppp_uname, args.ppp_password, args.lan_ifd, args.wan_ifd))