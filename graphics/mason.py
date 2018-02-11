import gi
gi.require_version("Gtk","3.0")
from gi.repository import GObject, Gtk, Gdk, GdkX11
import os
import logging

logging.basicConfig(level=logging.DEBUG)

DEFAULT_WINDOW_WIDTH=640
DEFAULT_WINDOW_HEIGHT=360

X_MARGIN=0
Y_MARGIN=0

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
        if len(self.screens) == 0:
            raise Exception("No screens detected. Cannot run. No headless zombies.")
    def tile(self, index):
        '''
        Get the screen and position of a window
        @return (screen #, x, y) where the window should be
        '''
        screen = 0
        x = X_MARGIN
        y = Y_MARGIN
        while index > 0:
            x = x + DEFAULT_WINDOW_WIDTH
            if x + DEFAULT_WINDOW_WIDTH > self.screens[screen].get_width():
                y = y + DEFAULT_WINDOW_HEIGHT
                x = X_MARGIN
            if y + DEFAULT_WINDOW_HEIGHT > self.screens[screen].get_height():
                screen = screen + 1
                y = Y_MARGIN
            if screen >= len(self.screens):
                screen = 0
                x = X_MARGIN
                y = Y_MARGIN
            index = index - 1
        return (self.screens[index], x, y, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
