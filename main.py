import subprocess
from scanner import scan_wifi, scan_lan
from analyzer import analyze_wifi, analyze_lan
from utils import print_wifi_report


def check_interface():
    result = subprocess.getoutput("iwconfig")

    if "wlan0" in result:
        return "wireless"
    else:
        return "wired"


def main():
    mode = check_interface()

    if mode == "wireless":
        print("📡 Wireless mode detected\n")

        networks = scan_wifi("wlan0")

        if not networks:
            print("❌ No Wi-Fi networks found")
            return

        report = analyze_wifi(networks)
        print_wifi_report(report)

    else:
        print("🔌 Wired mode detected (eth0)\n")

        devices = scan_lan()
        analyze_lan(devices)


if __name__ == "__main__":
    main()
