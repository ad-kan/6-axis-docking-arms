# 6 Axis Robotic Arms

This my repository of code for synchronously controlling 2x myCobot 280 six-axis robotic arms over the local network. Commands were run on my laptop through the master script and were executed on the Linux-based arms over SSH. 

One arm is bigger than the other, so both arms used the same locally stored script but linkage lengths are different. The arms did have the in-built ability to be commanded to move to any point in a coordinate space, but this worked horribly so I came up with my own inverse kinematics logic.

I wrote this code when I worked for the SpaceTREx Laboratory at the University of Arizona.

# Useful to know

To reset default password on MyCobot 280:
1. Go to terminal and create user 'newuser': sudo adduser newuser
2. Give 'newuser' admin privileges: sudo usermod -aG sudo newuser
3. Log in to the new user and open the terminal
4. Change password of main user (username is usually 'Pi'): sudo passwd Pi
5. Done! Delete 'newuser' if you want.
The password can be used to SSH into the arm.
