import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

import av.video
count=1
class AV(av.video.Video):
    '''
    @author starchmd
    A combined audio source and video stream
    '''
    def __init__(self,window,aout):
        '''
        Initialize the video, and the audio source
        @param window - window object to draw to
        @param aout - global audio out
        '''
        global count
        self.aout = aout
        self.audio = Gst.ElementFactory.make("audiotestsrc","ATC")
        self.audio.set_property("freq",100*count)
        count=count+1
        window.registerFocusEvent(self.replace)
        super(AV,self).__init__(window)
    def replace(self):
        '''
        Replace the global audio source with this audio track
        '''
        print("Calling replace")
        self.aout.setSource(self.audio)
