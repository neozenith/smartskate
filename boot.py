import os
import storage
from adafruit_circuitplayground.express import cpx

# NOTE: If switch is closest to the B button
# This is the "no-remount" mode which allows
# savings data files.
# If the board is restarted in this mode it
# WILL DELETE the existing data file if it exists.
#
# The idea is that if you run this until the 2Mb
# storage is full, then flip the switch left to
# the A button and restart.
# This mode is safe to connect to a PC and grab
# a copy of the file.
#
# Flipping back to B side, data logging mode will
# auto clean up space on the next run.
cpx.red_led = cpx.switch
storage.remount("/", cpx.switch)

if not cpx.switch:
    try:
        os.remove("/data.csv")
    except OSError:
        pass
