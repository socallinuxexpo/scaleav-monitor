import gi
gi.require_version("Gtk","3.0")
from gi.repository import GObject, Gtk, Gdk, GdkX11
import os
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
        self.window.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window.connect("destroy",self.destroy)
        self.window.connect("focus-in-event",self.focusIn)
        self.window.connect("focus-out-event",self.focusOut)
        self.window.connect("key-press-event", self.keyPressed)
        #Construct window with drawing area
        self.area = Gtk.DrawingArea()
        self.area.set_double_buffered(True)
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.makeMenu)
        self.img = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__),"..","img","stop.jpg"))
        self.window.set_default_size(640, 360)
        self.overlay = Gtk.Overlay()
        self.overlay.add(self.area)
        self.overlay.add_overlay(self.img)
        self.overlay.set_overlay_pass_through(self.img, True)
        self.window.add(self.overlay)
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
            item = Gtk.CheckMenuItem(label)
            if label == self.getCurrentItem():
                 item.set_active(True)
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
        for item in self.menu:
            item.set_active(False)
        menuItem.set_active(True)
        self.menuCallback(menuItem.get_label())
    def show(self,stream=None):
        '''
        Start the main program
        '''
        self.window.show_all()
        #Must be done on same thread as the above call, so cache here
        self.xid = self.area.get_window().get_xid()
        if not stream is None:
            def startStream(stream):
                 self.img.hide()
                 stream.start()
            GObject.idle_add(startStream,stream)
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
    def getCurrentItem(self):
        '''
        Gets item to be checked
        '''
        return None
    def keyPressed(self, args, arg2):
        '''
        Do nothing key-press
        '''
        pass
