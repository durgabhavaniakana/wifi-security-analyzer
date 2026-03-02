import json

ALERT_FILE = "alerts.json"


def save_alert(msg):
    try:
        with open(ALERT_FILE, "r") as f:
            alerts = json.load(f)
    except:
        alerts = []

    alerts.append(msg)

    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)


def calculate_risk(devices, known_devices):
    score = 0
    risks = []

    # Unknown devices
    for d in devices:
        if d["mac"] not in known_devices:
            score += 40
            risks.append("🚨 Unknown device detected")
            break

    # Too many devices
    if len(devices) > 5:
        score += 20
        risks.append("⚠️ Too many devices connected")

    # Duplicate MAC
    macs = [d["mac"] for d in devices]
    if len(macs) != len(set(macs)):
        score += 30
        risks.append("🚨 Possible MAC spoofing")

    return score, risks


def generate_alerts(devices, known_devices):
    alerts = []

    for d in devices:
        if d["mac"] not in known_devices:
            msg = f"🚨 Unknown device: {d['mac']}"
            alerts.append(msg)
            save_alert(msg)

    if len(devices) > 5:
        msg = "⚠️ Too many devices connected"
        alerts.append(msg)
        save_alert(msg)

    return alerts
