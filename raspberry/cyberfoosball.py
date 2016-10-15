#!/usr/bin/env python

import data_processing
import time
import pygame
from multiprocessing import Process, Queue

# main loop
# 2) 
# 1) initialize -> read team data 

def play_sound(sound_mode):
    if sound_mode == "idle_mode_finished":
        pygame.mixer.music.load("./sounds/fanfare3.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def idle_mode_proc(q):
    try:
        while True:
            button_status = q.get()[0]
            if button_status["silver"] != "undefined":
                return;
            if button_status["black"] != "undefined":
                return;
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def game_mode_proc(q):
    try:
        while True:
            score_status = q.get()[1]
            print score_status
##            if button_status["silver"] != "undefined":
##                return;
##            if button_status["black"] != "undefined":
##                return;
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

def main():

    pygame.mixer.init()
    q = Queue()
    
    try:
        # add a loop to be able to return to idle mode
        
        print "Start data processing"
        data_reader = Process(target=data_processing.start, args=(q,))
        data_reader.start()

        print "Idle Mode"
        idle_mode = Process(target=idle_mode_proc, args=(q,))
        idle_mode.start()
        idle_mode.join()
        print "Idle Mode finished"
        play_sound("idle_mode_finished")

        print "Game Mode"
        game_mode = Process(target=game_mode_proc, args=(q,))
        game_mode.start()
        game_mode.join()
        print "Game Mode finished"
##        play_sound("idle_mode_finished")

        data_reader.join()
        print "Finished"
        
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
