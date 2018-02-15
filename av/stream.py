'''
Base stream class used to handle the basic functions of GST processing.

@author starchmd
@data: 2018-02-14 (refactor)
'''
import logging
import gi
gi.require_version("Gst", "1.0")
from gi.repository import  Gst

logging.basicConfig(level=logging.DEBUG)

class BaseStream(object):
    '''
    @author starchmd
    Base GStreamer stream
    '''
    def __init__(self, name, stages, pipeline=None, onerror=lambda msg: 1):
        '''
        Initializes this pipeline
        @param name - name of the pipeline
        @param stages - ordered list of gst elements names in the pipeline
        '''
        logging.debug("Building base stream")
        self.running = None
        self.errorfn = onerror
        self.stages = stages
        self.pipeline = pipeline
        self.build(name, stages)
    def build(self, name, stages):
        '''
        Build the GStreamer pipeline
        @param name - name of the pipeline
        @param stages - ordered list of gst elements names in the pipeline
        '''
        if self.pipeline is None:
            self.pipeline = Gst.Pipeline(name)
        logging.info("Building pipeline from: %s", str(stages))
        #Basic bus setup
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::error", self.on_error)
        self.bus.connect("message::eos", self.on_error)
        self.bus.enable_sync_message_emission()
        self.bus.connect("sync-message::element", self.on_sync)
        #Build the stages
        for index, stage in enumerate(stages):
            elem = Gst.ElementFactory.make(stage["type"], stage["name"])
            for sname, prop in stage.items():
                if sname == "type" or sname == "callback" or sname == "nolink":
                    continue
                elem.set_property(sname, prop)
            #Register callback on decode create
            if "callback" in stage:
                BaseStream.register_dynamic_callback(stage, elem)
            self.pipeline.add(elem)
            if index > 0 and not "callback" in stages[index-1] and \
               not stages[index].get("nolink", False):
                logging.debug("Linking %s to %s", stages[index-1]["name"], elem.get_name())
                self.pipeline.get_child_by_name(stages[index-1]["name"]).link(elem)
        self.running = False
    @staticmethod
    def register_dynamic_callback(stage, elem):
        '''
        Separate function for registering callback on new pad. Used to get around
        python's loose scooping rules in loops
        @param stage: stage to be registered as a callback
        @param elem: element tp connect on pad
        '''
        def on_new_decoded_pad(dbin, pad):
            '''
            Function called on the discovery of a new pad
            @param dbin: decoder binary discovering pad
            @param pad: pad discovered
            '''
            logging.debug("Setting up dynamic pad: %s on %s", pad.get_name(), dbin.get_name())
            decode = pad.get_parent()
            #pipeline = decode.get_parent()
            stage(decode, pad)
        elem.connect("pad-added", on_new_decoded_pad)

    def get_first_stage(self):
        '''
        Get the first stage of this portion of the pipeline
        '''
        return self.pipeline.get_child_by_name(self.stages[0]["name"])
    def on_sync(self, bus, msg):
        '''
        What to do on sync requests
        @param bus - bus relaying message
        @param msg - message sent
        '''
        pass
    def on_error(self, bus, msg):
        '''
        What to do on errors
        @param bus - bus relaying message
        @param msg - message sent
        '''
        logging.warning("Error received on BUS %s: %s", bus.get_name(), msg.parse_error())
        self.errorfn(msg)
    def start(self):
        '''
        Runs the stream
        '''
        if self.running is None:
            logging.warning("Trying to run an un-built stream")
            raise StreamNotBuiltException()
        logging.info("Running pipeline: %s", self.pipeline.get_name())
        self.running = True
        self.pipeline.set_state(Gst.State.PLAYING)
    def stop(self):
        '''
        Stop the stream
        '''
        if self.running is None:
            logging.warning("Trying to stop an un-built stream")
            raise StreamNotBuiltException()
        logging.info("Stopping pipeline: %s", self.pipeline.get_name())
        self.pipeline.set_state(Gst.State.NULL)
        self.running = False
class StreamNotBuiltException(Exception):
    '''
    @author starchmd
    An exception thrown when the stream is not built but other functions are called
    '''
    pass
