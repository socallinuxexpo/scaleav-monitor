import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GdkX11


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
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.connect("destroy",self.destroy)
        self.window.connect("focus-in-event",self.focusIn)
        self.window.connect("focus-out-event",self.focusOut)
        #Construct window with drawing area
        self.area = Gtk.DrawingArea()
        self.area.set_double_buffered(True)
        self.window.set_default_size(400, 300)
        self.window.add(self.area)
        self.window.set_title(title)
        self.title = title
        self.xid = None
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
