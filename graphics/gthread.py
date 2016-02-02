import gi
gi.require_version("Gst","1.0")
from gi.repository import  GObject,Gtk,Gst
#Global initializations
Gst.init(None)
GObject.threads_init()
def loop():
    '''
    Start GTK loop
    '''
    Gtk.main()

