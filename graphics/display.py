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
        print("I am for:",title,stream,self)
        self.title = title
        self.stream = stream
        super(AVDisplay,self).__init__(title)
        #Pass in 'self' as window
        self.av = av.av.AV(self,stream)
        print("I am done for:",title,stream,self)
    def show(self):
        '''
        Start the main program
        '''
        print("Showing:",self)
        super(AVDisplay,self).show()
        self.av.start() 
    def destroy(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        print("Killing:",self)
        try:
            self.av.stop()
            tmp = AVDisplay(self.title,self.stream)
            tmp.show()
        except:
            print("I AM MAD")
            pass
    def focusIn(self,*args):
       '''
       Focus change event
       '''
       print("Focus In:",self)
       self.av.startAudio()
    def focusOut(self,*args):
       '''
       Focus change event
       '''
       print("Focus Out:",self)
       self.av.stopAudio()
    def menuCallback(self, item):
        '''
        A callback called when a menu item is clicked
        @param item: menu item name passed back
        '''
        self.av.switchAudios(item)
    def getMenuItems(self):
        '''
        Responds with the menu items that should be provided
        to select from
        '''
        #Does nothing, reimplement in child class
        return self.av.getAudioStreams()
