#!/usr/bin/python

# This script to generate IPSec VPN Connections on Juniper MX-Series with MS-MPC
# {0} -- IPSec Customer ID e.g. [1-99], type int
# {1} -- IPSec Customer ID + 100, type int
# {2} -- Customer IPSec Tunnel End Point IP Address, type ipv4
# {3} -- IPSec IKE Pre-shared key, type string (default = jnpr123)

Juniper_vSRX_1 = { "name" : "vSRX-1", "wan_ip" : "192.168.147.212", "ipsec_client_id" : "23", "ipsec_key" : "jnpr123" }
Juniper_vSRX_2 = { "name" : "vSRX-2", "wan_ip" : "192.168.147.213", "ipsec_client_id" : "24", "ipsec_key" : "jnpr123" }

ipsec_clients = [ Juniper_vSRX_1, Juniper_vSRX_2 ]

config = """
delete security ike policy ike-policy-ipsec-{0}
delete security ike gateway ike-gateway-ipsec-{0}
delete security ipsec vpn ipsec-{0}
delete interfaces st0.{0}
delete security zones security-zone trust interfaces st0.{0}


set security ike proposal ike-proposal-default description ike-phase1-proposal
set security ike proposal ike-proposal-default authentication-method pre-shared-keys
set security ike proposal ike-proposal-default dh-group group5
set security ike proposal ike-proposal-default authentication-algorithm sha1
set security ike proposal ike-proposal-default encryption-algorithm aes-256-cbc
set security ike proposal ike-proposal-default lifetime-seconds 86400

set security ike policy ike-policy-ipsec-{0} mode main
set security ike policy ike-policy-ipsec-{0} description ipsec-{0}
set security ike policy ike-policy-ipsec-{0} proposals ike-proposal-default
set security ike policy ike-policy-ipsec-{0} pre-shared-key ascii-text {3}

set security ike gateway ike-gateway-ipsec-{0} ike-policy ike-policy-ipsec-{0}
set security ike gateway ike-gateway-ipsec-{0} address 1.0.0.11
set security ike gateway ike-gateway-ipsec-{0} dead-peer-detection interval 10
set security ike gateway ike-gateway-ipsec-{0} dead-peer-detection threshold 5
set security ike gateway ike-gateway-ipsec-{0} no-nat-traversal
set security ike gateway ike-gateway-ipsec-{0} external-interface ge-0/0/0.0
set security ike gateway ike-gateway-ipsec-{0} local-address {2}

set security ipsec proposal ipsec-default-proposal description ike-phase2-policy
set security ipsec proposal ipsec-default-proposal protocol esp
set security ipsec proposal ipsec-default-proposal authentication-algorithm hmac-sha1-96
set security ipsec proposal ipsec-default-proposal encryption-algorithm aes-256-cbc
set security ipsec proposal ipsec-default-proposal lifetime-seconds 3600

set security ipsec policy ipsec-default-policy perfect-forward-secrecy keys group5
set security ipsec policy ipsec-default-policy proposals ipsec-default-proposal

set security ipsec vpn ipsec-{0} bind-interface st0.{0}
set security ipsec vpn ipsec-{0} df-bit clear
set security ipsec vpn ipsec-{0} ike gateway ike-gateway-ipsec-{0}
set security ipsec vpn ipsec-{0} ike ipsec-policy ipsec-default-policy
set security ipsec vpn ipsec-{0} establish-tunnels immediately

set interfaces st0.{0} family inet address 3.0.{0}.2/30

set security zones security-zone trust interfaces st0.{0} host-inbound-traffic protocols bgp
set security zones security-zone trust interfaces st0.{0} host-inbound-traffic system-services ping

set security zones security-zone untrust host-inbound-traffic system-services ike
set security flow tcp-mss ipsec-vpn mss 1387
"""

for ipsec_client in ipsec_clients:
   for key in ipsec_client.keys():
     if key == "name":
        print ("#"* 20 + ipsec_client[key] + "#"*20)
   print (config.format(ipsec_client["ipsec_client_id"], int(ipsec_client["ipsec_client_id"])+100, ipsec_client["wan_ip"], ipsec_client["ipsec_key"]))
