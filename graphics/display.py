import graphics.base
import av.av

class AVDisplay(graphics.base.BaseDisplay):
    '''
    @author starchmd
    A display that shows a video stream and plays audio only on focus.
    '''
    def __init__(self,title,stream):
        '''
        Initialize the window
        @param title - name of window
        '''
        self.title = title
        super(AVDisplay,self).__init__(title)
        #Pass in 'self' as window
        self.av = av.av.AV(self,stream)
    def show(self):
        '''
        Start the main program
        '''
        super(AVDisplay,self).show()
        self.av.startVideo() 
    def destroy(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        self.av.stopAll()
        tmp = AVDisplay(self.title)
        tmp.show()
    def focusIn(self,*args):
       '''
       Focus change event
       '''
       #self.av.startAudio()
    def focusOut(self,*args):
       '''
       Focus change event
       '''
       #self.av.stopAudio()
