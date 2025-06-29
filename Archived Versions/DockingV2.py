"""
Command to run program: 
python /home/pi/Desktop/DockingV2/Docking.py

List of commands to run if testing from terminal:
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
mc = MyCobot(PI_PORT, 115200)
"""

'''
Decided x displacement is -22 cm
'''

from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import time
import os
import math

def readfile(file):
    with open(home + '/resources/' + file + '.txt','r') as Position:
        position = Position.readlines()
    Position.close()

    pos = [0]*len(position)

    for i in range(0,len(position)):
        pos[i] = float(position[i].strip())

    return pos

def displacement():
    armlength = [178.66,136.00,99.00,85.15,61.9,128]
    angles = mc.get_angles()

    x_displacement = 0
    x_anglesum = math.radians(90) # Taking base angle as 90 because the arm is mounted perpendicularly to the frame of reference

    for x in range(1,4): # Angle of the first motor is accomodated later
        x_anglesum += math.radians(angles[x])
        x_displacement += armlength[x]*math.cos(x_anglesum)

    x_displacement += (armlength[4] + armlength[5])*math.cos(x_anglesum - math.radians(90)) # Adding the length of frame & adapter to tip, and accomodates for the 90 degree bend in the arm
    x_displacement = x_displacement*math.cos(math.radians(angles[0])) # Accomodating for the angle of the first motor
        # print(f"{displacement:.2f}\t")
    
    z_displacement = armlength[0]
    z_anglesum = math.radians(90) # Taking base angle as 90.
    for x in range(1,5): # Angle of the first motor does not change z displacement therefore it is ignored
        z_anglesum += math.radians(angles[x])
        z_displacement += armlength[x]*math.sin(z_anglesum)
        
    z_displacement += (armlength[4] + armlength[5])*math.sin(z_anglesum - math.radians(90))*math.cos(math.radians(angles[4])) # Adding the length of frame & adapter to tip, accomodating for the 90 degree bend and the effect of the 5th motor

    displacements = [x_displacement, 0, z_displacement]
    return displacements
    
def straightline(speed):
    armlength = [178.66,136.00,99.00,85.15,61.9,128]
    angles = mc.get_angles()
    start_displacement = displacement()

    print("Current x displacement from center: {:.2f} cm".format(start_displacement[0]/10))
    print("Current z displacement from center: {:.2f} cm".format(start_displacement[2]/10))

    z_tomove = input("\nCentimeters to move in z axis: ")
    z_tomove = z_tomove*10
    resolution = input("Input resolution of movement (degrees): ")
    
    z_moved = 0
    angle_1 = angles[1]
    angle_2 = angles[2]

    while(z_moved < z_tomove):
        angle_1 -= resolution
        angle_2 += resolution

        mc.send_angle(2,angle_1,speed)
        mc.send_angle(3,angle_2,speed)

        z_moved += armlength[1]*(math.sin(math.radians(90+angles[1]-resolution)) - math.sin(math.radians(90+angles[1])))
        print(z_moved)
        
        if(angle_1 < 0):
            print("Exceeded range of motion!\n")
            break

    return
 

'''
def kill(mc,speed):
    print("Press Enter to pause the movement...\n")
    input()
    print("Reached!")
    angle = mc.get_angles()
    mc.send_angles(angle,speed)
    
    return
'''

mc = MyCobot(PI_PORT, 115200)
mc.power_on()

home = "/home/pi/Desktop/DockingV2"
angles = mc.get_angles()

with open(home + '/resources/speed.txt','r') as Speed:
    speed = int(Speed.readlines()[0])
Speed.close()

print('\nWelcome to Docking.py V2\nCurrent robot position: ' + str(angles) + '\n')
while(1):
    print('---------------------------')
    command = input("1: Reset\n2: Move to position\n3: Change speed (current speed: " + str(speed) + ")\n4: Straight line motion\n5: Exit\n\nChoice: ")
    
    if command == 1:
        print("Resetting...\n")
        reset = readfile("reset")
        mc.send_angles(reset,speed)

    elif command == 2:
        while(1):
            choice = input("Which position? 1: Start 2: Ready 3: Fully extended 4: Exit\nChoice: ")
            if choice == 1:
                print("Reading file")
                position = readfile("start")
                print("Moving to position... " + str(position) + "\n")
                mc.send_angles(position,speed)
            elif choice == 2:
                print("Reading file")
                position = readfile("ready")
                print("Moving to position... " + str(position) + "\n")
                mc.send_angles(position,speed)
            elif choice == 3:
                print("Reading file")
                position = readfile("fullyextended")
                print("Moving to position... " + str(position) + "\n")
                mc.send_angles(position,speed)
            else:
                break

    elif command == 3:
        speed = input("New speed (1-100): ")
        with open(home + '/resources/speed.txt','w') as Speed:
            Speed.write(str(speed))
        Speed.close()

    elif command == 4:
        straightline(speed)

    else:
        choice = input("Do you want to power off the arm? 1: Yes 2: No\nChoice: ")
        if choice == 1:
            print("Hold the arm! You have 5 seconds before it drops.")
            time.sleep(5)
            mc.power_off()
            break
        else:
            break