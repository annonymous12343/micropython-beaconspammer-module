import time
from beacon_spammer import BeaconSpammer

spammer = BeaconSpammer("ssids.txt", channel=6)

try:
    spammer.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    spammer.stop()

