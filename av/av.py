import av.video
import av.audio
count=1
class AV():
    '''
    @author starchmd
    A combined audio source and video stream
    '''
    def __init__(self,window):
        '''
        Initialize the video, and the audio streams
        @param window - window object to draw to
        '''
        global count
        self.audio = av.audio.Audio()
        self.video = av.video.Video(window)
        self.audio.pipeline.get_child_by_name("0").set_property("freq",100*count)
        count=count+1
    def startAudio(self):
        '''
        Start the audio
        '''
        self.audio.start()
    def stopAudio(self):
        '''
        Stop the audio
        '''
        self.audio.stop()
    def startVideo(self):
        '''
        Start the video
        '''
        self.video.start()
    def stopVideo(self):
        '''
        Stop the video
        '''
        self.video.stop()
    def startAll(self):
        '''
        Start streams
        '''
        self.video.start()
        self.audio.start()
    def stopAll(self):
        '''
        Stop streams
        '''
        self.video.stop()
        self.audio.stop()
#       window.registerGainFocus(self.gainFocus)
#       window.registerLoseFocus(self.loseFocus)
#       window.registerQuit(self.stopAll)
#    def startVideo(self):
#        '''
#        Starts the video stream
#        '''
#        self.video.start()
#    def stopAll(self):
#        '''
#        Stops all streams
#        '''
#        self.video.stop()
#        self.audio.stop()
#    def gainFocus(self):
#        '''
#        Gain focus to controlling window
#        '''
#        self.audio.start()
#    def loseFocus(self):
#        '''
#        Lose the focuse to controlling window
#        '''
#        self.audio.stop()
