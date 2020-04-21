#!/usr/bin/python

# This script to generate IPSec VPN Connections on Juniper MX-Series with MS-MPC
# {0} -- IPSec Customer ID e.g. [1-99], type int
# {1} -- IPSec Customer ID + 100, type int
# {2} -- Customer IPSec Tunnel End Point IP Address, type ipv4
# {3} -- IPSec IKE Pre-shared key, type string (default = jnpr123)

Cisco_CSR1kv_1 = { "name" : "Cisco-CSR1Kv-1", "wan_ip" : "192.168.147.204", "ipsec_client_id" : "21", "ipsec_key" : "jnpr123" }
Cisco_CSR1kv_2 = { "name" : "Cisco-CSR1Kv-2", "wan_ip" : "192.168.147.211", "ipsec_client_id" : "22", "ipsec_key" : "jnpr123" }
Juniper_vSRX_1 = { "name" : "vSRX-1", "wan_ip" : "192.168.147.212", "ipsec_client_id" : "23", "ipsec_key" : "jnpr123" }
Juniper_vSRX_2 = { "name" : "vSRX-2", "wan_ip" : "192.168.147.213", "ipsec_client_id" : "24", "ipsec_key" : "jnpr123" }
PA_vFW_1 = { "name" : "PA-vFW-1", "wan_ip" : "192.168.147.69", "ipsec_client_id" : "25", "ipsec_key" : "jnpr123" }
PA_vFW_2 = { "name" : "PA-vFW-2", "wan_ip" : "192.168.147.72", "ipsec_client_id" : "26", "ipsec_key" : "jnpr123" }
VyOS_1 = { "name" : "VyOS_1", "wan_ip" : "192.168.147.74", "ipsec_client_id" : "27", "ipsec_key" : "jnpr123" }


ipsec_clients = [ Cisco_CSR1kv_1, Cisco_CSR1kv_2, Juniper_vSRX_1, Juniper_vSRX_2, PA_vFW_1, PA_vFW_2, VyOS_1 ]

config = """
delete interfaces ms-5/0/0 unit {0}
delete interfaces ms-5/0/0 unit {1}
delete services service-set ipsec-{0}
delete services ipsec-vpn rule ipsec-{0}
delete services ipsec-vpn ike policy ike-policy-ipsec-{0}

set interfaces ms-5/0/0 unit {0} description ipsec-{0}-inside
set interfaces ms-5/0/0 unit {0} family inet
set interfaces ms-5/0/0 unit {0} family inet address 3.0.{0}.1/30
set interfaces ms-5/0/0 unit {0} service-domain inside

set interfaces ms-5/0/0 unit {1} description ipsec-{0}-outside
set interfaces ms-5/0/0 unit {1} family inet
set interfaces ms-5/0/0 unit {1} service-domain outside

set services service-set ipsec-{0} next-hop-service inside-service-interface ms-5/0/0.{0}
set services service-set ipsec-{0} next-hop-service outside-service-interface ms-5/0/0.{1}
set services service-set ipsec-{0} ipsec-vpn-options local-gateway 1.0.0.11
set services service-set ipsec-{0} ipsec-vpn-rules ipsec-{0}

set services ipsec-vpn rule ipsec-{0} apply-groups ipsec-rule
set services ipsec-vpn rule ipsec-{0} term all-traffic then remote-gateway {2}
set services ipsec-vpn rule ipsec-{0} term all-traffic then dynamic ike-policy ike-policy-ipsec-{0}
set services ipsec-vpn rule ipsec-{0} term all-traffic then clear-dont-fragment-bit

set services ipsec-vpn ike policy ike-policy-ipsec-{0} description ipsec-{0}
set services ipsec-vpn ike policy ike-policy-ipsec-{0} mode main
set services ipsec-vpn ike policy ike-policy-ipsec-{0} proposals ike-proposal-default
set services ipsec-vpn ike policy ike-policy-ipsec-{0} pre-shared-key ascii-text {3}
"""

for ipsec_client in ipsec_clients:
   for key in ipsec_client.keys():
     if key == "name":
        print ("#"* 20 + ipsec_client[key] + "#"*20)
   print (config.format(ipsec_client["ipsec_client_id"], int(ipsec_client["ipsec_client_id"])+100, ipsec_client["wan_ip"], ipsec_client["ipsec_key"]))
