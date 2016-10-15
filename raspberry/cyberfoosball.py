#!/usr/bin/env python

import data_processing
import time
import pygame
from multiprocessing import Process, Queue

# main loop
# 2) 
# 1) initialize -> read team data 

def play_sound(what_to_play):
    if what_to_play == "idle_mode_finished":
        pygame.mixer.music.load("./sounds/fanfare3.wav")
    if what_to_play == "game_mode_finished":
        pygame.mixer.music.load("./sounds/fanfare3.wav")
    if what_to_play == "register_mode_finished":
        pygame.mixer.music.load("./sounds/Vader/begin.wav")
    if what_to_play == "goal":
        pygame.mixer.music.load("./sounds/fanfare.wav")
    try:
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    except KeyboardInterrupt:
        pass
    except:
        pass

def idle_mode_proc(dp_queue):
    try:
        while True:
            button_status = dp_queue.get()[0]
            if button_status["silver"] != "undefined":
                return;
            if button_status["black"] != "undefined":
                return;
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def game_mode_proc(dp_queue, game_status_queue):
    try:
        while True:
            button_status = dp_queue.get()[0]
            score_status = dp_queue.get()[1]
            print score_status
##            if score_status["silver"] != game_status_queue.get()[1]["silver"]:
##                play_sound("goal")
##                return;
##            if score_status["black"] != game_status_queue.get()[1]["black"]:
##                play_sound("goal")
##                return;
            time.sleep(1)
    except KeyboardInterrupt:
        return
    except:
        return

def main():

    pygame.mixer.init()
    dp_queue = Queue()
    game_status_queue = Queue()
    
    try:
        while True:        
            # add a loop to be able to return to idle mode
            
            print "Start data processing"
            data_reader = Process(target=data_processing.start, args=(dp_queue,))
            data_reader.start()

            print "Idle Mode"
            idle_mode = Process(target=idle_mode_proc, args=(dp_queue,))
            idle_mode.start()
            idle_mode.join()
            print "Idle Mode finished"
            play_sound("idle_mode_finished")

            ## Register mode
            play_sound("register_mode_finished")
            
            print "Game Mode"
            game_mode = Process(target=game_mode_proc, args=(dp_queue, game_status_queue, ))
            game_mode.start()
            
            game_mode.join()
            print "Game Mode finished"
            play_sound("game_mode_finished")

            data_reader.join()
            print "Finished"
        
    except KeyboardInterrupt:
        pass
    except:
        pass

if __name__ == "__main__":
    main()
