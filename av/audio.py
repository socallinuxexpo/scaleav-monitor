'''
Module controlling the setup of the audio portion of the stream.

@author: starchmd
@date: 2018-02-14 (refactor)
'''
import logging
import av.stream
import util.log

class Audio(av.stream.BaseStream):
    '''
    @author starchmd
    Audio stream for audio sink
    '''
    def __init__(self, pipeline):
        '''
        Initialize the GStreamer pipeline
        '''
        logging.debug("Creating audio pipeline")
        stages = [{"name":"input-mux-1", "type":"input-selector"},
                  {"name":"audio-converter-1", "type":"audioconvert"},
                  {"name":"audio-sink", "type":"autoaudiosink"}]
        super(Audio, self).__init__("Audio Pipeline", stages, pipeline)
