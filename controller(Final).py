from evdev import InputDevice, categorize, ecodes
import servo_data as servo_data
from servo_data import servo, servo_speed, move_standard_servo
import feedback
from feedback import feedback, find_max_and_min, calibrate
#creates object gamepad
#controller must be plugged into the top left USB port
gamepad = InputDevice('/dev/input/event2')

#Global Variables (designed to be easily changed)

left_joystick_x_threshold = [5000,-5000]
left_joystick_y_threshold = [3500,-5000]
right_joystick_x_threshold = [5000,-5000]
right_joystick_y_threshold = [5000,-5000]
joystick_division_number = 3000 

left_trigger_threshold = 40
right_trigger_threshold = 40
right_trigger_threshold2 = 250
trigger_division_number = 25
open_jaw = 1 
close_jaw = -1


#Main is defined here and referenced at the bottom
def main_control_system():

    controller_type = 0 #This is for testing purposes, there is another control schematic that is designed specifically for testing
    while(True): 
    
        if controller_type == 0:        
    
            for event in gamepad.read_loop():
   
                if event.type == 3:
            
                    absevent = categorize(event)
            
                    if absevent.event.code == 1:   #if left joystick is moved         
                        joystick_control(2,absevent.event.code ,(-1*absevent.event.value))   #A negative number is put in to flip the axis

                    elif absevent.event.code == 2: #if left trigger is moved
                        jaw_control(0,1,absevent.event.code,absevent.event.value)    
            
                    elif absevent.event.code == 5: #if right trigger is moved
                        jaw_control(0,1,absevent.event.code,absevent.event.value)   
        
 #                   elif event.code == 16 and event.value == -1: #Red Button is pressed 
 #                       feedback(0)
 #               
 #                   elif event.code == 17 and event.value == 1: #Red Button is pressed 
 #                       feedback(1)
 #           
 #                   elif event.code == 16 and event.value == 1: #Red Button is pressed 
 #                       feedback(2)


                elif event.type == 1:
             
                    if event.code == 307 and event.value == 1: #Blue Button is pressed 
                        move_standard_servo(3,-1)

                    elif event.code == 305 and event.value == 1: #Red Button is pressed 
                        move_standard_servo(3,1)

                    elif event.code == 314 and event.value == 1: #Start Button is pressed 
                        print("Calibrating...") 
                        calibrate()
                        print("Calibration Complete") 

#                    elif event.code == 315 and event.value == 1: #Start Button is pressed 
#                        print("Entering Test Mode Controls") 
#                        controller_type = 1 
#                        break
        
        
#        elif controller_type == 1: #Test Mode Controls (Commented out for Demo Day)
#
#            for event in gamepad.read_loop():
#   
#                if event.type == 3:
#            
#                    absevent = categorize(event)
#            
#                    if absevent.event.code == 1:   #if left joystick is moved         
#                        joystick_control(0,absevent.event.code ,absevent.event.value)   #servo number and axis can be easily changed
#            
#                    elif absevent.event.code == 4: #if right joystick is moved
#                        joystick_control(1,absevent.event.code,(-1*absevent.event.value))    
#
#
#                    elif absevent.event.code == 2: #if left trigger is moved
#                        trigger_control(2,absevent.event.code,absevent.event.value)    
#            
#                    elif absevent.event.code == 5: #if right trigger is moved
#                        trigger_control(3,absevent.event.code,absevent.event.value)    
#        
#                    elif event.code == 16 and event.value == -1: #Red Button is pressed 
#                        feedback(0)
#                
#                    elif event.code == 17 and event.value == 1: #Red Button is pressed 
#                        feedback(1)
#            
#                    elif event.code == 16 and event.value == 1: #Red Button is pressed 
#                        feedback(2)
#        
#                    elif event.code == 17 and event.value == -1: #Red Button is pressed 
#                        find_max_and_min(0)
#                        find_max_and_min(1)
#                        find_max_and_min(2)
#
#                elif event.type == 1:
#            
#                    if event.code == 310: #LB is pressed
#                        button_control(2,event.value)
#            
#                    elif event.code == 311 and event.value == 1: #RB is pressed
#                        move_standard_servo(3,3)
#
#                    elif event.code == 314 and event.value == 1: #Start Button is pressed 
#                        print("Calibrating...") 
#                        calibrate()
#                        print("Calibration Complete") 
#
#                    elif event.code == 315 and event.value == 1: #Start Button is pressed 
#                        print("Entering Demo Day Controls") 
#                        controller_type = 0 
#                        break

def joystick_control (servo_number,event_code,input_value): #The algorithm that determines how much a joystick moves a servo motor

    global left_joystick_x_threshold, left_joystick_y_threshold, right_joystick_x_threshold, right_joystick_y_threshold,joysitck_division_number

    if event_code == 0:
        threshold = list(left_joystick_x_threshold) 

    elif event_code == 1:
        threshold = list(left_joystick_y_threshold)
        
    elif event_code == 3:
        threshold = list(right_joystick_x_threshold)

    elif event_code == 4:
        threshold = list(right_joystick_y_threshold)

    else:
        raise ValueError("Improper event code was given to joystick_control")
    
    
    if input_value < threshold[0] and input_value > threshold[1]:
        servo_speed(servo_number,0) 
    
    elif input_value > threshold[0]: 
        x = (input_value - threshold[0])/joystick_division_number
        round(x,1) 
        servo_speed(servo_number,x)

    elif input_value < threshold[1]: 
        x = (input_value + threshold[1])/(joystick_division_number) 
        round(x,1) 
        servo_speed(servo_number,x) 


def jaw_control(servo_number_one,servo_number_two,event_code,input_value): #The function that allows for two motors to drive opposite of each other

    global servo,left_trigger_threshold, right_trigger_threshold,trigger_division_number

    if event_code == 2:
        threshold = left_trigger_threshold 

    elif event_code == 5:
        threshold = right_trigger_threshold

    else:
        raise ValueError("Improper event code was given to trigger_control")


    if input_value < threshold:
        servo_speed(servo_number_one,0) 
        servo_speed(servo_number_two,0) 

    elif input_value >= threshold: 
        x = (input_value - threshold)/trigger_division_number
        neg_x = -x + -2
        x = round(x,0) 
        neg_x = round(neg_x,0)

        if event_code == 5:
            servo_speed(servo_number_one,x)
            servo_speed(servo_number_two,neg_x)

        elif event_code == 2:
            servo_speed(servo_number_one,neg_x)
            servo_speed(servo_number_two,x)


def trigger_control(servo_number,event_code,input_value): #Used for testing only, moves a servo when the trigger threshold is exceded

    global left_trigger_threshold, right_trigger_threshold2,servo

    if event_code == 2:
        threshold = left_trigger_threshold 

        if input_value >= threshold:
            servo_speed(servo_number,15)
        else: 
            servo_speed(servo_number,0)

    elif event_code == 5:

        threshold = right_trigger_threshold2 
        if input_value >= threshold:
            move_standard_servo(3,-3)
    else:
        raise ValueError("Improper event code was given to trigger_control")


def button_control(servo_number,input_value): #Moves a Servo on a button press

    global servo

    if input_value == 1: 
        servo_speed(servo_number,-15) 
    
    elif input_value == 0:
        servo_speed(servo_number,0) 
