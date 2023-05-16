import motor
from servo_control import pen_lift
for i in range(1):
    pen_lift(1)
    motor.motor_control(0.01,0.04,1,0,7,40)
    motor.motor_control(0.08,0.005,0,0,8,20)
    motor.motor_control(0.08,0.02,0,1,10,40)
    motor.motor_control(0.02,0.01,1,1,10,15)
    pen_lift(0)