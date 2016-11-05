#
# Boot script, called by cron using @reboot
#
# Gerard Kelly, November 2016
#

import time
import subprocess

# functions
def speak(phrase):
    p1 = subprocess.Popen(['echo', phrase], stdout=subprocess.PIPE)
    subprocess.Popen(['festival', '--tts'], stdin=p1.stdout).wait()

# main
speak("starting boot script")

# monitor shutdown button 
speak("press the red button to shut down")
subprocess.Popen(['sudo', 'python', '/home/pi/boot/shutdownbutton.py'])

# start the Bluetooth server for robot functions
speak("starting the bluetooth server")
logfile = open('/home/pi/boot/roboserver-bt.log', 'w')
errfile = open('/home/pi/boot/roboserver-bt.err', 'w')
subprocess.Popen(['sudo', 'python', '/home/pi/boot/roboserver-bt.py'], stdout=logfile, stderr=errfile)

# end
