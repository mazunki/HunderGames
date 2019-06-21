import RPi.GPIO as GPIO
#import keyboard
from time import sleep
from random import randint
import signal
import threading
from tkinter import *

def close_program(signal, frame):
        global smashers
        for smasher in smashers:
                smasher.dark()
        #sleep(2)
        #GPIO.cleanup()
        exit()
signal.signal(signal.SIGINT, close_program)

IDLE_MODE = 0
GET_READY_MODE = 1
GAME_MODE = 2
GAME_OVER_MODE = 3
mode = IDLE_MODE

BOOTUP_HIGHSCORE = -1
GAME_DURATION = 60
GAME_OVER_SCORE_DURATION = 3
GAME_OVER_RESULT_DURATION = 3
DELAY_GET_READY = 1.5 # seconds


# User display
class Screen():
        def __init__(self):
                self.highscore = BOOTUP_HIGHSCORE
                self.top_message = ""
                self.middle_message = "Booting up..."
                self.bottom_message = ""

        def update_mode(self):
                global mode, smashers

                while True:
                        if mode == IDLE_MODE:
                                self.top_message = "Highscore"
                                self.middle_message = self.highscore
                                if self.middle_message == -1:
                                        self.middle_message = "Empty!"
                                self.bottom_message = "Press a button to play!"

                                frame = 0
                                while True:
                                        for smasher in smashers:
                                                if smashers.index(smasher) == frame:
                                                        smasher.light()
                                                else:
                                                        smasher.dark()

                                                if smasher.pressed_status():
                                                        mode = GAME_MODE
                                                # print(smasher.button, smasher.pressed_status(), "\t", smasher.led, smasher.lit)
                                        frame = (frame+1)%len(smashers) # around the clock
                                        # print()

                                        for smasher in smashers:
                                                if smasher.pressed_status():
                                                        mode = GET_READY_MODE
                                                        break

                                        if mode == IDLE_MODE:
                                                sleep(1)
                                        else:
                                                for smasher in smashers:
                                                        smasher.dark()
                                                break

                        elif mode == GET_READY_MODE:
                                self.top_message = "Get ready!"
                                self.middle_message = "3"
                                self.bottom_message = ""
                                sleep(DELAY_GET_READY)

                                self.top_message = "Press the buttons"
                                self.middle_message = "2"
                                self.bottom_message = "as they're lit"
                                sleep(DELAY_GET_READY)

                                self.top_message = "And don't hit"
                                self.middle_message = "1"
                                self.bottom_message = "wrong ones!"
                                sleep(DELAY_GET_READY)

                                self.top_message = "Go!"
                                self.middle_message = "0"
                                self.bottom_message = ""
                                sleep(DELAY_GET_READY/2)

                                mode = GAME_MODE

                        elif mode == GAME_MODE:
#                               global smashers
                                self.current_score = 0
                                self.time_left = GAME_DURATION
                                def metronome():
                                        while self.time_left >= 0:
                                                self.time_left -= 1
                                                sleep(1)
                                        else:
                                                return
                                counter = threading.Thread(target=metronome)
                                counter.daemon = True
                                counter.start()
                                while mode == GAME_MODE:

                                        smasher_aim = randint(0, len(smashers)-1)
                                        #print(smashers)
                                        for smasher in smashers:
                                                if smashers.index(smasher) == smasher_aim:
                                                        smasher.light()
                                                else:
                                                        smasher.dark()

                                        found_target = False
                                        while self.time_left >= 0 and not found_target:
                                                self.top_message = "Score"
                                                self.middle_message = str(self.current_score)
                                                self.bottom_message  = str(self.time_left)+"s left"
                                                
                                                for smasher in smashers:
                                                        if smasher.last_state != smasher.pressed_status():
                                                                if smasher.pressed_status():
                                                                        if smashers.index(smasher) == smasher_aim:
                                                                                self.current_score += 1
                                                                                found_target = True
                                                                        else:
                                                                                self.current_score -= 1
                                                                        self.middle_message = str(self.current_score)  # for quick updating                                                                     
                                                                        smasher.last_state = True
                                                                if not smasher.pressed_status():        
                                                                        killer = threading.Thread(target=smasher.set_off)
                                                                        killer.start()
                                        if self.time_left < 0:
                                                mode = GAME_OVER_MODE

                        elif mode == GAME_OVER_MODE:
                                self.top_message = "Time's up!"
                                self.middle_message = self.current_score
                                self.bottom_message = "total score"
                                sleep(GAME_OVER_SCORE_DURATION)

                                if self.current_score > self.highscore:
                                        self.highscore = self.current_score

                                        self.top_message = "Congratulations!"
                                        self.middle_message = "New highscore: "
                                        self.bottom_message = self.current_score

                                elif self.current_score < self.highscore:
                                        self.top_message = "Aww..."
                                        self.middle_message = "better luck"
                                        self.bottom_message = "next time"

                                else:
                                        self.top_message = "It's a tie!"
                                        self.middle_message = "You almost won!"
                                        self.bottom_message = "Try again?"

                                sleep(GAME_OVER_RESULT_DURATION)
                                mode = IDLE_MODE

        def print_to_screen(self):
                class HunderGamesWindow(Frame):
                        def __init__(app, master):
                                Frame.__init__(app, master)
                                app.master = master
                                app.fallback_geometry = "480x260"
                                master.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
                                master.bind("<Escape>", app.unfullscreen)

                                root.attributes("-fullscreen", True)

                        def unfullscreen(app, event):
                                app.master.geometry(app.fallback_geometry)
                                root.attributes("-fullscreen", False)

                root = Tk()
                window = HunderGamesWindow(master=root).pack()
                root.configure(background="black")

                self.top_message_holder = StringVar()
                self.middle_message_holder = StringVar()
                self.bottom_message_holder = StringVar()

                top_label = Label(window, textvariable=self.top_message_holder, width=root.winfo_screenwidth())
                middle_label = Label(window, textvariable=self.middle_message_holder, width=root.winfo_screenwidth())
                bottom_label = Label(window, textvariable=self.bottom_message_holder, width=root.winfo_screenwidth())
                top_label.config(font=("Courier", 36, "bold"), fg="white", bg="black")
                middle_label.config(font=("Courier", 150, "bold"), fg="white", bg="black")
                bottom_label.config(font=("Courier", 36, "bold"), fg="white", bg="black")
                top_label.pack(expand=True)
                middle_label.pack(expand=True)
                bottom_label.pack(expand=True)

                def update_labels():
                        while True:
                                self.top_message_holder.set(self.top_message)
                                self.middle_message_holder.set(self.middle_message)
                                if len(self.middle_message_holder.get()) > 6:
                                        middle_label.config(font=("Courier", 36, "bold"))
                                else:
                                        middle_label.config(font=("Courier", 150, "bold"))      
                                self.bottom_message_holder.set(self.bottom_message)
                updater = threading.Thread(target=update_labels)
                updater.daemon = True
                updater.start()

                root.mainloop()





# GPIO setup
GPIO.setmode(GPIO.BCM)
BCM_PAIRS = [   
        (25,22),  # top
        (8,10),   # blue
        (7,9),     # right
        (14,2),   # green
        (15,3),   # bottom
        (18,4),   # yellow
        (23,17),  # left
        (24,27)  # red 
] # (led, button) BCM GPIO


# Hardware interaction
class LightButton():
        def __init__(self, bcm_button, bcm_led):
                self.button = bcm_button
                self.led = bcm_led

                GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.led, GPIO.OUT)

                self.lit = False
                self.last_state = self.pressed_status()

        def light(self):
                GPIO.output(self.led, GPIO.HIGH)
                self.lit = True
        def dark(self):
                GPIO.output(self.led, GPIO.LOW)
                self.lit = False

        def pressed_status(self):
                #return keyboard.is_pressed(self.button)
                return GPIO.input(self.button)

        def set_off(self):
            sleep(0.2)
            self.last_state = False

# Add buttons to a list
smashers = list()
for pair in BCM_PAIRS:
        logical_pair = LightButton(*pair)
        smashers.append(logical_pair)


def idle_modus():
        global screen, mode

        mode = IDLE_MODE
        screen.update_mode()

if __name__ == '__main__':

        screen = Screen()
        
        printer = threading.Thread(target=screen.print_to_screen)
        printer.daemon = True
        printer.start()

        idle_modus()
