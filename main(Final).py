import time
import controller
from controller import main_control_system 
import servo_data
from servo_data import servo_check, servo_speed
import feedback 
from feedback import initialize_feedback 

def initialize_servos(): #Stops Servos before main
    servo_speed(0,0)
    servo_speed(1,3)
    servo_speed(2,0)

def stop_servos():  #Stops programs once the code 
    servo_speed(0,0)
    servo_speed(1,0)
    servo_speed(2,0)

def setup():
    servo_check() #checks to see if correct values were filled foe the servos
    initialize_servos() #Defined above
    initialize_feedback() #Sets up the preset conditions for the raspberry pi to recieve positonal feedback
    print('Set up Complete.')

def end_program(): 
    stop_servos() #Defined above

if __name__ == '__main__':
    setup() #Pre sets the main conroller
    try:
        main_control_system()
    except KeyboardInterrupt: 
        end_program()





