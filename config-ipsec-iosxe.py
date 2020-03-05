#!/usr/bin/python

# This script to generate IPSec VPN Connections on Juniper MX-Series with MS-MPC
# {0} -- IPSec Customer ID e.g. [1-99], type int
# {1} -- IPSec Customer ID + 100, type int
# {2} -- Customer IPSec Tunnel End Point IP Address, type ipv4
# {3} -- IPSec IKE Pre-shared key, type string (default = jnpr123)


Cisco_CSR1kv_1 = { "name" : "Cisco-CSR1Kv-1", "wan_ip" : "192.168.147.204", "ipsec_client_id" : "21", "ipsec_key" : "jnpr123" }
Cisco_CSR1kv_2 = { "name" : "Cisco-CSR1Kv-2", "wan_ip" : "192.168.147.211", "ipsec_client_id" : "22", "ipsec_key" : "jnpr123" }

ipsec_clients = [ Cisco_CSR1kv_1, Cisco_CSR1kv_2 ]

config = """
conf t
no crypto isakmp policy {0}
no crypto keyring ike-policy-ipsec-{0}
no crypto isakmp profile ike-policy-ipsec-{0}
no crypto ipsec transform-set ipsec-default-proposal
no crypto ipsec profile ipsec-default-policy
no interface Tunnel{0}

crypto isakmp policy {0}
  encryption aes 256
  authentication pre-share
  group 5
  lifetime 86400
  hash sha
exit

crypto keyring ike-policy-ipsec-{0}
  local-address {2}
  pre-shared-key address 1.0.0.11 key {3}
exit

crypto isakmp profile ike-policy-ipsec-{0}
  local-address {2}
  match identity address 1.0.0.11
  keyring ike-policy-ipsec-{0}
exit

crypto ipsec transform-set ipsec-default-proposal esp-aes 256 esp-sha256-hmac 
  mode tunnel
exit

crypto ipsec profile ipsec-default-policy
  set pfs group5
  set security-association lifetime seconds 3600
  set transform-set ipsec-default-proposal
exit

crypto ipsec df-bit clear
crypto isakmp keepalive 10 10 on-demand
crypto ipsec security-association replay window-size 128
crypto ipsec fragmentation before-encryption


interface Tunnel{0}
  ip address 3.0.{0}.2 255.255.255.252
  ip virtual-reassembly
  tunnel source {2}
  tunnel destination 1.0.0.11
  tunnel mode ipsec ipv4
  tunnel protection ipsec profile ipsec-default-policy isakmp-profile ike-policy-ipsec-{0}
  ip tcp adjust-mss 1387 
  no shutdown
exit

exit
write

"""


for ipsec_client in ipsec_clients:
   for key in ipsec_client.keys():
     if key == "name":
        print ("#"* 20 + ipsec_client[key] + "#"*20)
   print (config.format(ipsec_client["ipsec_client_id"], int(ipsec_client["ipsec_client_id"])+100, ipsec_client["wan_ip"], ipsec_client["ipsec_key"]))
