from adafruit_servokit import ServoKit
import time
#from feedback import angle_check
#Sets up the Servo Hat Type
kit = ServoKit(channels=16)

#Global Variables (Don't change)
servo_max_throttle = 1
servo_min_throttle = -1

#Servo list of dictionaries 
#all major data for servos is stored in here
#max and min angles are about 10 - 15 degrees above or below there maximum and minimum value
servo = [
        {'number': 0,'channel': 0, 'base throttle': 0, 'type':360, 'max voltage': 3.139, 'min voltage': 0.077, 'A2D channel': 0, 'starting angle': 60,'max angle': 130 ,'min angle':285,'shift angle': 100, 'direction':-1, 'calibrate speed': 7},
        {'number': 1,'channel': 4, 'base throttle': 0, 'type':360, 'max voltage': 3.242, 'min voltage': 0.08,  'A2D channel': 1, 'starting angle': 150,'max angle': 285 ,'min angle':65, 'shift angle': 100, 'direction':-1, 'calibrate speed': 7},
        {'number': 2,'channel': 8, 'base throttle': 0, 'type':360, 'max voltage': 3.126, 'min voltage': 0.074, 'A2D channel': 2, 'starting angle': 280,'max angle': 15 ,'min angle':190, 'shift angle': 100, 'direction':-1, 'calibrate speed': 7},
        {'number': 3,'channel': 12, 'base throttle': 0,'type':180, 'max angle': 160,'starting position': 105, 'position shift': 15, 'previous position': 0}
        ] 


def servo_speed (servo_number,new_throttle): #The function that controls the speed of a 360 servo motor
    global servo, servo_max_throttle, servo_min_throttle
    new_speed = ((servo[servo_number]['base throttle']*100) + new_throttle)/100 
    new_speed = round(new_speed,3)

    if new_speed >= servo_max_throttle: 
        kit.continuous_servo[servo[servo_number]['channel']].throttle = servo_max_throttle 
        return servo_max_throttle
    
    elif new_speed <= servo_min_throttle: 
        kit.continuous_servo[servo[servo_number]['channel']].throttle = servo_min_throttle
        return servo_min_throttle

    else:
        kit.continuous_servo[servo[servo_number]['channel']].throttle = new_speed
        return new_speed

def move_standard_servo(servo_number, servo_shift): #The function that controls the position of a standard motor
    global servo 
    if servo[servo_number]['type'] == 180:
        new_angle = (servo_shift*servo[servo_number]['position shift']) + servo[servo_number]['previous position']
        if new_angle >= servo[servo_number]['max angle']:
            new_angle = servo[servo_number]['max angle']
        elif new_angle <= 0:
            new_angle = 0
        kit.servo[servo[servo_number]['channel']].angle = new_angle
        servo[servo_number]['previous position'] = new_angle

#The code below checks the values that are defined in servo and sends an error if they are incorrect.
#Direction and calibrate speed are not checked because they were added relatively shortly before demo day

def check_channel(servo_channel): 
    if(servo_channel < 0 or servo_channel > 15): 
        raise ValueError("The servo channel number must be between 0 and 15")
    elif(not isinstance(servo_channel,int)): 
        raise ValueError("The servo channel number must be an integer")

def check_number(servo_number): 
    if(servo_number < 0 or servo_number > 3): 
        raise ValueError("The servo number must be between 0 and 3")
    elif(not isinstance(servo_number,int)): 
        raise ValueError("The servo number must be an integer")

def check_throttle(servo_throttle): 
    if(servo_throttle < -1.0 or servo_throttle > 1.0): 
        raise ValueError("The servo pre-set throttles must be between -1.0 and 1.0")

def check_type(servo_type): 
    if(servo_type != 180 and servo_type != 360): 
        raise ValueError("The servo type must be either 180 or 360")
    elif(not isinstance(servo_type,int)): 
        raise ValueError("The servo type must be an integer")

def check_max_voltage(servo_max_voltage): 
    if(servo_max_voltage > 3.3 or servo_max_voltage < 0): 
        raise ValueError("The servo max voltage must be between 0 and 3.3")

def check_min_voltage(servo_min_voltage): 
    if(servo_min_voltage > 3.3 or servo_min_voltage < 0): 
        raise ValueError("The servo min voltage must be between 0 and 3.3")

def check_A2D_channel(A2D_channel): 
    if(A2D_channel < 0 or A2D_channel > 7): 
        raise ValueError("The A2D channel must be between 0 and 7")
    elif(not isinstance(A2D_channel, int)): 
        raise ValueError("The A2D channel must be an integer")

def check_max_angle(max_angle): 
    if(max_angle < 0 or max_angle > 180): 
        raise ValueError("The starting position must be between 0 and 180")
    elif(not isinstance(max_angle,int)): 
        raise ValueError("The starting position must be an integer")

def check_360_angle(angle): 
    if(angle < 0 or angle > 360): 
        raise ValueError("The continuous servo angle must be between 0 and 360")
    elif(not isinstance(angle,int)): 
        raise ValueError("The starting position must be an integer")

def check_starting_position(servo_number, starting_position): 
    global servo 
    if(starting_position < 0 or starting_position > servo[servo_number]['max angle']): 
        raise ValueError("The starting position must be between 0 and ", servo[servo_number]['max angle'])
    elif(not isinstance(starting_position,int)): 
        raise ValueError("The starting position must be an integer")

def check_position_shift(servo_number,position_shift): 
    global servo
    if(position_shift < 0 or position_shift > (servo[servo_number]['max angle']/2)): 
        raise ValueError("The position shift must be between 0 and ",servo[servo_number]['max angle']/2)
    elif(not isinstance(position_shift,int)): 
        raise ValueError("The position shift must be an integer")


def standard_servo_setup(i): #This initializes a standard servo
    kit.servo[servo[i]['channel']].actuation_range = servo[i]['max angle'] #Sets the range of the normal servo (slot 0)
    kit.servo[servo[i]['channel']].angle = servo[i]['starting position'] 
    servo[i]['previous position'] = servo[i]['starting position'] 

def angle_check(angle): #A function designed to check an angle and put it into proper range for the sake of calculation
    return_angle = angle
    while(not (return_angle >= 0 and return_angle <= 360)):  
        if return_angle > 360: 
            return_angle = angle - 360 
        elif return_angle < 0: 
            return_angle = angle + 360
    return return_angle

def set_shift_angle(i): #This is a function that was designed to go with the calibrate function (in feedback.py). It never ended up being used
    global servo 
    max_angle = servo[i]['max angle']
    min_angle = servo[i]['min angle']
    if min_angle > max_angle: 
        max_angle = max_angle + 360 
    elif min_angle == max_angle: 
        if max_angle > 180: 
            set_angle == max_angle - 180
        elif max_angle < 180: 
            set_angle == max_angle + 180
        elif max_angle == 180:
            set_angle = 0
        else: 
            raise ValueError("Set Shift Angle function is having some problems")
        return set_angle 

    difference = 360  - (max_angle - min_angle)
    set_angle = min_angle - (difference/2)
    set_angle = angle_check(set_angle)
    set_angle = round(set_angle,0) 
    servo[i]['shift angle'] = set_angle
    return set_angle

def servo_check(): #preforms all of the set up and check servo functions defined above
    global servo
    for i in range(0,4):
        check_number(servo[i]["number"])
        check_channel(servo[i]["channel"])
        check_throttle(servo[i]["base throttle"])
        check_type(servo[i]["type"])
        if servo[i]["type"] == 360:
            check_max_voltage(servo[i]["max voltage"])
            check_min_voltage(servo[i]["min voltage"])
            check_A2D_channel(servo[i]["A2D channel"]) 
            check_360_angle(servo[i]['max angle'])
            check_360_angle(servo[i]['min angle'])
            check_360_angle(servo[i]['starting angle'])
            set_shift_angle(i)
        elif servo[i]["type"] == 180:     
            check_max_angle(servo[i]["max angle"])
            check_starting_position(i,servo[i]["starting position"])
            check_position_shift(i,servo[i]["position shift"]) 
            standard_servo_setup(i)
