import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

led1 = GPIO.setup(2, GPIO.OUT)
all_leds = [14, 15, 18, 23, 24, 25, 8, 7]
for led in all_leds:
	GPIO.setup(led, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	for led in all_leds:
		if GPIO.input(led):
			print(led, "HIGH")
		else:
			print(led, "LOW")
	sleep(1)