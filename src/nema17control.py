from time import sleep
import RPi.GPIO as GPIO
import sys
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (13, 6, 5) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 26       # Direction -> GPIO Pin
step = 19      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
if (int(sys.argv[1])>0):
    direction = True # True for clockwise, False for counter-clockwise
else:
    direction = False
mymotortest.motor_go(direction, "Full" , int(abs(int(sys.argv[1]))*50/90),0.1, False, .01)
GPIO.cleanup()
print("Rotating Clockwise")
