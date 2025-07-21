# 🔐 hcxcombo

**hcxcombo** is a Python-based, all-in-one tool that automates WPA/WPA2/PMKID capture and hash extraction. It combines the functionality of [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool) and [`hcxpcapngtool`](https://github.com/ZerBea/hcxtools) into a single, streamlined workflow — perfect for wireless security assessments and red teaming.

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
- Linux (Kali, Ubuntu, Debian recommended)
- Root privileges (`sudo`)
- A wireless card that supports **monitor mode and packet injection**

---

## 📥 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/hcxcombo.git
cd hcxcombo
sudo python3 hcxcombo.py -i <your_interface>
