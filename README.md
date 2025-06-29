# cobot_docking

To reset default password on MyCobot 280:
1. Go to terminal and create user 'newuser': sudo adduser newuser
2. Give 'newuser' admin privileges: sudo usermod -aG sudo newuser
3. Log in to the new user and open the terminal
4. Change password of main user (username is usually 'Pi'): sudo passwd Pi
5. Done! Delete 'newuser' if you want.
The password can be used to SSH into the arm.
