import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

import av.stream

class Audio(av.stream.BaseStream):
    '''
    @author starchmd
    Audio stream for audio sink
    '''
    def __init__(self,pipeline):
        '''
        Initialize the GStreamer pipeline
        '''
        stages = [{"name":"input-mux-1","type":"input-selector"},{"name":"audio-sink","type":"autoaudiosink"}]
        super(Audio,self).__init__("Audio Pipeline",stages,pipeline)
