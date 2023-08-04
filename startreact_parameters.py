from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 4
prefs.hardware['audioDriver'] = 'Primary Sound'

from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, colors
import os
import numpy as np
import utils

def get_startreact_parameters():
    # Store info about the experiment session
    expInfo = {
        'ID': '',
        'Blocks': 5, # 5 plus practice
        'Practice Trials': 3,
        'Trials per Block': 15,
        'Block Start (Please only input 1, 2, 3, 4, or 5)': 1, #1-5
        # ^ pick what trial you want to start at if you need to restart the experiment
        'Other Notes': '',
    }

    # https://psychopy.org/api/gui.html
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title='StartReact Experiment')
    if dlg.OK == False:
        core.quit()  # user pressed cancel

    #expInfo['ID']
    #expInfo['Blocks']
#   expInfo['Trials per Block']
    expInfo['expName']          = 'StartReact Experiment'
    expInfo['psychopyVersion']  = '2021.2.3'
    expInfo['Date']             = data.getDateStr()  # add a simple timestamp
   
    expInfo['Block Start']      = expInfo['Block Start (Please only input 1, 2, 3, 4, or 5)'] - 1
    #expInfo['Practice Trials']  = 3
    #expInfo['TOTAL_TRIALS']     = NUM_TRIALS + PRACTICE_TRIALS
    expInfo['DELAY_MIN']        = 5 # seconds
    expInfo['DELAY_MAX']        = 7 # seconds
    expInfo['BLOCK_TEXTS']      = np.array(["Raise your arm to the side", 
                                            "Bend your elbow", 
                                            "Extend your elbow", 
                                            "Lift your wrist", 
                                            "Move your index finger towards your thumb"])
    expInfo['TEST_RUN_TEXT']    = "Practice Trials. Press any key to start"

    ####
    

    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    fileName = _thisDir + os.sep + u'data/%s.txt' %(expInfo['ID']) 
    dataFile = open(fileName, 'w') 
    dataFile.write("ID, Experiment Name, Date, Number of Blocks. Number of Trials \n")
    dataFile.write("%s, %s, %s, %s, %s" %(expInfo['ID'], expInfo['expName'], expInfo['Date'], expInfo['Blocks'], expInfo['Trials per Block']))
 
    logFile = logging.LogFile(fileName+'.log', level=0)  

    return expInfo, logFile


def defFixation(win):
    # Fixation cross
    fixation = visual.ShapeStim(win, 
        vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth=5,
        closeShape=False,
        lineColor="white",
        autoLog=True 
    )
    return fixation


def defStimulus(win):
    # Stimulus circle
    stimulus = visual.Circle(win, 
        radius=9,
        fillColor = 'red',
        lineColor = 'red',
        autoLog=True
    )
    return stimulus

def stimParameters():
# Stimulus Parameters
    stimParams = {}
    stimParams['STIMULUS_DURATION'] = 0.02 # 20 ms

# Sound Parameters 
    stimParameters["READY"]     = 80
    stimParams['NUM_SOUNDS']    = 3
    stimParams['QUIET_DB']      = 80 # db
    stimParams['QUIET_HZ']      = 500 # Hz
    stimParams['QUIET_TIME']    = 1/20 # 50 ms
    stimParams['LOUD_DB']       = 100 # db
    stimParams['LOUD_HZ']       = 500 # Hz
    stimParams['LOUD_TIME']     = 1/20 # 50 ms
    stimParams['SYNC_DB']       = 48# db
    stimParams['SYNC_HZ']       = 500 # Hz
    stimParams['SYNC_TIME']     = 100e-3 # sec
    stimParams['SYNC_TIME']
    print(utils.convert_db_to_vol(stimParams['QUIET_DB']))
    stimParams['sound_used'] = { 
                0: None, # no audio
                1: utils.get_audio(amp=stimParams['QUIET_DB'], freq=stimParams['QUIET_HZ'], time=stimParams['QUIET_TIME']), # quiet audio
                2: utils.get_audio(amp=stimParams['LOUD_DB'],  freq=stimParams['LOUD_HZ'],  time=stimParams['LOUD_TIME']) # startling_audio 
            }
    return stimParams