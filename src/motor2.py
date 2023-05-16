from time import sleep
import RPi.GPIO as GPIO

in1 = 12
in2 = 16
in3 = 20
in4 = 21

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.02

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

DIR = 26       # Direction GPIO Pin
STEP = 24      # Step GPIO Pin
CW = 1         # Clockwise Rotation
CCW = 1        # Counterclockwise Rotation
SPR = 200       # Steps per Revolution (360 / 1.8)
delay = 1/20
# delay = 1

MODE = (13, 6, 5) # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

class Motor2: 

    def __init__(self): 
        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( in1, GPIO.OUT )
        GPIO.setup( in2, GPIO.OUT )
        GPIO.setup( in3, GPIO.OUT )
        GPIO.setup( in4, GPIO.OUT )
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CW)
        GPIO.setup(MODE, GPIO.OUT)
        GPIO.output(MODE, RESOLUTION['Half'])

        # initializing
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )

    def cleanup(self):
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )
        # GPIO.cleanup()

    def run(self, angle):
        print("In motor 2 thread")

        motor_pins = [in1,in2,in3,in4]
        motor_step_counter = 0 
        step_count =  int(abs(int(angle))*4096/360) # 5.625*(1/64) per step, 4096 steps is 360°
        print("Step count is " + str(step_count))
        if (int(angle)>0):
            direction = True # True for clockwise, False for counter-clockwise
        else:
            direction = False
        print(direction)
        try:
            i = 0
            for i in range(step_count):
                for pin in range(0, len(motor_pins)):
                    GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
                if direction==True:
                    motor_step_counter = (motor_step_counter - 1) % 8
                elif direction==False:
                    motor_step_counter = (motor_step_counter + 1) % 8
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    self.cleanup()
                    exit( 1 )
            self.cleanup()
        except KeyboardInterrupt:
            self.cleanup()
            exit( 1 )
