import av.video
import av.audio
class AV(av.stream.BaseStream):
    '''
    @author starchmd
    A combined audio source and video stream
    '''
    def __init__(self,window,stream):
        '''
        Initialize the video, and the audio streams
        @param window - window object to draw to
        @param stream - AV stream URL to display
        '''
        self.stream = stream
        stages = [{"name":"soup-1","type":"souphttpsrc","location":stream},
        #stages = [{"name":"source-1","type":"videotestsrc"},
                  {"name":"decode-1","type":"decodebin",
                      "callback": self.createChild},
                  {"name":"test-src-1","type":"audiotestsrc","nolink":True,"volume":0}]
        self.audios = {}
        self.video = None
        self.audio = None
        self.currentAudio = None
        self.window = window
        super(AV,self).__init__("Global Pipeline",stages)
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
    def switchAudios(self, name):
        '''
        Switch audio streams to named stream
        @param name: name of audio stream
        '''
        if self.currentAudio is None:
            return
        #self.stop()
        #Unlink current
        #pad = self.audios[self.currentAudio]
        #parent.unlink(self.audio.getFirstStage())
        switch = self.audio.getFirstStage()
        #switch.emit("block")
        print("Doing: ",name)
        if name != "None":
            self.currentAudio = name
        pad = self.audios[name]
        print("Switching to Pad: ",pad.get_name())
        switch.set_property("active-pad",pad)
        #self.start()
    def startAudio(self):
        '''
        Start the audio
        '''
        self.switchAudios(self.currentAudio) 
    def stopAudio(self):
        '''
        Stop the audio
        '''
        self.switchAudios("None")
    def createChild(self,parent,pad):
        '''
        Create a child page
        '''
        print("CAPS:",pad.get_current_caps()[0].get_name())
        linkable = None
        if pad.get_current_caps()[0].get_name().startswith("video"):
            child = self.video.getFirstStage()
            print("Linking video: ",child)
            parent.link(child)
        elif pad.get_current_caps()[0].get_name().startswith("audio"):
            active = "Audio-{0}".format(len(self.audios.keys()))
            switch = self.audio.getFirstStage()
            parent.link_pads(pad.get_name(),switch,None)
            self.audios[active] = switch.get_static_pad("sink_{0}".format(switch.get_property("n-pads")-1))
            print("Audio Active: ",self.audios[active].get_name())
            if self.currentAudio is None:
                self.currentAudio = active
