import av.video
import av.audio
#Note: count is used for the tone ladder audio test code below
count=1
class AV():
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
        global count
        self.stream = stream
        self.audio = av.audio.Audio()
        self.video = av.video.Video(window,self.stream)
        #self.audio.pipeline.get_child_by_name("0").set_property("freq",100*count)
        count=count+1
    def startAudio(self):
        '''
        Start the audio
        '''
        #self.audio.start()
    def stopAudio(self):
        '''
        Stop the audio
        '''
        #self.audio.stop()
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
        #self.audio.start()
    def stopAll(self):
        '''
        Stop streams
        '''
        self.video.stop()
        #self.audio.stop()
