import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GdkX11


class Display(object):
    '''
    @author starchmd
    A display built on GTK for use in diaplying GStreamer streams
    '''
    def __init__(self,title):
        '''
        Initialize the window
        @param title - name of window
        '''
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.connect("destroy", self.quit)
        self.window.connect("focus-in-event",self.focus)
        #Construct window with drawing area
        self.area = Gtk.DrawingArea()
        self.area.set_double_buffered(True)
        self.window.set_default_size(400, 300)
        self.window.add(self.area)
        self.window.set_title(title)
        self.title = title
        self.xid = None
    def run(self):
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
    def quit(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        #TODO: callbacks happen here
        Gtk.main_quit()
    def focus(self,*args):
       '''
       Focus change event
       '''
       print("Focus-in:",self.title)
       for arg in args:
           print(type(arg),arg)


