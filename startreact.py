#!/usr/bin/env python
# -*- coding: utf-8 -*-
# %% Import libraries
#import psychopy.iohub as io

import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import utils


#os.add_dll_directory(os.path.join(os.environ['Conda_prefix'],"Lib/site-packages/PyQt5/Qt5/bin")) # Fix required for cerebus for python > 3.8

# from psychopy import prefs
# prefs.hardware['audioLib'] = ['PTB']
# prefs.hardware['audioLatencyMode'] = 4
# prefs.hardware['audioDriver'] = 'Primary Sound'


from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, colors
print(sound.Sound) # <class 'psychopy.sound.backend_ptb.SoundPTB'>
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
from startreact_parameters import get_startreact_parameters, defFixation, defStimulus, stimParameters
# from cerebus import cbpy

# %% Setup connection to blackrock amplifier
# blackrock_ConnectionParameters = cbpy.defaultConParams()
# blackrock_ConnectionParameters['client-addr']='192.168.137.3'
# try:
#     cbpy.open(parameter=blackrock_ConnectionParameters)
#     print("Sending timestamps.....")
# except RuntimeError:
#     print("Could not connect to blackrock amplifier")

# %% Experiment parameters


expInfo, logFile = get_startreact_parameters()
print("expInfo is", expInfo)

#was true  
win = visual.Window([800,600], fullscr= False, monitor="testMonitor", units="cm",color="white")

stimulus = defStimulus(win)
fixation = defFixation(win)
stimParams = stimParameters()

# %% Experiment 
print("Starting experiment...")

for block in range(expInfo['Block Start'],  expInfo['Blocks']):
    # if (block == 0 and expInfo['Practice Trials'] > 0):
        # do a practice block
        # test_run_instruction = visual.TextStim(win,
            # text=expInfo['TEST_RUN_TEXT'], color="black"
        # )
 
        # sounds_practice = np.zeros(expInfo['Practice Trials'], dtype=int)
        # for i in range (expInfo['Practice Trials']):
            # sounds_practice[i] = i % stimParams['NUM_SOUNDS']
        # 
        # text=expInfo['TEST_RUN_TEXT']
        # utils.presentBlock(win,text, 'P' + str(block+1))
        # utils.presentTrials(win, expInfo, stimParams, 'P' + str(block+1), logFile, expInfo['Practice Trials'], sounds_practice, fixation, stimulus)

    #randomize order of presented stimuli
    sounds_random = np.tile(np.arange(stimParams['NUM_SOUNDS']), int(expInfo['Trials per Block']/stimParams['NUM_SOUNDS']))
    print("sounds random is", sounds_random)
    np.random.shuffle(sounds_random)

    # Present block instructions
    
    text=f"Block {block+1}\n{expInfo['BLOCK_TEXTS'][block]}\nPress any key to Start"
    

    utils.presentBlock(win, text, 'B' + str(block+1))
    # def presentTrials(win, expInfo, stimParams, blockText, logFile, numTrials, soundStrengths, fixation, stimulus):
    utils.presentTrials(win, expInfo, stimParams, 'B' + str(block+1), logFile, expInfo['Trials per Block'], sounds_random, fixation, stimulus)
    

# make sure everything is closed down

# cbpy.close()
win.close()
core.quit()
