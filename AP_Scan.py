import argparse
import scapy.all as scapy


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP Address/Addresses")
    options = parser.parse_args()

    if not options.target:
        parser.error("[!] Please specify an IP address or addresses, use --help for more info")
    return options


def scan(ip):
    arp_req_frame = scapy.ARP(pdst=ip)
    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=1, verbose=False)[0]
    result = []
    for i in range(0, len(answered_list)):
        client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
        result.append(client_dict)
    return result


def display_result(result):
    for i in result:
        print(f"{i['ip']}\t{i['mac']}")


options = get_args()
scanned_output = scan(options.target)
display_result(scanned_output)
