import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
BCM_PAIRS = [	(14,2),   # green
				(15,3),   # bottom
				(18,4),   # yellow
				(23,17),  # left
				(24,22),  # red 
				(25,27),  # top
				(8,10),   # blue
				(7,9)     # right
			] # (led, button) BCM GPIO


class LightButton():
	def __init__(self, bcm_led, bcm_button):
		self.led = bcm_led
		self.button = bcm_button

		GPIO.setup(self.led, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.button, GPIO.OUT)

		self.lit = False

	def light(self):
		GPIO.output(self.led, GPIO.HIGH)
		self.lit = True
	def dark(self):
		GPIO.output(self.led, GPIO.LOW)
		self.lit = False

	def pressed_status(self):
		return GPIO.input(self.led)


smashers = list()
for pair in BCM_PAIRS:
	logical_pair = LightButton(*pair)
	smashers.append(logical_pair)

while True:
	for smasher in smashers:
		print(smasher.button, smasher.pressed_status(), "\t", smasher.led, smasher.lit)
		smasher.light()
		print()

	print()
	sleep(1)