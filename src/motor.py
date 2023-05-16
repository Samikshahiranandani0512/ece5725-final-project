
def motor_control(delay, step_sleep, dir, sig, step_count, ratio):
    from time import sleep
    import RPi.GPIO as GPIO
    
    DIR = 26       # Direction GPIO Pin
    STEP = 6     # Step GPIO Pin
    CW = 1         # Clockwise Rotation
    CCW = 1        # Counterclockwise Rotation
    SPR = 200       # Steps per Revolution (360 / 1.8)

    # delay = 1/20
    #delay  = 0.1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)
    

    MODE = (13, 6, 5) # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}

    GPIO.output(MODE, RESOLUTION['Half'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.output(MODE, RESOLUTION['Half'])

    from time import sleep
    import RPi.GPIO as GPIO

    in1 = 12
    in2 = 16
    in3 = 20
    in4 = 21

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    #step_sleep = 0.01

    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]


    # setting up
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( in1, GPIO.OUT )
    GPIO.setup( in2, GPIO.OUT )
    GPIO.setup( in3, GPIO.OUT )
    GPIO.setup( in4, GPIO.OUT )

    # initializing
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )

    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )

    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0 
    step_count0 = step_count*ratio
    print("Step count 0 is " + str(step_count0))
    step_count1 = step_count
    x = step_count0
    y = step_count1
    print(x)
    #sig = 1
    if (int(sig)>0):
        direction = True # True for clockwise, False for counter-clockwise
    else:
        direction = False
        print(direction)
    while (1):
        #print(x)
        while x>0 or y>0:
            if x>0:
                i = 0
                for i in range(ratio):
                    for pin in range(0, len(motor_pins)):
                        GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
                    if direction==True:
                        motor_step_counter = (motor_step_counter - 1) % 8
                    elif direction==False:
                        motor_step_counter = (motor_step_counter + 1) % 8
                    else: # defensive programming
                        print( "uh oh... direction should *always* be either True or False" )
                        
                        exit( 1 )
                    sleep( step_sleep )
                    x = x - 1
                print(x)
            if y>0:
                GPIO.output(DIR, dir)
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)
                y = y - 1
                print(y)
        #GPIO.cleanup()
        break
    return 0
