# 🔐 hcxdupcap

**hcxdupcap** is a Python-based, all-in-one tool that automates WPA/WPA2/PMKID capture and hash extraction. It combines the functionality of [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool) and [`hcxpcapngtool`](https://github.com/ZerBea/hcxtools) into a single, streamlined workflow.

---
# Just run `sudo python3 hcxdupcap.py -i <your_interface>` 
---
## 🧰 What You Need

Before running `hcxdupcap`, ensure you meet the following prerequisites:

### ✅ System & Tools
- Linux OS (Kali, Ubuntu, or Debian recommended)
- Python 3.x
- Install the tools using apt:
  - sudo apt install hcxdumptool hcxtools -y

If this doesnt work then here are the tools
- Tools to clone:
  - [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool)
  - [`hcxpcapngtool`](https://github.com/ZerBea/hcxtools)

If these tools are not installed, the script will attempt to install them:
---

## 📦 Requirements

- Python 3.x
- Linux (Kali, Ubuntu, Debian recommended)
- Root privileges (`sudo`)
- A wireless card that supports **monitor mode and packet injection**

---

## 📥 Installation

1. Clone the repo: https://github.com/yourusername/hcxdupcap.git

```bash
git clone https://github.com/yourusername/hcxdupcap.git
cd hcxdupcap
sudo python3 hcxdupcap.py -i <your_interface>
