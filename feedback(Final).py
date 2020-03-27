import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import servo_data 
from servo_data import servo, servo_speed, move_standard_servo, angle_check, kit

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

chan0 = None
chan1 = None
chan2 = None
chan3 = None
chan4 = None
chan5 = None
chan6 = None
chan7 = None

def initialize_feedback():
    global chan0,chan1,chan2,chan3,chan4,chan5,chan6,chan7,servo
    for i in range(0,4): 
        if servo[i]["type"] == 360:
            if servo[i]["A2D channel"] == 0: 
                chan0 = AnalogIn(mcp, MCP.P0)
            elif servo[i]["A2D channel"] == 1: 
                chan1 = AnalogIn(mcp, MCP.P1)
            elif servo[i]["A2D channel"] == 2: 
                chan2 = AnalogIn(mcp, MCP.P2)
            elif servo[i]["A2D channel"] == 3: 
                chan3 = AnalogIn(mcp, MCP.P3)
            elif servo[i]["A2D channel"] == 4: 
                chan4 = AnalogIn(mcp, MCP.P4)
            elif servo[i]["A2D channel"] == 5: 
                chan5 = AnalogIn(mcp, MCP.P5)
            elif servo[i]["A2D channel"] == 6: 
                chan6 = AnalogIn(mcp, MCP.P6)
            elif servo[i]["A2D channel"] == 7: 
                chan7 = AnalogIn(mcp, MCP.P7)
    
def get_SPI_channel(servo_number): 
    global chan0,chan1,chan2,chan3,chan4,chan5,chan6,chan7,servo
    if servo[servo_number]["A2D channel"] == 0: 
        return chan0
    elif servo[servo_number]["A2D channel"] == 1: 
        return chan1
    elif servo[servo_number]["A2D channel"] == 2: 
        return chan2
    elif servo[servo_number]["A2D channel"] == 3: 
        return chan3
    elif servo[servo_number]["A2D channel"] == 4: 
        return chan4
    elif servo[servo_number]["A2D channel"] == 5: 
        return chan5
    elif servo[servo_number]["A2D channel"] == 6: 
        return chan6
    elif servo[servo_number]["A2D channel"] == 7: 
        return chan7

def feedback(servo_number): #The main function used to find the positional feedback of a 360 servo motor
    global chan0,chan1,chan2,chan3,chan4,chan5,chan6,chan7,servo
    chan = get_SPI_channel(servo_number)
    maximum = 0
    minimum = 5
    sample_total = 100
    total = 0
    for i in range(0,sample_total): 
        voltage = chan.voltage
        if voltage > maximum: 
            maximum = voltage
        elif voltage < minimum: 
            minimum = voltage
        total = total + voltage
    if maximum > 3.1 and minimum < 0.1: 
        print('Angle: 0 degrees')
        return 0
    else:    
        Angle = (((total/sample_total) - servo[servo_number]["min voltage"])/(servo[servo_number]["max voltage"] - servo[servo_number]["min voltage"]))*360 
        Angle = round(Angle,0)
        print('Angle for Servo '+ str(servo_number) +' is : ' + str(Angle) + ' degrees')
        return Angle

def find_max_and_min(servo_number): #Used as a testing function, wasn't impimented in The final demonstration
    global chan0,chan1,chan2,chan3,chan4,chan5,chan6,chan7,servo
    chan = get_SPI_channel(servo_number)
    servo_speed(servo_number,7)
    maximum = 0
    minimum = 5
    run_time = 40
    t0 = time.clock()
    while(True):
        value = chan.voltage
        if value > maximum: 
            maximum = value 
        if value < minimum: 
            minimum = value 
        t1=time.clock() 
        if (t1-t0) > run_time: 
            servo[servo_number]["max voltage"] = maximum 
            servo[servo_number]["min voltage"] = minimum
            print('Maximum Voltage for Servo ',servo_number,' is ',maximum,"V")
            print('Minimum Voltage for Servo ',servo_number,' is ',minimum,"V")
            servo_speed(servo_number,0)
            break


def move_servo_position(servo_number): #Used with the calibrate function, was designed to move a 360 servo to a certain position
    global servo, servo_speed
    buff = 20
    main_speed = 0
    speed_threshold = servo[servo_number]['calibrate speed']
    direction = servo[servo_number]['direction']
    up_speed = speed_threshold*direction 
    down_speed = -speed_threshold*direction
    start_speed = 0
    cur_val = feedback(servo_number)
    goal_val = servo[servo_number]['starting angle']
    set_val = servo[servo_number]['shift angle']
    max_val = servo[servo_number]['max angle']
    min_val = servo[servo_number]['min angle']

    if goal_val <= cur_val+buff and goal_val >= cur_val - buff: 
        print(goal_val, " degrees was found!")   
        servo_speed(servo_number,0) 
        return goal_val

    elif max_val > goal_val and min_val < goal_val:
        if cur_val < goal_val: 
            print(" We landed at part 0")
            main_speed = up_speed
        else:
            main_speed = down_speed
            print(" We landed at part 1")
  
    elif max_val == goal_val or min_val == goal_val: 
        raise ValueError ("The condition of set_val == goal_val has been neglected by the programmer")

    else:
        if goal_val < max_val: 
            if cur_val < goal_val or cur_val > min_val:
                main_speed = up_speed
                print(" We landed at part 2")
            else:
                main_speed = down_speed
                print(" We landed at part 3")
        elif goal_val > min_val: 
            if cur_val < goal_val and cur_val > min_val:
                main_speed = up_speed
                print(" We landed at part 4")
            else:
                main_speed = down_speed
                print(" We landed at part 5")

  
    servo_speed(servo_number, main_speed)
    while(True):
        new_val = feedback(servo_number)
        if goal_val <= new_val+buff and goal_val >= new_val - buff: 
            servo_speed(servo_number,0) 
            print(goal_val, "degrees was found!")
            break   
    return goal_val

def calibrate(): #Designed to set the surgical tool to a default position
    global servo 
    for i in range(0,4): 
        if servo[i]['type'] == 360: 
            move_servo_position(i)
        elif servo[i]['type'] == 180:
            kit.servo[servo[i]['channel']].angle = servo[i]['starting position']
