#!/usr/bin/env python
# -*- coding: utf-8 -*-
# %% Import libraries
#import psychopy.iohub as io

import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import utils
from modified_startreact import ModifiedStartReact

#os.add_dll_directory(os.path.join(os.environ['Conda_prefix'],"Lib/site-packages/PyQt5/Qt5/bin")) # Fix required for cerebus for python > 3.8

# from psychopy import prefs
# prefs.hardware['audioLib'] = ['PTB']
# prefs.hardware['audioLatencyMode'] = 4
# prefs.hardware['audioDriver'] = 'Primary Sound'


from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, colors

from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
from startreact_parameters import get_startreact_parameters, stimParameters
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
stimParams = stimParameters()


start_react_obj = ModifiedStartReact(logFile)



for block in range(expInfo['Block Start'],  expInfo['Blocks']):

    sounds_random_array = np.tile(np.arange(stimParams['NUM_SOUNDS']), 
                            int(expInfo['Trials per Block'] / stimParams['NUM_SOUNDS']))
    
    np.random.shuffle(sounds_random_array)

    curr_block_num = block + 1

    # Present block instructions
    text = f"Block {block+1}\n{expInfo['BLOCK_TEXTS'][block]}\nPress any key to Start"
    utils.mod_present_block(start_react_obj, text, "B" + str(curr_block_num))

    utils.present_modified_trials(start_react_obj, 
                                  sounds_random_array, expInfo, curr_block_num)
    


# make sure everything is closed down

# cbpy.close()
start_react_obj.WIN.close()
core.quit()
