import gi
gi.require_version("Gst","1.0")
from gi.repository import  GObject, Gst, GstVideo

import av.stream
import logging

logging.basicConfig(level=logging.DEBUG)

class Video(av.stream.BaseStream):
    '''
    @author starchmd
    Stream GStream pipline to window
    '''
    def __init__(self,window,pipeline):
        '''
        Initialize the GStreamer pipeline
        @param window - window object to draw to
        '''
        logging.debug("Setting up video stream")
        self.window = window
        stages = [{"name":"autosink-1","type":"xvimagesink"}]
        super(Video,self).__init__("Video Pipeline",stages,pipeline)
         
    def onSync(self,bus,msg):
        '''
        What to do on sync requests
        @param bus - bus relaying message
        @param msg - message sent
        '''
        if msg.get_structure().get_name() == "prepare-window-handle":
            xid = self.window.getXId()
            print("Self Message Source",xid, msg.src)
            if xid is None:
                logging.warning("Started video stream before window creation")
                raise Exception("Error: Stream play before window creation")
            def setHandle(xid):
                msg.src.set_window_handle(xid)
            #GObject.idle_add(setHandle,xid)
            setHandle(xid)
