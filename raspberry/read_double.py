#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import signal
import pygame
import hashlib
import data_processing
from rfid_rc522 import MFRC522

BLACK_TEAM_CHANNEL = 22
SILVER_TEAM_CHANNEL = 18

DEFENSE_REGISTER = "defense_register"
STRIKER_REGISTER = "striker_register"

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
##    print "Ctrl+C captured, ending read."
    continue_reading = False

def play_sound(what_to_play):
    if what_to_play == BLACK_TEAM_CHANNEL:
        pygame.mixer.music.load("./sounds/beep-black.wav")
    elif what_to_play == SILVER_TEAM_CHANNEL:
        pygame.mixer.music.load("./sounds/beep-silver.wav")
    elif what_to_play == DEFENSE_REGISTER:
        pygame.mixer.music.load("./sounds/StandardWoman/DefendersReg_Woman.wav")
    elif what_to_play == STRIKER_REGISTER:
        pygame.mixer.music.load("./sounds/StandardWoman/StrikersReg_Woman.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def get_player_id(reader, rfid_board_id):

    # Scan for cards
    (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    # If a card is found
    if status == reader.MI_OK:
        if rfid_board_id == BLACK_TEAM_CHANNEL:
            print "Black team card detected"
        elif rfid_board_id == SILVER_TEAM_CHANNEL:
            print "Silver team card detected"

    # Get the UID of the card
    (status,uid) = reader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == reader.MI_OK:
        if rfid_board_id == BLACK_TEAM_CHANNEL:
            play_sound(BLACK_TEAM_CHANNEL)
        elif rfid_board_id == SILVER_TEAM_CHANNEL:
            play_sound(SILVER_TEAM_CHANNEL)
        return uid
    
##        # This is the default key for authentication
##        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
##        
##        # Select the scanned tag
##        reader.MFRC522_SelectTag(uid)
##
##        # Authenticate
##        status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, key, uid)
##
##        # Check if authenticated
##        if status == reader.MI_OK:
##            reader.MFRC522_Read(8)
##            reader.MFRC522_StopCrypto1()
##        else:
##            print "Authentication error"


def register_two_players():

    black_player_registered = False
    silver_player_registered = False
    
    # Welcome message
##    print "Press Ctrl-C to stop."

    # Hook the SIGINT
##    signal.signal(signal.SIGINT, end_read)
    
    # Create an object of the class MFRC522
    MIFAREReader1 = MFRC522.MFRC522(dev='/dev/spidev0.0', rfid_pin=BLACK_TEAM_CHANNEL)
    MIFAREReader2 = MFRC522.MFRC522(dev='/dev/spidev0.1', rfid_pin=SILVER_TEAM_CHANNEL)
    try:
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            
            # Init black team card reader
            MIFAREReader1.init_rfid_board(dev='/dev/spidev0.0', rfid_pin=BLACK_TEAM_CHANNEL)

            if black_player_registered == False:
                black_team_uid = get_player_id(MIFAREReader1, BLACK_TEAM_CHANNEL)
                if black_team_uid is not None:
                    print "Black team card read UID: "+str(black_team_uid[0])+","+str(black_team_uid[1])+","+str(black_team_uid[2])+","+str(black_team_uid[3])
                    black_player_registered = True
            
            time.sleep(0.1)
           
            # Init silver team card reader
            MIFAREReader2.init_rfid_board(dev='/dev/spidev0.1', rfid_pin=SILVER_TEAM_CHANNEL)

            if silver_player_registered == False:
                silver_team_uid = get_player_id(MIFAREReader2, SILVER_TEAM_CHANNEL)
                if silver_team_uid is not None:
                    print "Silver team card read UID: "+str(silver_team_uid[0])+","+str(silver_team_uid[1])+","+str(silver_team_uid[2])+","+str(silver_team_uid[3])
                    silver_player_registered = True

            if black_player_registered == True and silver_player_registered == True:
                black_team_player_str  = str(black_team_uid[0])+str(black_team_uid[1])+str(black_team_uid[2])+str(black_team_uid[3])
                silver_team_player_str = str(silver_team_uid[0])+str(silver_team_uid[1])+str(silver_team_uid[2])+str(silver_team_uid[3])
                return {'black_team_player': black_team_player_str, 'silver_team_player': silver_team_player_str}
    except KeyboardInterrupt:
        return 


def init_teams(hash_output=True):

    # Initialize audio player
    pygame.mixer.init()

    play_sound(DEFENSE_REGISTER)
    defenders_id = register_two_players()

    print "Defenders: "+str(defenders_id['black_team_player'])+" and "+str(defenders_id['silver_team_player'])
    
    play_sound(STRIKER_REGISTER)
    strikers_id = register_two_players()
    print "Strikers: "+str(strikers_id['black_team_player'])+" and "+str(strikers_id['silver_team_player'])

    if (hash_output):
        black_team = data_processing.TeamData(hashlib.md5(str(defenders_id['black_team_player'])).hexdigest(), hashlib.md5(str(strikers_id['black_team_player'])).hexdigest())
        silver_team = data_processing.TeamData(hashlib.md5(str(defenders_id['silver_team_player'])).hexdigest(), hashlib.md5(str(strikers_id['silver_team_player'])).hexdigest())
    else:
        black_team = data_processing.TeamData(defenders_id['black_team_player'], strikers_id['black_team_player'])
        silver_team = data_processing.TeamData(defenders_id['silver_team_player'], strikers_id['silver_team_player'])

##    teams = {"black" : black_team, "sivler" : silver_team}

    return {"black" : black_team, "sivler" : silver_team}



##players = init_teams(True) # If you pass True, you will get string HEX value of hashed player-id's using MD5 algorithm.
##print str(players[0].defense_id) + " , " + str(players[0].offense_id)
##print str(players[1].defense_id) + " , " + str(players[1].offense_id)
