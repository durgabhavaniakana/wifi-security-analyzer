# WiFi Security Analyzer

## Overview
WiFi Security Analyzer is a network monitoring tool built using Python. 
It scans the local network to detect connected devices and analyze potential security risks.

## Technologies Used
- Python
- Streamlit
- ARP Scanning
- Network Packet Analysis

## Features
- Detect devices connected to the network
- Monitor network activity
- Identify unknown devices
- Display results through a Streamlit dashboard

## Project Files

analyzer.py – core analysis logic  
scanner.py – network scanning module  
sniffer.py – packet monitoring  
dashboard.py – Streamlit dashboard interface  
utils.py – helper functions  
main.py – main program entry point

## How to Run

Install dependencies

pip install -r requirements.txt

Run the application

streamlit run dashboard.py
