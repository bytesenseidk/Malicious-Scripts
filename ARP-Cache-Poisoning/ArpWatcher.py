#!/usr/bin/python

import sys, os
from scapy.all import sniff, ARP
from signal import signal, SIGINT


watcher_db = "/var/cache/watcher.txt"
ip_mac = {}

# Create log file if not exists
if not os.path.exists(watcher_db):
    tmp = open(watcher_db, "w")
    tmp.close()

# Save ARP table on shutdown
def sig_int_handler(signum, frame):
    print("Got SIGINT Signal. Saving ARP Database...")
    try:
        with open(watcher_db, "w") as file:
            for (ip, mac) in ip_mac.items():
                file.write(ip + ' ' + mac + '\n')
            
            print("Done..")
    except IOError:
        print("Cannot write to file: " + watcher_db)
        sys.exit(1)


def watch_arp(pkt):
    # Check for is-at packet (ARP Response)
    if pkt[ARP].op == 2:
        print(pkt[ARP].hwsrc + ' ' + pkt[ARP].psrc)
        # Remember new devices
        if ip_mac.get(pkt[ARP].psrc) == None:
            print(f"Found new device: {pkt[ARP].hwsrc} {pkt[ARP].psrc}")
            ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc
        
        # If device is known, but got a new IP
        elif ip_mac.get(pkt[ARP].psrc) and ip_mac[pkt[ARP].psrc] != pkt[ARP].hwsrc:
            print(f"{pkt[ARP].hwsrc} got a new IP: {pkt[ARP].psrc}\nOld IP: {ip_mac[pkt[ARP].psrc]}")
            ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc

signal(SIGINT, sig_int_handler)

if len(sys.argv) < 2:
    print(f"{sys.argv[0]}: <interface>")
    sys.exit(0)

try:
    with open(watcher_db, "r") as file:
        for line in file:
            (ip, mac) = line.split(' ')
            ip_mac[ip] = mac
except IOError:
    print(f"Cannot read file: {watcher_db}")
    sys.exit(1)

sniff(prn=watch_arp,
      filter="arp",
      iface=sys.argv[1],
      store=0)