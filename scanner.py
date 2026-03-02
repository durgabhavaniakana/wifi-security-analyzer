import subprocess
import re
import time
import json

try:
    from mac_vendor_lookup import MacLookup
    mac_lookup = MacLookup()
    mac_lookup.update_vendors()
except:
    mac_lookup = None

KNOWN_DEVICES_FILE = "known_devices.txt"
HISTORY_FILE = "device_history.json"
PROFILE_FILE = "device_profiles.json"


def load_known_devices():
    try:
        with open(KNOWN_DEVICES_FILE, "r") as f:
            return set(f.read().splitlines())
    except:
        return set()


def save_known_device(mac):
    with open(KNOWN_DEVICES_FILE, "a") as f:
        f.write(mac + "\n")


def get_vendor(mac):
    if mac_lookup:
        try:
            return mac_lookup.lookup(mac)
        except:
            return "Unknown"
    return "Unknown"


def load_profiles():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=4)


def update_profiles(devices):
    profiles = load_profiles()

    for d in devices:
        mac = d["mac"]

        if mac not in profiles:
            profiles[mac] = {
                "vendor": d["vendor"],
                "first_seen": d["last_seen"],
                "last_seen": d["last_seen"],
                "times_seen": 1
            }
        else:
            profiles[mac]["last_seen"] = d["last_seen"]
            profiles[mac]["times_seen"] += 1

    save_profiles(profiles)


def save_history(devices):
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "devices": devices
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def scan_lan():
    try:
        output = subprocess.check_output("arp -a", shell=True).decode()

        devices = []

        for line in output.split("\n"):
            match = re.search(r"\((.*?)\) at ([0-9a-f:]+)", line)
            if match:
                device = {
                    "ip": match.group(1),
                    "mac": match.group(2),
                    "vendor": get_vendor(match.group(2)),
                    "last_seen": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                devices.append(device)

        known = load_known_devices()
        for d in devices:
            if d["mac"] not in known:
                save_known_device(d["mac"])

        save_history(devices)
        update_profiles(devices)

        return devices

    except Exception as e:
        return [{"ip": "ERROR", "mac": str(e)}]
