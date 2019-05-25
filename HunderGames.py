import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
BCM_PAIRS = [	
				(25,27),  # top
				(8,10),   # blue
				(7,9)     # right
				(14,2),   # green
				(15,3),   # bottom
				(18,4),   # yellow
				(23,17),  # left
				(24,22),  # red 
			] # (led, button) BCM GPIO


class LightButton():
	def __init__(self, bcm_button, bcm_led):
		self.button = bcm_button
		self.led = bcm_led

		GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.led, GPIO.OUT)

		self.lit = False

	def light(self):
		GPIO.output(self.led, GPIO.HIGH)
		self.lit = True
	def dark(self):
		GPIO.output(self.led, GPIO.LOW)
		self.lit = False

	def pressed_status(self):
		return GPIO.input(self.button)


smashers = list()
for pair in BCM_PAIRS:
	logical_pair = LightButton(*pair)
	smashers.append(logical_pair)

frame = 0
while True:
	for smasher in smashers:
		if smashers.index(smasher) == frame:
			smasher.light()
		else:
			smasher.dark()
		print(smasher.button, smasher.pressed_status(), "\t", smasher.led, smasher.lit)
		print()
	frame = (frame+1)%len(smashers)

	print()
	sleep(1)