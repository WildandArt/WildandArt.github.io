#!/usr/bin/python3
# Import required libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,12,13,15 <-- change to your pins
# GPIO17,GPIO22,GPIO23,GPIO24 <--change to your pins

ControlPin = [17,18,21,22]
# Set all pins as output
for pin in ControlPin:
  print ("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]
for pin in range(512):
    for halfstep in range(8):
        for i in range(4):
            GPIO.output(ControlPin[i],Seq[halfstep][i])
        time.sleep(0.001)
GPIO.cleanup()
