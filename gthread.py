from gi.repository import GObject,Gtk
#Global initializations
GObject.threads_init()
def loop():
    '''
    Start GTK loop
    '''
    Gtk.main()

