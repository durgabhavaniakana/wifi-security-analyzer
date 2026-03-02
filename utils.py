def print_wifi_report(report):
    print("\n🔐 Wi-Fi Security Report\n")

    for net in report:
        print(f"SSID: {net['ssid']}")

        for issue in net["issues"]:
            print(f"  - {issue}")

        print("-" * 30)
