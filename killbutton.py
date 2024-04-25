from gpiozero import Button, LED
from time import sleep
import subprocess
import os
import signal
import psutil

# Name of processes to kill later
UVCPROC = "uvc-gadget"
OTHERPROC = "cam2.py"

button1 = Button(6)  # GPIO.BOARD pin 31
led1 = LED(5)        # GPIO.BOARD pin 29

button2 = Button(22)
led2 = LED(23)

button3 = Button(4)
led3 = LED(27)

# Function to handle USB camera via subprocess
def USBcamera():
	# run the configFS script including line --> uvc-gadget -c 0 uvc.0
	subprocess.run(["/bin/bash", "-c", "/home/addieschroeder/.rpi-uvc-gadget.sh &"])

def Ninacamera():
	# Run nina's code
	subprocess.run(["~/cam2.py"])

# Pass the proc you're trying to kill
def SearchAndDestroy(process_name):
	for proc in psutil.process_iter(['name']):
	#check whether the process name matches
		if proc.info['name'] == process_name:
			proc.kill()
			print(f"Killed {process_name}")

def handle_button1():
	if not led1.is_lit:
		led1.on()
		print("LED ON")
		USBcamera()  # Assuming you want to run this when the LED turns on

def handle_button3():
	led1.off()
	print("LED 1 OFF")
	led2.off()
	led3.off()
	print("All LEDs turned off")

	# Kill processes
	SearchAndDestroy(UVCPROC)
	SearchAndDestroy(OTHERPROC)


button1.when_pressed = handle_button1
button3.when_pressed = handle_button3

# This loop keeps the script running to manage the callbacks
while True:
	sleep(1)
