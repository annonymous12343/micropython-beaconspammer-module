import network
import time
import _thread
import esp

esp.osdebug(None)  # Disable verbose WiFi debug logs


class BeaconSpammer:
    def __init__(self, ssid_file: str, channel: int = 1):
        self.ssid_file = ssid_file
        self.channel = channel
        self.running = False
        self.thread_running = False
        self.wlan = network.WLAN(network.AP_IF)
        self.ssid_list = []
        self._load_ssids()

    def _load_ssids(self):
        try:
            with open(self.ssid_file, 'r') as f:
                self.ssid_list = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"[!] Failed to read SSID file: {e}")
            self.ssid_list = []

    def _generate_mac(self, index):
        base = b'\xDE\xAD\xBE'
        return base + bytes([index & 0xFF, 0x00, 0x01])

    def _broadcast_loop(self):
        self.thread_running = True
        index = 0
        self.wlan.active(True)

        while self.running and self.ssid_list:
            ssid = self.ssid_list[index % len(self.ssid_list)]
            mac = self._generate_mac(index)
            self.wlan.config(essid=ssid)
            self.wlan.config(mac=mac)
            self.wlan.config(channel=self.channel)
            print(f"[+] Broadcasting SSID: {ssid}")
            time.sleep(0.2)
            index += 1

        self.wlan.active(False)
        self.thread_running = False
        print("[*] Beacon spammer stopped.")

    def start(self):
        if not self.ssid_list:
            print("[!] No SSIDs to broadcast.")
            return
        if self.running:
            print("[!] Beacon spammer already running.")
            return

        self.running = True
        _thread.start_new_thread(self._broadcast_loop, ())

    def stop(self):
        print("[*] Stopping beacon spammer...")
        self.running = False
        while self.thread_running:
            time.sleep(0.1)  # Wait for thread to exit

