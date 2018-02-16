'''
Tiler used to place windows deterministically, along with constants required.
@author starchmd
@datw 2018-02-13 (refactor)
'''
import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk

logging.basicConfig(level=logging.DEBUG)

DEFAULT_WINDOW_WIDTH = 640
DEFAULT_WINDOW_HEIGHT = 360

X_MARGIN = 0
Y_MARGIN = 0

X_RIGHT_MARGIN = 300


class WindowTiler(object):
    '''
    Setup a window tiler based around the default screen
    '''
    def __init__(self):
        '''
        Initialize this
        '''
        self.screens = []
        display = Gdk.Display.get_default()
        for i in range(0, display.get_n_screens()):
            self.screens.append(display.get_screen(i))
        if not self.screens:
            raise Exception("No screens detected. Cannot run. No headless zombies.")
    def tile(self, index):
        '''
        Get the screen and position of a window
        @return (x, y, height, wdith) where the window should be
        '''
        screen = 0
        xpos = X_MARGIN
        ypos = Y_MARGIN
        while index > 0:
            xpos = xpos + DEFAULT_WINDOW_WIDTH
            if xpos + DEFAULT_WINDOW_WIDTH > self.screens[screen].get_width() - X_RIGHT_MARGIN:
                ypos = ypos + DEFAULT_WINDOW_HEIGHT
                xpos = X_MARGIN
            if ypos + DEFAULT_WINDOW_HEIGHT > self.screens[screen].get_height():
                screen = screen + 1
                ypos = Y_MARGIN
            if screen >= len(self.screens):
                screen = 0
                xpos = X_MARGIN
                ypos = Y_MARGIN
            index = index - 1
        return (self.screens[screen], (xpos, ypos), (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT))
    def unindexed_tile(self):
        '''
        Get position in untiled space
        @return (x, y, height, wdith) where the window should be (untiled)
        '''
        return (self.screens[-1], (self.screens[-1].get_width() - X_RIGHT_MARGIN, 0), (X_RIGHT_MARGIN, 0))
