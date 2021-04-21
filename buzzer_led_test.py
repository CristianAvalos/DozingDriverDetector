import RPi.GPIO as GPIO
from time import sleep
import sys
import signal 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledpin = 17
GPIO.setup(ledpin,GPIO.OUT)

buzzer_pin = 27
GPIO.setup(buzzer_pin,GPIO.OUT)



GPIO.output(buzzer_pin,1)
GPIO.output(ledpin,1)

sleep(10)

#GPIO.output(buzzer_pin,0)
GPIO.output(ledpin,0)
