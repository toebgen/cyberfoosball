#!/usr/bin/env python

import data_processing
import read_double
import time
import pygame
from multiprocessing import Process, Queue

# main loop
# 2) 
# 1) initialize -> read team data

def play_sound(what_to_play):

    # Currently we create for each sound a own mixer to be
    # able to play a sound in each process. This needs to be
    # optimized
    sound_box = pygame.mixer
    sound_box.init()
    
    if what_to_play == "idle_mode_finished":
        sound_box.music.load("./sounds/fanfare3.wav")
    if what_to_play == "game_mode_finished":
        sound_box.music.load("./sounds/fanfare3.wav")
    if what_to_play == "register_mode_finished":
        sound_box.music.load("./sounds/StandardWoman/AllRegistered_Woman.wav")
    if what_to_play == "begin_game":
        sound_box.music.load("./sounds/Vader/begin.wav")
    if what_to_play == "goal_black":
        sound_box.music.load("./sounds/fanfare.wav")
    if what_to_play == "goal_silver":
        sound_box.music.load("./sounds/fanfare2.wav")
    if what_to_play == "beep":
        sound_box.music.load("./sounds/car_x.wav")

    try:
        sound_box.music.play()
        while sound_box.music.get_busy() == True:
            continue
        sound_box.quit()
    except KeyboardInterrupt:
        sound_box.quit()
        

def idle_mode_proc(dp_queue):
    try:
        while True:
            button_status = dp_queue.get()[0]
            if button_status["silver"] != "undefined":
                return;
            if button_status["black"] != "undefined":
                return;
            time.sleep(.01)
    except KeyboardInterrupt:
        return

def game_mode_proc(dp_queue):
    global score

    sound_box = pygame.mixer
    sound_box.init()
    play_sound("idle_mode_finished")

    try:
        while True:
            data_status = dp_queue.get()
            button_status = data_status[0]
            score_status = data_status[1]

            ## Update score after a goal
            if score_status["silver"] == 1:
                print "Goal Silver"
                score["silver"] += 1
                print score
                play_sound("goal_silver")
                
            if score_status["black"] == 1:
                print "Goal Black"
                score["black"] += 1
                print score
                play_sound("goal_black")
                
            ## Remove unvalid goal
            if button_status["silver"] == "single_click":
                print "Remove Goal Silver"
                print score
                if score["silver"] > 0:
                    score["silver"] -= 1
                print score

            if button_status["black"] == "single_click":
                print "Remove Goal Black"
                if score["black"] > 0:
                    score["black"] -= 1
                print score

            ## Start a new game
            if button_status["black"] == "double_click" or button_status["silver"] == "double_click":
                print "new game"
                print score
                return

            winner = evaluate_winner(score)
            if winner != "undefined":
                print "Winner is: " + winner
                print "game over"
                return
            

            time.sleep(.01)
    except KeyboardInterrupt:
        return
    except:
        return

def evaluate_winner(score):
    if score["black"] == 5 and score["silver"] <= 3:
        return "black"
    if score["silver"] == 5 and score["black"] <= 3:
        return "silver"
    if score["black"] == 7:
        return "black"
    if score["silver"] == 7:
        return "silver"
    return "undefined"

def main():
    global score
  
    dp_queue = Queue()

    play_sound("beep")

    try:
        data_reader = Process(target=data_processing.start, args=(dp_queue,))
        print "Start data processing"
        data_reader.start()
        
        while True:
            print "Idle Mode"
            idle_mode = Process(target=idle_mode_proc, args=(dp_queue,))
            idle_mode.start()
            idle_mode.join()
            print "Idle Mode finished"
            play_sound("idle_mode_finished")

            ## Register mode
            teams = read_double.init_teams()
            play_sound("register_mode_finished")

            time.sleep(1)
            
            print "Game Mode"
            # Re-Set game score
            score = {"silver" : 0, "black": 0}
            play_sound("begin_game")
            game_mode = Process(target=game_mode_proc, args=(dp_queue, ))
            game_mode.start()
            game_mode.join()
            print "Game Mode finished"

            print "Finished"

            play_sound("game_mode_finished")
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
