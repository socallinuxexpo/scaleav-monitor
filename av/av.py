'''
Module containing the functions for build a combined audio/visual stream.

@author starchmd
@date 2018-02-14 (refactor)
'''
import logging
import av.video
import av.audio
import util.log

class AV(av.stream.BaseStream):
    '''
    @author starchmd
    A combined audio source and video stream
    '''
    def __init__(self, window, stream, onerror=lambda msg: 1):
        '''
        Initialize the video, and the audio streams
        @param window - window object to draw to
        @param stream - AV stream URL to display
        '''
        logging.debug("Building AV stream")
        self.stream = stream
        stages = [{"name":"rtmp-1", "type":"rtmpsrc", "location":stream, "timeout":1},
                  {"name":"decode-1", "type":"decodebin", "callback": self.create_child},
                  {"name":"test-src-1", "type":"audiotestsrc", "nolink":True, "volume":0}]
        self.audios = {}
        self.aplay = False
        self.video = None
        self.audio = None
        self.current_audio = None
        self.window = window
        super(AV, self).__init__("Global Pipeline", stages, onerror=onerror)
        self.video = av.video.Video(self.window, self.pipeline)
        self.audio = av.audio.Audio(self.pipeline)
        switch = self.audio.get_first_stage()
        testsrc = self.pipeline.get_child_by_name("test-src-1")
        testsrc.link_pads(None, switch, None)
        full_sink = "sink_{0}".format(switch.get_property("n-pads") - 1)
        self.audios["None"] = switch.get_static_pad(full_sink)
    def get_audio_streams(self):
        '''
        Get list of audio streams
        @return: list of available audio streams
        '''
        return sorted(self.audios.keys())
    def get_active_stream(self):
        '''
        Get the current active stream
        @return: current audio stream name
        '''
        if self.current_audio is None:
            return "None"
        return self.current_audio
    def switch_audios(self, name, update_current=False):
        '''
        Switch audio streams to named stream
        @param name: name of audio stream
        '''
        if update_current:
            self.current_audio = name
        if self.current_audio is None or not self.aplay:
            return
        switch = self.audio.get_first_stage()
        pad = self.audios.get(name, None)
        if not pad is None:
            logging.debug("Switching to audio: %s", pad.get_name())
            switch.set_property("active-pad", pad)
    def start_audio(self):
        '''
        Start the audio
        '''
        self.aplay = True
        self.switch_audios(self.current_audio)
    def stop_audio(self):
        '''
        Stop the audio
        '''
        self.switch_audios("None")
        self.aplay = False
    def create_child(self, parent, pad):
        '''
        Create a child page
        '''
        logging.debug("Creating dynamic link from type: %s", pad.get_current_caps()[0].get_name())
        if pad.get_current_caps()[0].get_name().startswith("video"):
            logging.debug("Linking dynamic video")
            child = self.video.get_first_stage()
            parent.link(child)
        elif pad.get_current_caps()[0].get_name().startswith("audio"):
            active = "Audio-{0}".format(len(self.audios.keys()))
            logging.debug("Linking dynamic audio from: %s", active)
            switch = self.audio.get_first_stage()
            parent.link_pads(pad.get_name(), switch, None)
            full_sink = "sink_{0}".format(switch.get_property("n-pads") - 1)
            logging.debug("Assigning %s to new pad: %s", str(active), full_sink)
            self.audios[active] = switch.get_static_pad(full_sink)
            if self.current_audio is None:
                logging.debug("Setting active audio to: %s", active)
                self.current_audio = active
            self.switch_audios(self.current_audio)
