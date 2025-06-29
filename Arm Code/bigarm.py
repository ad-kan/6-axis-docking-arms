from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import os
import math
import sys
import time

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
    
def straightline(speed, z_tomove):
    armlength = [178.66,136.00,99.00,85.15,61.9,128]
    angles = mc.get_angles()
    start_displacement = displacement()

    z_tomove = z_tomove*10

    coords = mc.get_coords()
    coords[2] += z_tomove
    mc.send_coords(coords,speed,1)

mc = MyCobot(PI_PORT, 115200)
mc.power_on()

home = "/home/pi/Desktop/DockingV4"
angles = mc.get_angles()

speed = int(sys.argv[1])

if sys.argv[2] == '1':
    position = readfile("start")
    mc.send_angles(position,50)

elif sys.argv[2] == '2':
        choice = int(sys.argv[3])
        if choice == 1:
            position = readfile("start")
            mc.send_angles(position,50)
        elif choice == 2:
            position = readfile("ready")
            mc.send_angles(position,50)
        elif choice == 3:
            position = readfile("fullyextended")
            mc.send_angles(position,50)

elif sys.argv[2] == '4':
    straightline(speed, int(sys.argv[3]))

elif sys.argv[2] == '5':
    position = readfile("start")
    mc.send_angles(position,50)
    time.sleep(2)
    straightline(speed, int(sys.argv[3]))

elif sys.argv[2] == '6':
    mc.power_off()