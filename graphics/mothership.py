'''
Code for displaying mothership's main window with buttons, sliders, etc.
@author starchmd, mescoops
@date 2018-02-10
'''
import os
import functools
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import graphics.base

class MothershipDisplay(graphics.base.BaseDisplay):
    '''
    A class used to display the mothership room on/off and shutdown
    controls

    @date 2018-02-10
    @author starchmd, mescoops
    '''
    def __init__(self, title):
        '''
        Initializes display
        @param title: title to display for this window
        '''
        self.buttons = []
        self.shutdowncb = lambda: True
        self.restartcb = lambda: True
        super(MothershipDisplay, self).__init__(title)
        #Set window boarder
        self.window.connect('delete_event', lambda x, y: True)
        self.window.set_border_width(15)
        buttonbox = Gtk.Box(spacing=6)
        #Add global buttons
        button = Gtk.Button.new_with_label("Shutdown")
        button.connect("clicked", self.shutdown)
        buttonbox.pack_start(button, True, True, 0)
        self.buttons.append(button)
        button = Gtk.Button.new_with_label("Restart All")
        button.connect("clicked", self.restart)
        buttonbox.pack_start(button, True, True, 0)
        self.buttons.append(button)
        #Load image to display at top of controls
        logo = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__),
                                                        "..", "img", "16x_logo_sm.png"))
        #Virtival display box
        self.roombox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.roombox.pack_start(logo, False, True, 0)
        self.roombox.pack_end(buttonbox, False, True, 0)
        self.window.add(self.roombox)
    def initial(self, screen, position, dimension):
        '''
        Set the initial screen, x, y, width, and height of a screen
        @param screen: screen to position it to
        @param position: (x,y) position
        @param dimension: (width, height) dimension of window
        '''
        self.window.resize(*dimension)
        self.window.move(*position)
        self.window.set_screen(screen)
    def set_callbacks(self, shutdown, restart):
        '''
        Sets callbacks for the global buttons
        @param shutdown: shutdown callback
        @param restart: restart callback
        '''
        self.shutdowncb = shutdown
        self.restartcb = restart
    def add_room(self, name, onf, off):
        '''
        Adds a room entry to the GUI
        @param name: name of room to add
        @param onf: callback function for turning on
        @param off: callback function for turining off
        '''
        room = Gtk.Box(spacing=6)
        #Room switch
        switch = Gtk.Switch()
        switch.connect("notify::active", functools.partial(room_on_off, onf, off))
        switch.set_active(True)
        self.buttons.append(switch)
        room.pack_start(switch, False, False, 0)
        #Room label
        label = Gtk.Label()
        label.set_text(name)
        label.set_justify(Gtk.Justification.LEFT)
        room.pack_start(label, False, False, 0)

        self.roombox.pack_start(room, False, False, 0)
    def lock(self):
        '''
        Locks all buttons
        '''
        for button in self.buttons:
            button.set_sensitive(False)
    def unlock(self):
        '''
        Unlocks all buttons
        '''
        for button in self.buttons:
            button.set_sensitive(True)
    def shutdown(self, event):
        '''
        Shutdown click callback
        '''
        self.shutdowncb()
    def restart(self, event):
        '''
        Restart button callback
        '''
        self.restartcb()
def room_on_off(onf, off, switch, gparam):
    '''
    Responds to the switch clicking by calling the on
    or off function
    @param onf: on function to call
    @param off: off function to call
    @param switch: switch from GTK
    @param gparam: gparam from GTK
    '''
    if switch.get_active():
        onf()
        return
    off()
