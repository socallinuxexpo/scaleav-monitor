'''
Main graphics loop code.
@author starchmd
@date 2018-02-13 (refactor)
'''
import gi
gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gtk, Gst
#Global initializations
Gst.init(None)
GObject.threads_init()
def loop():
    '''
    Start GTK loop
    '''
    Gtk.main()
