#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        print "BLAH BLAH SHEEP"

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=3000)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# infinite loop
while True:
        time.sleep(1)

