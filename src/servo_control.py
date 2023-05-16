
def pen_lift(command):
    import RPi.GPIO as GPIO
    from time import sleep
    GPIO.setmode( GPIO.BCM )
    GPIO.setup(4, GPIO.OUT)
    pwm=GPIO.PWM(4, 50)
    pwm.start(0)

    if (command):
        pwm.ChangeDutyCycle(5)
        sleep(0.1)
    else: 
        pwm.ChangeDutyCycle(12)
        sleep(0.1)