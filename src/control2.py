from time import sleep
import RPi.GPIO as GPIO
import motor1
import motor2
from threading import Thread

#sleep(3)
# motor1.motor1(0, 20)
print("second")




# motor1(0, 25)
# print("done both")

# motor2(-40)


# motor1(1, 30)
# print("done one way")


# motor2(25)



#Create Class
class_motor1 = motor1.Motor1()
#Create Thread
motor1thread = Thread(target=class_motor1.run(0, 50)) 
#Start Thread 
motor1thread.start()



Exit = False #Exit flag
while Exit==False:
    cycle = cycle + 0.1 
    print("Main Program increases cycle+0.1 - " + str(cycle))
    time.sleep(1) #One second delay
    if (cycle > 5): Exit = True #Exit Program



