# micropython-beaconspammer-module

This is a module made for micropython which uses threading and spamms with beacon devices(wifi names) from a list.

Usage:
# main.py

import time
from beacon_spammer import BeaconSpammer

spammer = BeaconSpammer("ssids.txt", channel=6)

try:
    spammer.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    spammer.stop()
