#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import signal
from LCD import LCD

class SoundAndVibrationDetection:

    GREEN_BUTTON = 40
    RED_BUTTON = 38
    VIBRATION_SENSOR = 36
    SOUND_SENSOR = 35
    LCD_I2C = 0x3f

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SoundAndVibrationDetection.GREEN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SoundAndVibrationDetection.RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SoundAndVibrationDetection.VIBRATION_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SoundAndVibrationDetection.SOUND_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.needs_cleanup = True
        self.lcd = LCD(SoundAndVibrationDetection.LCD_I2C)
        

    def main_loop(self):
        GPIO.add_event_detect(SoundAndVibrationDetection.GREEN_BUTTON, GPIO.RISING, callback=self.green_button_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.RED_BUTTON, GPIO.RISING, callback=self.red_button_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.VIBRATION_SENSOR, GPIO.FALLING, callback=self.vibration_finished_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.SOUND_SENSOR, GPIO.RISING, callback=self.sound_handler)

        while True:
            time.sleep(1)
    
    def green_button_handler(self, channel):
        print("Green button pressed")

    def red_button_handler(self, channel):
        print("Red button pressed")

    def vibration_finished_handler(self, channel):
        print("Vibration finished")

    def sound_handler(self, channel):
        print("Sound heard")

    def shutdown(self):
        if self.needs_cleanup:
            print("Cleaning up GPIO")
            GPIO.cleanup()
            self.needs_cleanup = False


app = None

def signal_handler(signal, frame):
    print("shutting down")
    if app != None:
        app.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to shutdown")
    app = SoundAndVibrationDetection()
    app.main_loop()
