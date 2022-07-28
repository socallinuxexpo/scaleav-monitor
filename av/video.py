'''
Module used to setup and handle the video portion of the
pipeline.

@author starchmd
@date 2018-02-14 (refactor)
'''
import logging
import av.stream
import util.log

class Video(av.stream.BaseStream):
    '''
    @author starchmd
    Stream GStream pipline to window
    '''
    def __init__(self, window, pipeline):
        '''
        Initialize the GStreamer pipeline
        @param window - window object to draw to
        '''
        logging.debug("Setting up video stream")
        self.window = window
        stages = [
            {"name": "intelpostproc-1", "type": "vaapipostproc"},
            {"name":"autosink-1", "type":"xvimagesink"}]
        super(Video, self).__init__("Video Pipeline", stages, pipeline)
    def on_sync(self, bus, msg):
        '''
        What to do on sync requests
        @param bus - bus relaying message
        @param msg - message sent
        '''
        if msg.get_structure().get_name() == "prepare-window-handle":
            xid = self.window.get_xid()
            if xid is None:
                logging.warning("Started video stream before window creation")
                raise Exception("Error: Stream play before window creation")
            msg.src.set_window_handle(xid)
