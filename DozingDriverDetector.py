'''
Topic:
    CSCSE 462 Project - Microcomputer Systems
    Dozing Driver Detector
Names:
    Cristian Avalos
    Hariharan Sivakumar
Date Began:
    03/27/2021
Last Edit:
    03/27/2021
'''

### IMPORTS ###
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Setting up pins, they can easily be changed
# led 1
led1RedPin = 18
led1GreenPin = 23
led1BluePin = 24
# led 2
led2RedPin = 17
led2GreenPin = 27
led2BluePin = 22
# buzzer
buzzerPin = 4


### CLASSES ###
class LED:
    def __init__(self, redPin, greenPin, bluePin):
        self.redPin = redPin
        self.bluePin = bluePin
        self.greenPin = greenPin

    def turnRed(self):
        GPIO.output(self.redPin,1)
        GPIO.output(self.greenPin,0)
        GPIO.output(self.bluePin,0)

    def turnGreen(self):
        GPIO.output(self.redPin,0)
        GPIO.output(self.greenPin,1)
        GPIO.output(self.bluePin,0)

    def turnBlue(self):
        GPIO.output(self.redPin,0)
        GPIO.output(self.greenPin,0)
        GPIO.output(self.bluePin,1)

    def turnOff(self):
        GPIO.output(self.redPin,0)
        GPIO.output(self.greenPin,0)
        GPIO.output(self.bluePin,0)


led1 = LED(led1RedPin, led1GreenPin, led1BluePin)
led2 = LED(led2RedPin, led2GreenPin, led2BluePin)
buzzer = Buzzer(buzzerPin)

### MAIN ###
try:
    while True:
        # Do stuff
    
finally:
    GPIO.cleanup()
    cv2.destroyAllWindows()
    vs.stop()