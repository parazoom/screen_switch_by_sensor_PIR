#!/usr/bin/env python

import sys
import time
import RPi.GPIO as io
import subprocess

io.setmode(io.BCM)
SHUTOFF_DELAY = 60 # in seconds, how long the monitor will be on until next button press or PIR detection
PIR_PIN = 4

def main():
    io.setup(PIR_PIN, io.IN)
    turned_off = False
    last_motion_time = time.time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turn_off()
        time.sleep(.1)

def turn_on():
	subprocess.call("sh /home/pi/screen_on.sh", shell=True)

def turn_off():
	subprocess.call("sh /home/pi/screen_off.sh", shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()