# System (Default Lib.)
import sys
# Own library for robot control (kinematics), visualization, etc. (See manipulator.py)
import manipulator
import numpy as np
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

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()


def motor1_control(angle):
    GPIO_pins = (13, 6, 5) # Microstep Resolution MS1-MS3 -> GPIO Pin
    direction= 26       # Direction -> GPIO Pin
    step = 19      # Step -> GPIO Pin
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( 13, GPIO.OUT )
    GPIO.setup( 6, GPIO.OUT )
    GPIO.setup( 5, GPIO.OUT )
    GPIO.setup( 26, GPIO.OUT )
    GPIO.setup( 19, GPIO.OUT )
    if (int(angle)>0):
        direction = True # True for clockwise, False for counter-clockwise
    else:
        direction = False
    mymotortest.motor_go(direction, "Full" , int(abs(int(angle))*50/90),0.1, False, .01)
    GPIO.cleanup()

def motor2_control(angle):
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


def motor3_control(c):
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( 17, GPIO.OUT )
    pwm=GPIO.PWM(17, 50)
    pwm.start(0)
    if (c==1):
        pwm.ChangeDutyCycle(5)
        sleep(0.1)
    else: 
        pwm.ChangeDutyCycle(12)
        sleep(0.1)
    GPIO.cleanup()

def generate_rectangle(centroid, dimension, angle):
    """
    Description:
        A simple function to generate a path for a rectangle.

    Args:
        (1) centroid [Float Array]: Centroid of the Rectangle (x, y).
        (2) dimension [Float Array]: Dimensions (width, height).
        (3) angle [Float]: Angle (Degree) of the Rectangle.
        
    Returns:
        (1 - 2) parameter{1}, parameter{2} [Float Array]: Results of path values.

    Examples:
        generate_rectangle([1.0, 1.0], [1.0, 1.0], 0.0)
    """

    p = [[(-1)*dimension[0]/2, (-1)*dimension[0]/2, (+1)*dimension[0]/2, (+1)*dimension[0]/2, (-1)*dimension[0]/2],
         [(-1)*dimension[1]/2, (+1)*dimension[1]/2, (+1)*dimension[1]/2, (-1)*dimension[1]/2, (-1)*dimension[1]/2]]

    x = []
    y = []

    for i in range(len(p[0])):
        # Calculation position of the Rectangle
        x.append((p[0][i]*np.cos(angle * (np.pi/180)) - p[1][i]*np.sin(angle * (np.pi/180))) + centroid[0])
        y.append((p[0][i]*np.sin(angle * (np.pi/180)) + p[1][i]*np.cos(angle * (np.pi/180))) + centroid[1])

    return [x, y]

def generate_circle(centroid, radius):
    """
    Description:
        A simple function to generate a path for a circle.

    Args:
        (1) centroid [Float Array]: Centroid of the Circle (x, y).
        (1) radius [Float]: Radius of the Circle (r).
        
    Returns:
        (1 - 2) parameter{1}, parameter{2} [Float Array]: Results of path values.

    Examples:
        generate_circle([1.0, 1.0], 0.1)
    """

    # Circle ->  0 to 2*pi
    theta = np.linspace(0, 2*np.pi, 25)

    # Calculation position of the Circle
    x = radius * np.cos(theta) + centroid[0]
    y = radius * np.sin(theta) + centroid[1]

    return [x, y]

def main2():
    
    # Initial Parameters -> ABB IRB910SC 
    # Product Manual: https://search.abb.com/library/Download.aspx?DocumentID=3HAC056431-001&LanguageCode=en&DocumentPartId=&Action=Launch

    # Working range (Axis 1, Axis 2)
    axis_wr = [[-140.0, 140.0],[-150.0, 150.0]]
    # Length of Arms (Link 1, Link2)
    arm_length = [0.25, 0.3]

    # DH (Denavit-Hartenberg) parameters
    theta_0 = [0.0,0.0]
    a       = [arm_length[0], arm_length[1]]
    d       = [0.0, 0.0]
    alpha   = [0.0, 0.0]

    # Initialization of the Class (Control Manipulator)
    # Input:
    #   (1) Robot name         [String]
    #   (2) DH Parameters      [DH_parameters Structure]
    #   (3) Axis working range [Float Array]
    scara = manipulator.Control('ABB IRB 910SC (SCARA)', manipulator.DH_parameters(theta_0, a, d, alpha), axis_wr)

    """
    Example (1): 
        Description:
            Chack Target (Point) -> Check that the goal is reachable for the robot

        Cartesian Target:
            x = {'calc_type': 'IK', 'p': [0.20, 0.60], 'cfg': 0}
        Joint Target:
            x = {'calc_type': 'FK', 'theta': [0.0, 155.0], 'degree_repr': True}

        Call Function:
            res = scara.check_target(check_cartesianTarget)

    Example (2): 
        Description:
            Test Results of the kinematics.

        Forward Kinematics:
            x.forward_kinematics(1, [0.0, 0.0], 'rad')
        Inverse Kinematics:
            (a) Default Calculation method
                x.inverse_kinematics([0.35, 0.15], 1)
            (b) Jacobian Calculation method
                x.inverse_kinematics_jacobian([0.35, 0.15], [0.0, 0.0], 0.0001, 10000)
        Both kinematics to each other:
            x.forward_kinematics(0, [0.0, 45.0], 'deg')
            x.inverse_kinematics(x.p, 1)
    """
    theta0 = 0
    theta1 = 0
    trajectory_str = []
    #a, b, cfg0 = scara.generate_trajectory({'interpolation': 'joint', 'start_p': [0.3,0.3], 'target_p': [0.3,0.2], 'step': 2, 'cfg': 0})
    #print(a,b)
    #print(np.rad2deg(a),np.rad2deg(b))
    pdown = False
    x, y = generate_rectangle([0.3, 0.3], [0.1, 0.1], 0.0)

    # Initial (Start) Position
    trajectory_str.append({'interpolation': 'joint', 'start_p': [0.50, 0.0], 'target_p': [x[0], y[0]], 'step': 2, 'cfg': 0})

    # for i in range(len(x) - 1):
    #     trajectory_str.append({'interpolation': 'linear', 'start_p': [x[i], y[i]], 'target_p': [x[i + 1], y[i + 1]], 'step': 2, 'cfg': 0})

    for i in range(len(trajectory_str)):
        # Generating a trajectory from a structure
        a, b, cfg = scara.generate_trajectory(trajectory_str[i])
        print(a,b)
        print(np.rad2deg(a),np.rad2deg(b))
        for i in range(len(a)):
        
            theta0+=np.rad2deg(a[i])
            theta1+=np.rad2deg(b[i])
            motor1_control(int(np.rad2deg(a[i])))
            sleep(1)
            motor2_control(int(np.rad2deg(b[i])))
            sleep(1)
            if not(pdown):
                motor3_control(1)
                pdown=True
            sleep(1)
        print (theta0,theta1)
        if (theta0>140 or theta1>140):
            break
        sleep(2)

    sleep(5)
    motor3_control(0)
    pdown=False
    motor1_control(-theta0)
    sleep(1)
    motor2_control(-theta1)
    sleep(1)

def main(): 
    # sleep(5)
    # print("motor 3 control 0")
    # motor3_control(1)
    # pdown=False
    # print("motor 1 control 10")
    motor1_control(-50)
    sleep(10)
    # print("motor 2 control 10")
    # motor2_control(-50)
    # sleep(1)

if __name__ == '__main__':
    sys.exit(main())