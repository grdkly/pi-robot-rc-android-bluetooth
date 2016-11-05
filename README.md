# Raspberry Pi Robot - Android Remote Control (Bluetooth)#

Remote control of a Raspberry Pi robot from an Android device using Bluetooth.

## Hardware Requirements ##

The Raspberry Pi code was developed using a Raspberry Pi 3 Model B and:

- [CamJam EduKit 1 Starter](http://camjam.me/?page_id=236)
- [CamJam EduKit 3 Robotics](http://camjam.me/?page_id=1035)
- earbuds or powered speaker

The Android app was developed with [MIT App Inventor](http://appinventor.mit.edu) and should run on any Android smartphone or tablet equipped with Bluetooth.

## Software Requirements ##

Bluetooth needs to be installed and configured on the Raspberry Pi.

First, ensure the Bluetooth packages are installed:

    sudo apt-get install bluez python-bluez

It is widely reported that PNAT should be disabled, as it can prevent Bluetooth services from working correctly. This can be done by adding the following line to **/etc/bluetooth/main.conf**

    DisablePlugins = pnat

The Bluetooth daemon needs to run in compatibility mode so that the serial port service can be enabled. This can be done by adding **-C** to the `bluetoothd` line in **/etc/systemd/system/dbus-org.bluez.service**

The [Festival speech synthesiser](http://www.cstr.ed.ac.uk/projects/festival/) is used to make announcements, installed as described on [this page](http://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech).

## Installation ##

Create a directory named `/home/pi/boot` and copy the three Python scripts into it. If the scripts are installed to a different directory, the file paths within the scripts should be modified accordingly.

Call bootscript-bt.py at boot time, for example by adding this line to **cron** with `sudo crontab -e`

    @reboot python /home/pi/boot/bootscript-bt.py >/home/pi/boot/bootscript-bt.log 2>/home/pi/boot/bootscript-bt.err

## Operation ##

The script **bootscript-bt.py** starts the robot Bluetooth server and the shutdown monitor. This script is optional, but may be useful for headless operation.

The script **shutdownbutton.py** waits for a button to be pressed, then halts the Raspberry Pi. This script is optional, but may be useful for headless operation.

The Bluetooth server script **roboserver-bt.py** initialises the Raspberry Pi hardware, then starts a Bluetooth serial port service to listen for commands to control the robot from a connected device. The server returns robot status information (from the LEDs, ultrasound unit and line follower unit) encoded in [JSON](http://www.w3schools.com/json/) format.

The script may need to be adapted depending on how the hardware components are connected; in particular, when using *EduKit 1* and *EduKit 3* simultaneously, it is necessary to use different GPIO pins for *EduKit 1* than are shown in the CamJam worksheets.

The script first flashes the LEDs, then illuminates the yellow LED while waiting for a Bluetooth client to connect.

The green LED is illuminated when a Bluetooth connection is initiated by the client Android device, and the server is ready to accept commands. The supported commands can be seen by inspecting the roboserver-bt.py script.

The red LED is illuminated whenever the motors are active. The yellow LED is illuminated, accompanied by an audible warning from the buzzer, when an object is detected within 10 cm of the infrared unit.

## Android App ##

The **roboclient_bt.apk** file is a packaged Android app that should run successfully on any recent Android device equipped with Bluetooth. ‘Sideloading’ of apps needs to be enabled in order to install the client app. On most devices there is a checkbox under *Settings -> Security* that refers to installing apps from unknown or untrusted sources. Some devices will prompt the user to change the setting when an attempt is first made to sideload an app.

The Android device must be paired with the Raspberry Pi before starting the app for the first time. This can be done by making the Android device discoverable and then using `bluetoothctl` on the Raspberry Pi:

    pi@raspberrypi:~ $ bluetoothctl
    [NEW] Controller AA:AA:AA:AA:AA:AA raspberrypi [default]
    [NEW] Device BB:BB:BB:BB:BB:BB Nexus 7
    [bluetooth]# pair BB:BB:BB:BB:BB:BB
    Attempting to pair with BB:BB:BB:BB:BB:BB
    [CHG] Device BB:BB:BB:BB:BB:BB Paired: yes
    Pairing successful
    [bluetooth]# exit
    pi@raspberrypi:~ $

Alternatively, make the Raspberry Pi discoverable, and initiate pairing from the Android device:

    sudo hciconfig hci0 piscan

Start the app and click the Connect button to establish a Bluetooth connection with the Raspberry Pi. On successful connection, the status message on the app changes to show the distance detected by the ultrasound module.

Sliding the Raspberry Pi icon around on the blue canvas controls the motors, and affords full control of speed and direction. The robot stops automatically when the icon is released. The slider below the canvas controls the maximum motor speed.

The buttons at the bottom sound the buzzer, speak a preset phrase, and flash the LEDs.
 
## MIT App Inventor ##

The **roboclient_bt.aia** file contains the MIT App Inventor source from which the app is built. This file is not required to use the app.

MIT App Inventor allows Android apps to be easily built using drag-and-drop interfaces for both design and coding. Further information is available at:

[http://appinventor.mit.edu/explore/get-started.html](http://appinventor.mit.edu/explore/get-started.html)

Once an account has been created on App Inventor, roboclient_bt.aia can be imported as a new project in order to examine and modify the code. The app can then be rebuilt and downloaded locally as an APK file, or installed directly to the Android device via a QR code.
 
Gerard Kelly, November 2016
