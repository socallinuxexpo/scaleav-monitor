import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

import stream

class Video(stream.BaseStream):
    '''
    @author starchmd
    Stream GStream pipline to window
    '''
    def __init__(self,window):
        '''
        Initialize the GStreamer pipeline
        @param window - window object to draw to
        '''
        self.window = window
        stages = ["videotestsrc","ximagesink"]
        super(Video,self).__init__("Video Pipeline",stages)
         
    def onSync(self,bus,msg):
        '''
        What to do on sync requests
        @param bus - bus relaying message
        @param msg - message sent
        '''
        if msg.get_structure().get_name() == "prepare-window-handle":
            xid = self.window.getXId()
            if xid is None:
                raise Exception("Error: Stream play before window creation")
            msg.src.set_window_handle(xid)
