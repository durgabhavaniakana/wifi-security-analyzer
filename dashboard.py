import streamlit as st
import pandas as pd
import json
import plotly.express as px

from scanner import scan_lan, load_known_devices
from analyzer import calculate_risk, generate_alerts

st.set_page_config(page_title="Network Security Analyzer", layout="wide")

# ---------------- LOGIN ----------------

def login(user, pwd):
    return user == "admin" and pwd == "admin123"

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ---------------- SIDEBAR ----------------

page = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Alerts", "History", "Profiles"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged = False
    st.rerun()

# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    st.title("📊 Network Dashboard")

    if st.button("Scan"):
        devices = scan_lan()

        if devices and devices[0]["ip"] != "ERROR":

            df = pd.DataFrame(devices)
            st.dataframe(df)

            # Export
            st.download_button(
                "Download CSV",
                df.to_csv(index=False),
                "devices.csv"
            )

            # Risk
            known = load_known_devices()
            score, risks = calculate_risk(devices, known)

            st.metric("Devices", len(devices))
            st.metric("Risk Score", score)

            for r in risks:
                st.warning(r)

            # Alerts
            alerts = generate_alerts(devices, known)
            for a in alerts:
                st.error(a)

            # Graph
            fig = px.bar(x=["Devices"], y=[len(devices)])
            st.plotly_chart(fig)

# ---------------- ALERTS ----------------

elif page == "Alerts":
    st.title("🚨 Alerts")

    try:
        alerts = json.load(open("alerts.json"))
        for a in alerts[-10:]:
            st.error(a)
    except:
        st.write("No alerts")

# ---------------- HISTORY ----------------

elif page == "History":
    st.title("📜 History")

    try:
        history = json.load(open("device_history.json"))

        st.download_button(
            "Download History",
            json.dumps(history),
            "history.json"
        )

        for h in history[-5:]:
            st.write(h["time"])
            st.dataframe(pd.DataFrame(h["devices"]))
    except:
        st.write("No history")

# ---------------- PROFILES ----------------

elif page == "Profiles":
    st.title("👤 Device Profiles")

    try:
        profiles = json.load(open("device_profiles.json"))
        for mac, data in profiles.items():
            st.write(mac, data)
    except:
        st.write("No profiles")

