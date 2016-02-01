import gi
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

#Global initializations
Gst.init(None)

class Stream(object):
    '''
    @author starchmd
    Stream GStream pipline to window
    '''
    def __init__(self,window):
        '''
        Initialize the GStreamer pipeline
        '''
        self.window = window
        self.stages = [{
                         "name":"video-source",
                         "handler":"videotestsrc",
                         "source":True
                       },
                       {
                         "name":"video-sink",
                         "handler":"ximagesink",
                         "sink":True
                       }]
        self.pipeline = Gst.Pipeline("audio-pipeline")
        last=None
        for stage in self.stages:
            print("Building stage: ",stage["handler"])
            stage["element"] = Gst.ElementFactory.make(stage["handler"],stage["name"])
            self.pipeline.add(stage["element"])
            if not last is None:
                last.link(stage["element"])
            if "source" in stage:
                self.source = stage["element"]
            if "sink" in stage:
                self.sink = stage["element"]
            last=stage["element"]
        #Setup busses
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::error",self.onError)
        #TODO: Handel EOS (message::eos)
        bus.enable_sync_message_emission()
        bus.connect("sync-message::element",self.onSync)
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
    def onError(self,bus,msg):
        '''
        What to do on errors
        @param bus - bus relaying message
        @param msg - message sent
        '''
        print("Error:",msg.parse_error())
    def run(self):
        '''
        Runs the stream
        '''
        self.pipeline.set_state(Gst.State.PLAYING)
