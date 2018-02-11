import av.video
import av.audio
import logging

logging.basicConfig(level=logging.DEBUG)
class AV(av.stream.BaseStream):
    '''
    @author starchmd
    A combined audio source and video stream
    '''
    def __init__(self,window,stream,onerror=lambda msg:1):
        '''
        Initialize the video, and the audio streams
        @param window - window object to draw to
        @param stream - AV stream URL to display
        '''
        logging.debug("Building AV stream")
        self.stream = stream
        stages = [{"name":"soup-1","type":"souphttpsrc","location":stream,"timeout":1},
        #stages = [{"name":"source-1","type":"videotestsrc"},
                  {"name":"decode-1","type":"decodebin",
                      "callback": self.createChild},
                  {"name":"test-src-1","type":"audiotestsrc","nolink":True,"volume":0}]
        self.audios = {}
        self.aplay = False
        self.video = None
        self.audio = None
        self.currentAudio = None
        self.window = window
        super(AV,self).__init__("Global Pipeline",stages,onerror=onerror)
        self.video = av.video.Video(self.window,self.pipeline)
        self.audio = av.audio.Audio(self.pipeline)
        switch = self.audio.getFirstStage()
        testsrc = self.pipeline.get_child_by_name("test-src-1")
        testsrc.link_pads(None,switch,None)
        self.audios["None"] = switch.get_static_pad("sink_{0}".format(switch.get_property("n-pads")-1)) 
    def getAudioStreams(self):
        '''
        Get list of audio streams
        '''
        return sorted(self.audios.keys())
    def getActiveStream(self):
        '''
        Get the current active stream
        @return: current audio stream name
        '''
        if self.currentAudio is None:
            return "None"
        return self.currentAudio
    def switchAudios(self, name, updateCurrent=False):
        '''
        Switch audio streams to named stream
        @param name: name of audio stream
        '''
        if updateCurrent:
            self.currentAudio = name
        if self.currentAudio is None or not self.aplay:
            return
        switch = self.audio.getFirstStage()
        pad = self.audios.get(name, None)
        if not pad is None:
            logging.debug("Switching to audio: {0}".format(pad.get_name()))
            switch.set_property("active-pad",pad)
    def startAudio(self):
        '''
        Start the audio
        '''
        self.aplay = True
        self.switchAudios(self.currentAudio) 
    def stopAudio(self):
        '''
        Stop the audio
        '''
        self.switchAudios("None")
        self.aplay = False
    def createChild(self,parent,pad):
        '''
        Create a child page
        '''
        linkable = None
        logging.debug("Creating dynamic link from type: {0}".format(pad.get_current_caps()[0].get_name()))
        if pad.get_current_caps()[0].get_name().startswith("video"):
            logging.debug("Linking dynamic video")
            child = self.video.getFirstStage()
            parent.link(child)
        elif pad.get_current_caps()[0].get_name().startswith("audio"):
            active = "Audio-{0}".format(len(self.audios.keys()))
            logging.debug("Linking dynamic audio from: {0}".format(active))
            switch = self.audio.getFirstStage()
            parent.link_pads(pad.get_name(),switch,None)
            logging.debug("Assigning {0} to new pad: {1}".format(active,"sink_{0}".format(switch.get_property("n-pads")-1)))
            self.audios[active] = switch.get_static_pad("sink_{0}".format(switch.get_property("n-pads")-1))
            if self.currentAudio is None:
                logging.debug("Setting active audio to: {0}".format(active))
                self.currentAudio = active
            self.switchAudios(self.currentAudio)


