
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 4
prefs.hardware['audioDriver'] = 'Primary Sound'
import sys


from psychopy import visual, core, sound, event, logging


import numpy as np
# from cerebus import cbpy

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
    
    # cbpy.set_comment(blockLog + ": start")


def mod_present_block(start_react_obj, blockText, blockLog):

    block_instruction = visual.TextStim(start_react_obj.WIN, blockText, color="black")

    wait_for_click(start_react_obj.WIN, block_instruction)
    
    # cbpy.set_comment(blockLog + ": start")


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


def present_modified_trials(start_react_obj, sounds_random_array, 
                            exp_info_dict, block_num): 

    num_trials = exp_info_dict["Trials per Block"]

    for trial_num in range(num_trials): 
        curr_trial_num = trial_num + 1
        loudness_key = sounds_random_array[trial_num]
        start_react_obj.run_experiment(loudness_key, block_num, curr_trial_num)

        # cbpy.set_comment("B " + str(block_num) + " T " + str(trial_num) + " P" + str(loudness_key))








def presentTrials(win, expInfo, stimParams, blockText, logFile, numTrials, soundStrengths, fixation, stimulus):
        total_time = 0
        current_time = core.getTime()

        # go for var number of trials 
        for trial in range(numTrials):
            quit_if_escape(win)
                
        
            # Fixation
            time_up = np.random.uniform(expInfo['DELAY_MIN'], expInfo['DELAY_MAX'] ) # Picks pause time between delay_min and delay_max seconds
            print("time up is ", time_up)
            # Stimulus
            #pick int 0 1 or 2 from array
            sound_picker = soundStrengths[trial]            
            sound_used = stimParams['sound_used'][sound_picker]              

            draw_visual(win, fixation, time_up-0.085)

            if sound_used != None:
                #nextFlip = win.getFutureFlipTime(clock='now')
                #print(str(nextFlip))
                sound_used.play(when=0, log=True) 

            core.wait(0.085)
            stimulus.draw()
            
        

            win.logOnFlip("stimPresented",10)
            win.flip()
            
            
            # cbpy.set_comment(blockText + " T " + str(trial) + " P" + str(soundStrengths[trial]))
            core.wait(stimParams['STIMULUS_DURATION'])
        
            print("block text is ", blockText)

            logFile.write(blockText + " Trial %d, Loudness: %d, Pause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, time_up, core.getTime()))
            print(blockText +         " Trial %d, Loudness: %d, Pause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, time_up, core.getTime()))
            
            logging.flush()
            if (trial == numTrials-1):
                draw_visual(win, fixation, 5)


