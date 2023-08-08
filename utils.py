
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 4
prefs.hardware['audioDriver'] = 'Primary Sound'
import sys


from psychopy import visual, core, sound, event, logging


import numpy as np
from cerebus import cbpy

def wait_for_click(win, visual):
    """
    Waits for a keypress to be pressed

    :param win: window projected on monitor
    :param visual: visual to be displayed
    :returns: key pressed
    """
    visual.draw()
    win.flip()
    keys_clicked = event.waitKeys()

    if len(keys_clicked) < 1 or "escape" in keys_clicked: 
        quit(win)


def draw_visual(window, visual, time):
    """
    Draws a visual image onto the window

    :param window: window projected on monitor
    :param visual: visual to be displayed
    :param time: time visual is displayed (s)
    :returns: shows visual on window
    """
    
    visual.draw()
    window.flip()
    core.wait(time)

def draw_visual_waitKeys(window, visual):
    """
    Draws a visual image onto the window

    :param window: window projected on monitor
    :param visual: visual to be displayed
    :param time: time visual is displayed (s)
    :returns: shows visual on window
    """
    
    visual.draw()
    window.flip()
    keys = event.getKeys()

    if "escape" in keys: 
        window.close()
        sys.exit() 
    event.waitKeys()
    #window.flip()
    
def convert_db_to_vol(this_vol):
    """
    Returns the volume value of a dB

    :param this_vol: the volume value (in dB)
    :returns: the volume value as a float between 0 and 1
    """
    return ((0.34/0.1)/(10**(111.8/20)))*(10**(this_vol/20))

def get_audio(amp, freq, time):
    """
    Returns a sound object given the amplitude, frequency, and time
    
    :param amp: Amplitude value (in dB)
    :param freq: Frequency value (in Hz)
    :param time: Time value (in s)
    :returns: sound object in Psychopy
    """
    return sound.Sound(value=freq, secs=time, hamming=False, volume=convert_db_to_vol(amp), preBuffer=-1, syncToWin=True, autoLog=True)  

def presentBlock(win, blockText, blockLog):

    block_instruction = visual.TextStim(win,blockText, color="black")

    wait_for_click(win, block_instruction)
    
    cbpy.set_comment(blockLog + ": start")


# returns true if the escape key is pressed, false otherwise
def is_escape_pressed(win):

    keys = event.getKeys()
    return "escape" in keys

def quit_if_escape(win): 

    if is_escape_pressed(win): 
        quit(win)

# when called, will terminate the entire experiment
def quit(win): 
    win.close()
    sys.exit()


def presentTrials(win, expInfo, stimParams, blockText, logFile, numTrials, soundStrengths, fixation, stimulus, stimulus_ready):

        total_time = 0
        current_time = core.getTime()
        for trial in range(numTrials):
            quit_if_escape(win)

            # Choose Jitter Times
            short_jitter_time = np.random.uniform(expInfo['SHORT_DELAY_MIN'], expInfo['SHORT_DELAY_MAX'] ) # Picks pause time between delay_min and delay_max seconds
            long_jitter_time =  np.random.uniform(expInfo['LONG_DELAY_MIN'], expInfo['LONG_DELAY_MAX'] ) 
            sound_picker = soundStrengths[trial]            
            sound_used = stimParams['sound_used'][sound_picker]              
            sound_ready = stimParams['sound_used'][3]              
           
            # Fixation
            draw_visual_waitKeys(win, fixation)
            
            
            # Stimulus Ready presentation
            core.wait(short_jitter_time-expInfo['FIXED_SPEAKER_DELAY'])        
            sound_ready.play(when=0, log=True) 
            core.wait(expInfo['FIXED_SPEAKER_DELAY'])
            stimulus_ready.draw()
            win.logOnFlip("readyPresented",10)
            win.flip()
            cbpy.set_comment(blockText + " T " + str(trial) + " READY")
            core.wait(stimParams['STIMULUSREADY_DURATION'])
            #win.flip()
        
            # Stimulus  presentation
            core.wait(long_jitter_time-expInfo['FIXED_SPEAKER_DELAY'])        
            if sound_used != None:
                sound_used.play(when=0, log=True) 
            core.wait(expInfo['FIXED_SPEAKER_DELAY'])
            stimulus.draw()
            win.logOnFlip("stimulusPresented",10)
            win.flip()
            cbpy.set_comment(blockText + " T " + str(trial) + " P" + str(soundStrengths[trial]))
            core.wait(stimParams['STIMULUS_DURATION'])
            win.flip()
            
            logFile.write(blockText + " Trial %d, Loudness: %d, ShortPause: %.3f, LongPause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, short_jitter_time, long_jitter_time, core.getTime()))
            print(blockText +         " Trial %d, Loudness: %d, ShortPause: %.3f, LongPause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, short_jitter_time, long_jitter_time, core.getTime()))
            
            logging.flush()
            if (trial == numTrials-1):
                draw_visual(win, fixation, 5)


