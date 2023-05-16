import motor
from servo_control import pen_lift

pen_lift(1)
for i in range(5):
    motor.motor_control(0.03,0.06,1,0,15,20)
    motor.motor_control(0.04,0.005,0,0,8,15)
    motor.motor_control(0.1,0.005,0,1,8,50)
pen_lift(0)