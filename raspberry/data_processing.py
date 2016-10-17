#!/usr/bin/env python

import RPi.GPIO as GPIO
import pygame
import time, traceback, sys
import math
import threading
import signal
from collections import namedtuple
from multiprocessing import Process

GOAL_HOME_GPIO = 29
GOAL_VISITORS_GPIO = 31

BUTTON_HOME_GPIO = 37
BUTTON_VISITORS_GPIO = 13

BUTTON_ABORT_TIME = 5.0
BUTTON_DOUBLE_PRESS_WINDOW = 1.0

PRESSED = "PRESSED"
RELEASED = "RELEASED"
NAN = float('nan')

class ButtonData:
    def __init__(self, press_time, timer, status):
        self.press_time = press_time
        self.timer = timer
        self.status = status

class TeamData:
    def __init__(self, defense_id = "undefined", offense_id = "undefined"):
        self.defense_id = defense_id
        self.offense_id = offense_id
        
class Score:
    def __init__(self, black, silver):
        self.defense_id = defense_id
        self.offense_id = offense_id


## Global data storage

button_info = {"silver" : ButtonData(NAN, None, RELEASED), 
               "black": ButtonData(NAN, None, RELEASED)}

button_status = {"silver" : "undefined", 
               "black": "undefined"}

team_info = {"silver" : TeamData(), 
             "black": TeamData()}

score_info = {"silver" : 0, 
             "black": 0}

## Accessfunctions
def reset():
    global button_info, button_status, team_info, score_info, READ_RFID
    button_info = {"silver" : ButtonData(NAN, None, RELEASED), 
                   "black": ButtonData(NAN, None, RELEASED)}
    button_status = {"silver" : "undefined", 
               "black": "undefined"}
    team_info = {"silver" : TeamData(), 
                 "black": TeamData()}
    score_info = {"silver" : 0, 
                  "black": 0}
    READ_RFID = True

def get_button_status():
    global button_status
    button = button_status.copy()
    button_status = {"silver" : "undefined", "black": "undefined"}
    return button

def get_score_info():
    global score_info
    score = score_info.copy()
    score_info = {"silver" : 0, "black": 0}
    return score

def start(q):
    global READ_RFID

    reset()
    
    try:
        print("__ read data from sensors __")
        #set up GPIO using BOARD numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Button Switch Pins
        GPIO.setup(BUTTON_HOME_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
        GPIO.add_event_detect(BUTTON_HOME_GPIO, GPIO.BOTH, callback=button, bouncetime=50)
        GPIO.setup(BUTTON_VISITORS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
        GPIO.add_event_detect(BUTTON_VISITORS_GPIO, GPIO.BOTH, callback=button, bouncetime=50)

        # IR Sensor Switch Pins - Pull Up since switch goes to ground when triggered
        GPIO.setup(GOAL_HOME_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP);
        GPIO.add_event_detect(GOAL_HOME_GPIO, GPIO.FALLING, callback=goal, bouncetime=1500)

        GPIO.setup(GOAL_VISITORS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP);
        GPIO.add_event_detect(GOAL_VISITORS_GPIO, GPIO.FALLING, callback=goal, bouncetime=1500)

        while True:
            try:
                time.sleep(.1)
                # Write output
##                print("...")
                q.put([get_button_status(), get_score_info()])
            except Exception:
                sys.stderr.write("WARNIGN: Unable to contact server to kick the dog\n")

    except KeyboardInterrupt:
        pass
    
    except:
        traceback.print_exc()
        sys.stderr.flush()

    finally:
        print("Cleanup")
        GPIO.cleanup()


def goal(channel):
    global score_info
    side = "silver" if channel == GOAL_HOME_GPIO else "black"
    score_info[side] = 1
              
def button(channel):
    side = "silver" if channel == BUTTON_HOME_GPIO else "black"
    if (GPIO.input(channel) and button_info[side].status is RELEASED):
        button_press(side)
        while (GPIO.input(channel)):
            if ((time.time() - button_info[side].press_time) >= BUTTON_ABORT_TIME):
                # excute abort
                button_info[side].press_time = NAN
                print(side + " abort!!!")
                break
    elif button_info[side].status is PRESSED:
        button_release(side)

def button_press(side):
    global button_info, button_status
##    print side + " button press"
    button_info[side].status = PRESSED
    if (math.isnan(button_info[side].press_time)):
        button_info[side].press_time = time.time()
    elif ((time.time() - button_info[side].press_time) <= BUTTON_DOUBLE_PRESS_WINDOW):
        # execute double press
        button_info[side].timer.cancel()
        button_info[side].timer = None
        button_info[side].press_time = NAN
        button_status[side] = "double_click"
        print(side + ": double click recognized")
    else:
        # this is an error state
        button_info[side].press_time = NAN
        print(side + " unknown button state!")

def button_release(side):
##    print side + ": button release"
    button_info[side].status = RELEASED
    if (not math.isnan(button_info[side].press_time)):
        # fire timer for single button press
        button_info[side].timer = threading.Timer(BUTTON_DOUBLE_PRESS_WINDOW, penalty, [side])
        button_info[side].timer.start()

def penalty(side):
    button_info[side].press_time = NAN
    button_status[side] = "single_click"
    print(side + " single click recognized!")

##def rfid_reader_proc():
##    global READ_RFID
##    global players
##    print("Card reader active!")
##
##    try:
##        # Create an object of the class MFRC522
##        MIFAREReader = MFRC522.MFRC522()
##
##        while READ_RFID:
##            # Scan for cards    
##            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
##
##            # If a card is found
##            if status == MIFAREReader.MI_OK:
##                print("Card detected")
##
##            # Get the UID of the card
##            (status,uid) = MIFAREReader.MFRC522_Anticoll()
##
##            # If we have the UID, continue
##            if status == MIFAREReader.MI_OK:
##                # If uid is unknown, send new user:
##                players.add("white_back", uid)
##                
##    except KeyboardInterrupt:
##        print("Card reader finished!")

