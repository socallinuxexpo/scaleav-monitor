import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

import stream

class Audio(stream.BaseStream):
    '''
    @author starchmd
    Audio stream for audio sink
    '''
    def __init__(self):
        '''
        Initialize the GStreamer pipeline
        '''
        stages = ["audiotestsrc","autoaudiosink"]
        super(Audio,self).__init__("Audio Pipeline",stages)
