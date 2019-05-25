import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

led1 = GPIO.setup(2, GPIO.OUT)
button1 = GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	if GPIO.input(14):
		print("HIGH")
	else:
		print("LOW")
	sleep(1)