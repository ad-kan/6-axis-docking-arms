"""
Command to run program: 
python /home/pi/Desktop/DockingV2/Docking.py

List of commands to run if testing from terminal:
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
mc = MyCobot(PI_PORT, 115200)

Decided x displacement is -22 cm

Coords of big arm at start position: [-206.0, -83.3, 270.3, 0.0, 0, -91.75]

TO DO:
1. Update arm lengths in smallarm.py for accurate calculations
2. Adjust position of smaller arm (displacement listed above)
3. Get photos of the docking process. Should be it.
"""

import paramiko
import time

def readoutput(stdout):
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line.strip())
    return

def execute(arglist):
    args = ''
    for terms in arglist:
        args += str(terms) + ' '

    stdin, stdout, stderr = client1.exec_command('python /home/pi/Desktop/DockingV4/probe.py ' + str(speed[0]) + ' ' + args) # For big arm
    stdin, stdout, stderr = client2.exec_command('python /home/pi/Desktop/DockingV4/reciever.py ' + str(speed[1]) + ' ' + args) # For small arm
    return

client1 = paramiko.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client1.connect('192.168.1.9', username='pi', password='password')

client2 = paramiko.SSHClient()
client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client2.connect('192.168.1.71', username='pi', password='password')

print("Welcome to DockingV4\n")

stdin, stdout, stderr = client1.exec_command('python /home/pi/Desktop/DockingV4/connectiontest.py') # For big arm
readoutput(stdout)
stdin, stdout, stderr = client2.exec_command('python /home/pi/Desktop/DockingV4/connectiontest.py') # For small arm
readoutput(stdout)
print('')

home = "C:\\Users\\Aditya\\Documents\\SpaceTREx Work\\DockingV2"

global speed

speed = [10,10]
with open(home + '/Resources/speed.txt','r') as Speed:
    lines = Speed.readlines()
Speed.close()
speed[0] = int(lines[0].strip()) 
speed[1] = int(lines[1].strip())

while(1):
    command = int(input("1: Reset\n2: Quick move to position\n3: Change speed\n4: Reciever Dock\n5: Probe Dock\n6: Exit\n\nChoice: "))
    if command == 1: # Reset robots
        execute([1])

    elif command == 2: # Move robots to position
        choice = int(input("Which position? 1: Reset 2: Ready 3: Fully extended 4: Exit\nChoice: "))
        if choice <= 4:
            execute([2, choice])

    elif command == 3: # Change speed of robots
        choice = int(input("1: Both arms 2: Left Arm 3: Right Arm (R) 4: Exit\nChoice: "))
        if choice <= 3:
            new_speed = int(input("New speed (1-100 mm/s): "))            
            if choice == 1:
                speed[0] = speed[1] = new_speed
            elif choice == 2:
                speed[0] = new_speed
            elif choice == 3:
                speed[1] = new_speed
            
            with open(home + '/resources/speed.txt', 'w') as Speed:
                for term in speed:
                    Speed.write(str(term) + '\n')
            Speed.close()
        else:
            break

    elif command == 4: # Reset and dock
        z_tomove = input("Centimeters to move in z axis: ")
        execute([4, z_tomove])

    elif command == 5:
        z_tomove = input("Centimeters to move in z axis: ")
        execute([5, z_tomove])

    elif command == 0:
        execute([4, 10])

    else:
        choice = input("Do you want to power off the arms? 1: Yes 2: No\nChoice: ")
        if choice == 1:
            print("Hold the arm! You have 5 seconds before it drops.")
            time.sleep(5)
            execute([6])
        else:
            break

client1.close()
client2.close()