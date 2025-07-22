# 🔐 hcxdupcap

**hcxdupcap** is a Python-based, all-in-one tool that automates WPA/WPA2/PMKID capture, hash extraction, and optional cracking using [Hashcat](https://github.com/hashcat/hashcat). It combines the functionality of [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool), [`hcxpcapngtool`](https://github.com/ZerBea/hcxtools), and `hashcat` into a single, streamlined workflow. 

---
# Just run `sudo python3 hcxdupcap.py -i <your_interface>` 
---
## 🔔 Notice

This tool uses **dictionary-based cracking only**, using the popular `rockyou.txt` wordlist.  
If you're interested in learning how to perform advanced or manual WPA/WPA2 cracking (e.g., using different attack modes or custom rule sets), check out the official Hashcat documentation:

👉 [Hashcat Wiki – Cracking WPA/WPA2](https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2)

---

## 🧰 What You Need

Before running `hcxdupcap`, ensure you meet the following prerequisites:

### ✅ System & Tools

- Linux OS (Kali, Ubuntu, or Debian recommended)
- Python 3.x
- A wireless card that supports **monitor mode** and **packet injection**
- Install the required tools with:

```bash
sudo apt install hcxdumptool hcxtools hashcat -y
```

If installation fails or tools are missing, the script will attempt to install them automatically.  
Alternatively, you can manually clone and build from source:

- [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool)
- [`hcxpcapngtool`](https://github.com/ZerBea/hcxtools)
- [`hashcat`](https://github.com/hashcat/hashcat)

If these tools are not installed, the script will attempt to install them:
---
## ✨ Features

- 📡 Capture WPA/PMKID handshakes using `hcxdumptool`
- 🔍 Auto-process `.pcapng` using `hcxpcapngtool` in real-time
- 💾 Outputs:
  - `hash.hc22000`: Raw WPA/PMKID hashes (Hashcat-ready format)
  - `SsidHash.txt`: Annotated SSID-to-hash mapping
- ⚙ Automatic interface validation and tool installation
- 🧪 Built for red teamers, pentesters, and Wi-Fi security researchers

---

## 📦 Requirements

- Python 3.x
- Linux (Kali, Ubuntu, or Debian)
- Root privileges (`sudo`)
- Compatible Wi-Fi adapter (monitor mode + injection support)

---

## 📥 Installation

1. Clone the repo:

```bash
git clone https://github.com/tfmbot/hcxdupcap.git
cd hcxdupcap
```

2. Run the script:

```bash
sudo python3 hcxdupcap.py -i <your_interface>
```

## 🛠 Example Usage

```bash
sudo python3 hcxdupcap.py -i wlan0
```

or

```bash
sudo python3 hcxdupcap.py -i wlan0 -w name.pcapng
```

---
