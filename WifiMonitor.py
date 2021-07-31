import os
import time
import pandas
from threading import Thread
from scapy.all import *


class WifiMonitor(object):
    def __init__(self):
        self.networks = pandas.DataFrame(columns=["BSSID", "SSID", "dB", "Channel", "Crypto"])
        self.networks.set_index("BSSID", inplace=True)


    def callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            try:
                dbm_signal = packet.dBm_AntSignal
            except:
                dbm_signal = "N/A"
            stats = packet[Dot11Beacon].network_stats()
            channel = stats.get("channel")
            crypto = stats.get("crypto")
            self.networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


    def change_channel(self):
        ch = 1
        while True:
            os.system(f"iwconfig {interface} channel {ch}")
            ch = ch % 14 + 1
            time.sleep(.5)


    def print_all(self):
        while True:
            os.system("clear")
            print(self.networks)
            time.sleep(.5)


if __name__ == "__main__":
    ap = WifiMonitor()
    interface = "wlan1mon"
    printer = Thread(target=ap.print_all)
    channel_changer = Thread(target=ap.change_channel)
    printer.daemon = True
    channel_changer.daemon = True
    printer.start()
    channel_changer.start()
    sniff(prn=ap.callback, iface=interface)

