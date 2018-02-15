'''
A module to encapsulate the base-display code for the monitoring
system's Gtk usage, windowing environment, and interaction code.

@author starchmd
'''
import os
import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

logging.basicConfig(level=logging.DEBUG)


class BaseDisplay(object):
    '''
    A base display window built on GTK containing a drawing area
    for GStream or anything else to draw in.
    @author starchmd
    @date 2018-02-11 (refactored)
    '''
    def __init__(self, title):
        '''
        Initialize the window
        @param title - name of window
        '''
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window.connect("destroy", self.destroy)
        self.window.connect("focus-in-event", self.focus_in)
        self.window.connect("focus-out-event", self.focus_out)
        self.window.connect("key-press-event", self.key_pressed)

        self.window.set_title(title)
        self.title = title
    def initial(self, screen, position, dimension):
        '''
        Set the initial screen, position, and dimensions
        @param screen: screen to display on
        @param position: (x, y) position
        @param dimension: (width, height) dimension of window
        '''
        self.window.resize(*dimension)
        self.window.move(*position)
        self.window.set_screen(screen)
    def show(self):
        '''
        Start the main program
        '''
        self.window.show_all()
    def destroy(self, window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        pass
    def focus_in(self, *args):
        '''
        Focus change event
        '''
        pass
    def focus_out(self, *args):
        '''
        Focus change event
        '''
        pass
    def key_pressed(self, *args):
        '''
        Do nothing key-press
        '''
        pass
class DrawableDisplay(BaseDisplay):
    '''
    A display that allows for drawing to the window, and represents a single unit of
    display size for the standard "tiled" displays.

    @author starchmd
    @date 2018-02-11
    '''
    def __init__(self, index, title):
        '''
        Construct the drawable display based on its tiling-index and
        title
        @param index: index into tiling display
        @param title: title of the window
        '''
        self.menu = []
        self.index = index
        #Why is super last? Setup is called by parent, *and* index must be set first
        super(DrawableDisplay, self).__init__(title)
        #Create a drawable area used to fill with video data
        self.area = Gtk.DrawingArea()
        self.area.set_double_buffered(True)
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.build_menu)
        #Create an image overlay for displaying errors/messages above the draw surface,
        #and add the drawing area as a child
        self.img = Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__),
                                                        "..", "img", "stop.jpg"))
        self.overlay = Gtk.Overlay()
        self.overlay.add_overlay(self.img)
        self.overlay.set_overlay_pass_through(self.img, True)
        self.overlay.add(self.area)
        self.window.add(self.overlay)
        self.xid = None
    def show(self):
        '''
        Show function
        '''
        super(DrawableDisplay, self).show()
        self.xid = self.area.get_window().get_xid()
    def get_xid(self):
        '''
        Gets the X11 window ID
        '''
        return self.xid
    def build_menu(self, event):
        '''
        Builds the menu upon creation during a right click
        @param event: click event triggering this
        '''
        #Ignore all but third button clicks (right click)
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 3:
            return
        #Create a new menu from the responded items
        self.menu = Gtk.Menu()
        for label in self.get_menu_items():
            item = Gtk.CheckMenuItem(label)
            if label == self.get_current_item():
                item.set_active(True)
            item.connect("button-press-event", self.menu_click)
            self.menu.append(item)
        #Force menu to pop up with all items displayed
        self.menu.show_all()
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def get_menu_items(self):
        '''
        List of menu items
        '''
        return []
    def get_current_item(self):
        '''
        Gets menu item to display as checked
        '''
        return None
    def menu_click(self, selected, event):
        '''
        A callback handling the GTK events and passing through to a callback
        that only needs to deal with the menu item name.
        @param selected: menu item clicked
        @param event: mouse event
        '''
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1:
            return
        for item in self.menu:
            item.set_active(False)
        selected.set_active(True)
        self.menu_callback(selected.get_label())
    def menu_callback(self, item):
        '''
        What to do when menu is clicked. Virtual function/
        @param item: menu item name which was clicked
        '''
        pass
