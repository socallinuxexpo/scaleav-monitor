import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GdkX11
import logging

logging.basicConfig(level=logging.DEBUG)


class BaseDisplay(object):
    '''
    @author starchmd
    A base display window built on GTK containing a drawing area
    for GStream or anything else to draw in.
    '''
    def __init__(self,title):
        '''
        Initialize the window
        @param title - name of window
        '''
        logging.debug("Setting up base window")
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.connect("destroy",self.destroy)
        self.window.connect("focus-in-event",self.focusIn)
        self.window.connect("focus-out-event",self.focusOut)
        #Construct window with drawing area
        self.area = Gtk.DrawingArea()
        self.area.set_double_buffered(True)
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.makeMenu)
        self.window.set_default_size(400, 300)
        self.window.add(self.area)
        self.window.set_title(title)
        self.title = title
        self.xid = None
        logging.debug("Done setting up base window")
    def makeMenu(self, drawArea, event):
        '''
        Generates a menu based on the GTK menu setup when the draw event
        is called with a 3rd mous click
        '''
        #Ignore all but third button clicks (right click)
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 3:
            return
        #Create a new menu from the responded items
        self.menu = Gtk.Menu()
        for label in self.getMenuItems():
            item = Gtk.MenuItem(label)
            item.connect("button-press-event", self.menuClick)
            self.menu.append(item)
        #Force menu to pop up with all items displayed
        self.menu.show_all()
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def menuClick(self, menuItem,event):
        '''
        A callback handling the GTK events and passing through to a callback
        that only needs to deal with the menu item name.
        '''
        logging.debug("Menu click recieved: {0}".format(menuItem.get_label()))
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1:
            return
        self.menuCallback(menuItem.get_label())
    def show(self):
        '''
        Start the main program
        '''
        self.window.show_all()
        #Must be done on same thread as the above call, so cache here
        self.xid = self.area.get_window().get_xid()
    def getXId(self):
        '''
        Gets the X11 window ID
        '''
        return self.xid
    def destroy(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        pass
    def focusIn(self,*args):
       '''
       Focus change event
       '''
       pass
    def focusOut(self,*args):
       '''
       Focus change event
       '''
       pass
    def menuCallback(self, item):
        '''
        A callback called when a menu item is clicked
        @param item: menu item name passed back
        '''
        #Does nothing, reimplement in child class
        pass
    def getMenuItems(self):
        '''
        Responds with the menu items that should be provided
        to select from
        '''
        #Does nothing, reimplement in child class
        return []
