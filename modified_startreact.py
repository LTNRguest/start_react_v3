"""
modified_startreact.py 
Author: Nadim Barakat
Date: 8/3/2023


Purpose: This class presents shapes and sound to users as it is used
in conjuction with other monitoring to assess reaction times. 

Here is the current workflow of this module 

display "+" until any key pressed -> a buffer of 1.5 seconds ->
a yellow square is displayed for 80 ms. A sound at 80 dB is also 
played -> a buffer of 3.5 seconds -> a green circle is shown 
for 50 ms along with a sound of 125 dB -> buffer of 2 seconds ->
end. 


Modules needed: 
    pip install psychopy 
    
    you need the utils file (I am not the author of that file)

Current usage: 
    create an instance of the class and call the run() method.

    ModifiedStartReact().run()

"""

from psychopy import visual, core, event
from utils import get_audio


class ModifiedStartReact: 
    # constant sound variables for quiet and loud sound settings 
    QUIET_DB   = 80 
    QUIET_HZ   = 500
    LOUD_DB    = 125
    LOUD_HZ    = 500 
    SOUND_TIME = 0.05

    # this is display time of the shape (square or circle)
    SHORT_DISPLAY_TIME = 0.5 
    LONG_DISPLAY_TIME  = 0.8

    # this is time after a stimulus is shown. Blank screen is shown during
    # this time. 
    SHORT_BUFFER_TIME  = 1.5 
    MEDIUM_BUFFER_TIME = 2.0
    LONG_BUFFER_TIME   = 3.5 

    # this size may need to be configured for the computer in the VA
    # change to fullscr = True for full screen  
    WIN = visual.Window(size = (800, 600),  monitor = "testMonitor", 
                            fullscr = False, allowGUI = True)

    # draws a + icon to the screen. does not remove the icon 
    def draw_plus(self): 
        size = 0.1
        line1 = visual.Line(self.WIN, start=(-size, 0), end=(size, 0), 
                                lineWidth=2)
        
        line2 = visual.Line(self.WIN, start=(0, size), end=(0, -size), 
                                lineWidth=2)

        line1.draw()
        line2.draw()

        self.WIN.flip()


    # draws the plus icon until users clicks any key. then waits for specified
    # time (time_seconds) on blank screen 
    def display_plus_until_click(self, time_seconds): 
        self.draw_plus()
        event.waitKeys()

        # clear the screen after user clicks 
        self.WIN.flip()
        core.wait(time_seconds)

    # return a square object that is yellow 
    def create_square(self): 
        square_side_len = 0.2
        square = visual.Rect(self.WIN, width = square_side_len, 
                                height = square_side_len, fillColor = 'yellow')
    
        return square 
    
    # returns a circle object that is green 
    def create_circle(self): 
        circle_radius = 0.3
        circle_position = (0, 0)

        circle = visual.Circle(self.WIN, radius = circle_radius, size = 0.9, 
                                pos = circle_position, fillColor = 'green')

        return circle

    # displays the given shape object to the screen. Does not clear screen
    def draw_shape(self, shape):
        shape.draw()
        self.WIN.flip()


    # plays a sound of a certain strength depending on provided keyword

    # sound_strengh_keyword: type = string. this can only be "quiet" or "loud"
    # quiet will play a sound of 80 db while loud will play 125 db 
    # 
    # if other param string entered, no sound will play 
    # 
    # quirks: couldn't figure out why, but sound was only played when 
    # this function returns sound object and caller stores returned value, even
    # though sound playing happens before return 
    def play_sound(self, sound_strength_keyword): 
        sound_strength_keyword = sound_strength_keyword.lower()

        sound_used = None 

        if sound_strength_keyword == "quiet": 
            sound_used = get_audio(self.QUIET_DB, self.QUIET_HZ, self.SOUND_TIME)
        elif sound_strength_keyword == "loud": 
            sound_used = get_audio(self.LOUD_DB, self.LOUD_HZ, self.SOUND_TIME)
        
        if sound_used != None: 
            sound_used.play(when = 0)

        return sound_used
    
    # this does the main heavy lifting.
    # Draws a specified shape at a specified sound, for a specified time, 
    # then presents blank screen for another specified time 
    #
    # params: 
    #       shape: (string). can have value of "circle" or "square"
    #       sound_keyword: (string). can have value of "quiet" or "loud"
    #               anything else will mean no sound 
    #       display_time: (int or float): the time to display shape before 
    #                       erasing it from screen 
    #       buffer_time: (int or float): time of blank screen after removing
    #                       shape 
    def draw_shape_play_sound_wait(self, shape, sound_keyword, display_time, 
                                buffer_time): 
       
        shape = shape.lower()
        shape_obj = None 

        if shape == "square": 
            shape_obj = self.create_square()
        elif shape == "circle": 
            shape_obj = self.create_circle()

        self.draw_shape(shape_obj)
        sound = self.play_sound(sound_keyword)

        core.wait(display_time)

        self.WIN.flip()

        core.wait(buffer_time)

    # "public" function of this class. 
    # performs workflow specified in file header 
    def run(self): 
        self.display_plus_until_click(self.SHORT_BUFFER_TIME)

        self.draw_shape_play_sound_wait("square", "quiet", 
                            self.LONG_DISPLAY_TIME, self.LONG_BUFFER_TIME)
        
        self.draw_shape_play_sound_wait("circle", "loud",
                            self.SHORT_DISPLAY_TIME, self.MEDIUM_BUFFER_TIME)
        self.WIN.close()




ModifiedStartReact().run()