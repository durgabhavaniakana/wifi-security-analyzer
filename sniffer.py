from scapy.all import *

known_devices = set()

def packet_callback(packet):
    if packet.haslayer(Dot11):
        mac = packet.addr2
        if mac and mac not in known_devices:
            known_devices.add(mac)
            print(f"📡 Device detected: {mac}")

def start_sniffing(interface="wlan0mon"):
    print("📡 Sniffing started...")
    sniff(iface=interface, prn=packet_callback, store=0)
