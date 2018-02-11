import gi
gi.require_version("Gtk","3.0")
from gi.repository import GObject, Gtk, Gdk, GdkX11
import graphics.base
import functools

class MothershipDisplay(object): #TODO: graphics.base.BaseDisplay):
    '''
    A class used to display the mothership room on/off and shutdown
    controls

    @date 2018-02-10
    @author lestarch, mescoops
    '''
    def __init__(self, index, title):
        '''
        Initializes display
        '''
        self.buttons = []
        self.shutdowncb = lambda: True
        self.restartcb = lambda: True
        #TODO: super(MothershipDisplay,self).__init__(index, title)
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window.connect("destroy",self.destroy)
        self.window.connect("key-press-event", self.keyPressed)
        #Setup mothership UI
        self.window.set_border_width(15)
        buttonbox = Gtk.Box(spacing=6)

        button = Gtk.Button.new_with_label("Shutdown")
        button.connect("clicked", self.shutdown)
        buttonbox.pack_start(button, True, True, 0)
        self.buttons.append(button)
        button = Gtk.Button.new_with_label("Restart All")
        button.connect("clicked", self.restart)
        buttonbox.pack_start(button, True, True, 0)
        self.buttons.append(button)
        
        self.roombox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.roombox.pack_end(buttonbox, False, True, 0)
        self.window.add(self.roombox)


    def initial(self, screen, x, y, width, height):
        '''
        Set the initial screen, x, y, width, and height of a screen
        @param screen: screen to display on
        @param x: x position
        @param y: y position
        @param width: width of window
        @param height: height of window
        '''
        self.window.resize(width, height)
        self.window.move(x, y)
    def set_callbacks(self, shutdown, restart):
        '''
        Sets callbacks for the global buttons
        @param shutdown: shutdown callback
        @param restart: restart callback
        '''
        self.shutdowncb = shutdown
        self.restartcb = restart
    def add_room(self, name, on, off):
        '''
        Adds a room entry to the GUI
        @param name: name of room to add
        @param on: callback function for turning on
        @param off: callback function for turining off
        '''
        room = Gtk.Box(spacing=6)
        #Room switch
        switch = Gtk.Switch()
        switch.connect("notify::active", functools.partial(self.room_on_off, on, off))
        switch.set_active(True) #TODO: check window state
        self.buttons.append(switch)
        room.pack_start(switch, False, False, 0)
 
        #Room label
        label = Gtk.Label()
        label.set_text(name)
        label.set_justify(Gtk.Justification.LEFT)
        room.pack_start(label, False, False, 0)

        self.roombox.pack_start(room, False, False, 0)
    def show(self,stream=None):
        '''
        Start the main program
        '''
        self.window.show_all()
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
    def destroy():
        pass
    def keyPressed():
        pass
    def room_on_off(self, on, off, switch, gparam):
        '''
        Responds to the switch clicking by calling the on
        or off function
        @param on: on function to call
        @param off: off function to call
        @param switch: switch from GTK
        @param gparam: gparam from GTK
        '''
        if switch.get_active():
            on()
            return
        off()
