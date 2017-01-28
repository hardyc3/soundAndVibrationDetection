#!/usr/bin/python3

import RPi.GPIO as GPIO
import smbus
import sys
import signal


class SoundAndVibrationDetction:

    def shutdown(self):
        pass


app = None

def signal_handler(signal, frame):
    print("shutting down")
    if app != None:
        app.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print "Press Ctrl+C to shutdown"
    app = SoundAndVibrationDetection()
    app.main_loop()
