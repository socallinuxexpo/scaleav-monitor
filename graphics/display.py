import graphics.base
import av.av
import os
import logging
import gi
gi.require_version("Gst","1.0")
from gi.repository import  GObject, Gst, GstVideo, Gtk

RETRY_INTERVAL_MS=1000

logging.basicConfig(level=logging.DEBUG)

class AVDisplay(graphics.base.BaseDisplay):
    '''
    @author starchmd
    A display that shows a video stream and plays audio only on focus.
    '''
    def __init__(self,title,stream):
        '''
        Initialize the window
        @param title - name of window
        '''
        logging.debug("Setting up AV Display")
        self.title = title
        self.stream = stream
        super(AVDisplay,self).__init__(title)
        #Pass in 'self' as window
        self.av = av.av.AV(self,stream,onerror=self.onError)
        logging.debug("Done setting up AV Display")
        self.retrying = False
    def show(self):
        '''
        Start the main program
        '''
        logging.debug("Showing AV display")
        super(AVDisplay,self).show(self.av)
    def start(self):
        '''
        Start the stream running
        '''
        self.img.hide()
        self.av.start() 
    def onError(self,msg):
        '''
        What to do when the stream errors
        @param msg: message containing error
        '''
        def showImg(param): 
            self.img.show()
        GObject.idle_add(showImg,None)
        if self.retrying:
            return
        for message in ["Stream doesn't contain enough data", "Internal data flow error"]:
            if message in str(msg.parse_error()):
                break
        else:
            return
        self.av.stop()
        self.retrying = True
        GObject.timeout_add(RETRY_INTERVAL_MS,self.retryConnection,None)
    def retryConnection(self,data): 
        '''
        Retry connection on disconnect
        '''
        state = self.av.pipeline.get_state(0).state
        print("State: {0}".format(state))
        if state == Gst.State.PLAYING:
            self.retrying = False
            return False
        self.av.stop()
        self.start()
        return True
    def destroy(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        logging.debug("Destroying AV Display, attempting recreation")
        try:
            self.av.stop()
            tmp = AVDisplay(self.title,self.stream)
            tmp.show()
        except Exception as e:
            logging.warning("Failed to stop AV and restart window. {0}:{1}".format(type(e),e))
    def focusIn(self,*args):
       '''
       Focus change event
       '''
       logging.debug("Focus in")
       self.av.startAudio()
    def focusOut(self,*args):
       '''
       Focus change event
       '''
       logging.debug("Focus out")
       self.av.stopAudio()
    def menuCallback(self, item):
        '''
        A callback called when a menu item is clicked
        @param item: menu item name passed back
        '''
        logging.debug("Switching audio to: {0}".format(item))
        self.av.switchAudios(item,updateCurrent=True)
    def getMenuItems(self):
        '''
        Responds with the menu items that should be provided
        to select from
        '''
        return self.av.getAudioStreams()
    def getCurrentItem(self):
        '''
        Responds with the menu items that should be checked
        '''
        return self.av.getActiveStream()
