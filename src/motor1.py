from time import sleep
import RPi.GPIO as GPIO
DIR = 26       # Direction GPIO Pin
STEP = 24      # Step GPIO Pin
CW = 1         # Clockwise Rotation
CCW = 1        # Counterclockwise Rotation
SPR = 200       # Steps per Revolution (360 / 1.8)

delay  = 1/20

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR, GPIO.OUT)
# GPIO.setup(STEP, GPIO.OUT)
# GPIO.output(DIR, CW)

MODE = (13, 6, 5) # Microstep Resolution GPIO Pins
# GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

# GPIO.output(MODE, RESOLUTION['Half'])

class Motor1: 

    def __init__(self): 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CW)
        GPIO.setup(MODE, GPIO.OUT)
        GPIO.output(MODE, RESOLUTION['Half'])

    def run(self, dir, step_count):
        print("in thread for motor 1")
        GPIO.output(DIR, dir)

        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

        self.cleanup()
            

    def cleanup(self):
        # GPIO.output( in1, GPIO.LOW )
        # GPIO.output( in2, GPIO.LOW )
        # GPIO.output( in3, GPIO.LOW )
        # GPIO.output( in4, GPIO.LOW )
        GPIO.output(STEP, GPIO.LOW)
        # GPIO.cleanup()
