from gi.repository import GObject,Gtk
#Global initializations
Gst.init(None)
GObject.threads_init()
def loop():
    '''
    Start GTK loop
    '''
    Gtk.main()

