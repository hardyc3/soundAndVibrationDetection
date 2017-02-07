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
        GPIO.setup(SoundAndVibrationDetection.SOUND_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.needs_cleanup = True
        self.lcd = LCD(SoundAndVibrationDetection.LCD_I2C)
        self.vibration_timer = 0
        self.vibrating = False
        self.track_vibration = False
        

    def main_loop(self):
        GPIO.add_event_detect(SoundAndVibrationDetection.GREEN_BUTTON, GPIO.BOTH, callback=self.green_button_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.RED_BUTTON, GPIO.BOTH, callback=self.red_button_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.VIBRATION_SENSOR, GPIO.BOTH, callback=self.vibration_finished_handler)
        GPIO.add_event_detect(SoundAndVibrationDetection.SOUND_SENSOR, GPIO.BOTH, callback=self.sound_handler)

        while True:
            time.sleep(1)
    
    def lcd_print(self, message):
        print(message)

    def green_button_handler(self, channel):
        self.lcd_print("Monitoring Vibration")
        self.track_vibration = True

    def red_button_handler(self, channel):
        self.lcd_print("Stop Monitoring")
        self.track_vibration = False

    def vibration_finished_handler(self, channel):
        self.lcd_print("Vibration detected")
        #need to capture a start time
        #need to track time between vibrations and if within a threshold ignore the break
        #need to evaluate the time between vibrations in a different loop so we can do something if
        #the time is long enough and if the green button has been pressed
        if self.vibrating == False:
            self.vibrating = True
            self.vibration_timer = time.clock()
        else:
            self.vibrating = False
            current_time = time.clock()
            time_change = current_time - self.vibration_timer 
            self.lcd_print("vibration duration: " + str(time_change))

    def sound_handler(self, channel):
        self.lcd_print("Sound heard")

    def shutdown(self):
        if self.needs_cleanup:
            self.lcd_print("Cleaning up GPIO")
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
