from time import sleep
import time
import RPi.GPIO as GPIO
import motor
import time
from servo_control import pen_lift

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 17, 22, 3=23, 27 are piTFT buttons
def gpio17_callback(channel):   #  callback for gpio17 
    print ("hit button 17")     #   set code_run with NO global
    motor.motor_control(0.03,0.06,1,0,3,20)

GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio17_callback, bouncetime=400)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 17, 22, 3=23, 27 are piTFT buttons
def gpio22_callback(channel):   #  callback for gpio17 
    print ("hit button 22")     #   set code_run with NO global
    motor.motor_control(0.04,0.005,0,0,3,15)

GPIO.add_event_detect(22, GPIO.FALLING, callback=gpio22_callback, bouncetime=400)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 17, 22, 3=23, 27 are piTFT buttons
def gpio23_callback(channel):   #  callback for gpio17 
    print ("hit button 23")     #   set code_run with NO global
    motor.motor_control(0.1,0.005,0,1,3,50)

GPIO.add_event_detect(23, GPIO.FALLING, callback=gpio23_callback, bouncetime=400)

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 17, 22, 3=23, 27 are piTFT buttons
def gpio27_callback(channel):   #  callback for gpio17 
    print ("hit button 22")     #   set code_run with NO global
    #motor2(-5)

GPIO.add_event_detect(27, GPIO.FALLING, callback=gpio27_callback, bouncetime=400)

def motor1(dir, step_count):
    GPIO.output(DIR, dir)

    delay = 1/20

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output(STEP, GPIO.LOW)
    # GPIO.cleanup()

def motor2(angle):
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
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0 ;
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
                cleanup()
                exit( 1 )
            sleep( step_sleep )
        cleanup()
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )

TIMEOUT = 60
start_time = time.time()

pen_lift(1)

while(time.time()-start_time<TIMEOUT):
    #print(time.time())
    pass

pen_lift(0)