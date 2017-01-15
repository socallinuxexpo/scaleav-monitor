import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

import av.stream

class Audio(av.stream.BaseStream):
    '''
    @author starchmd
    Audio stream for audio sink
    '''
    def __init__(self):
        '''
        Initialize the GStreamer pipeline
        '''
        stages = [] #{"type":"audiotestsrc"},{"type":"autoaudiosink"}]
        super(Audio,self).__init__("Audio Pipeline",stages)
