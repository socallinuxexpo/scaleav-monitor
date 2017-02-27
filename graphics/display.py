import graphics.base
import av.av
import logging

logging.basicConfig(level=logging.DEBUG)

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
        logging.debug("Setting up AV Display")
        self.title = title
        self.stream = stream
        super(AVDisplay,self).__init__(title)
        #Pass in 'self' as window
        self.av = av.av.AV(self,stream)
        logging.debug("Done setting up AV Display")
        print("I am done for:",title,stream,self)
    def show(self):
        '''
        Start the main program
        '''
        logging.debug("Showing AV display")
        super(AVDisplay,self).show()
        self.av.start() 
    def destroy(self,window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        logging.debug("Destroying AV Display, attempting recreation")
        try:
            self.av.stop()
            tmp = AVDisplay(self.title,self.stream)
            tmp.show()
        except Exception as e:
            logging.warning("Failed to stop AV and restart window. {0}:{1}".format(type(e),e))
    def focusIn(self,*args):
       '''
       Focus change event
       '''
       logging.debug("Focus in")
       self.av.startAudio()
    def focusOut(self,*args):
       '''
       Focus change event
       '''
       logging.debug("Focus out")
       self.av.stopAudio()
    def menuCallback(self, item):
        '''
        A callback called when a menu item is clicked
        @param item: menu item name passed back
        '''
        logging.debug("Switching audio to: {0}".format(item))
        self.av.switchAudios(item)
    def getMenuItems(self):
        '''
        Responds with the menu items that should be provided
        to select from
        '''
        #Does nothing, reimplement in child class
        return self.av.getAudioStreams()
