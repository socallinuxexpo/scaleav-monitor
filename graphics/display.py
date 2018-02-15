import logging
import graphics.base
import graphics.mason
import av.av
import gi
gi.require_version("Gst", "1.0")
from gi.repository import  GObject, Gst

RETRY_INTERVAL_MS = 1000

logging.basicConfig(level=logging.DEBUG)

class AVDisplay(graphics.base.DrawableDisplay):
    '''
    @author starchmd
    A display that shows a video stream and plays audio only on focus.
    '''
    def __init__(self, index, title, stream):
        '''
        Initialize the window
        @param title - name of window
        '''
        logging.debug("Setting up AV Display")
        self.title = title
        self.stream = stream
        super(AVDisplay, self).__init__(index, title)
        #Pass in 'self' as window
        logging.debug("Done setting up AV Display")
        self.retrying = False
        self.avs = None
        self.start()
    def show(self):
        '''
        Start the main program
        '''
        super(AVDisplay, self).show()
        #Must be done on same thread as the above UI
        if not self.avs is None:
            def start_stream(stream):
                '''Run on GUI thread'''
                self.img.hide()
                stream.start()
            GObject.idle_add(start_stream, self.avs)
    def start(self):
        '''
        Start the stream running
        '''
        if not self.avs is None:
            self.avs.stop()
        self.avs = av.av.AV(self, self.stream, onerror=self.on_error)
        self.avs.start()
        if self.window.is_active():
            self.avs.start_audio()
    def on_error(self, msg):
        '''
        What to do when the stream errors
        @param msg: message containing error
        '''
        def show_img(*args):
            '''Callback to show image'''
            self.img.show()
        GObject.idle_add(show_img, None)
        if self.retrying:
            return
        for message in ["Stream doesn't contain enough data", "Internal data flow error"]:
            if message in str(msg.parse_error()):
                break
        else:
            return
        if not self.avs is None:
            self.avs.stop()
        self.retrying = True
        GObject.timeout_add(RETRY_INTERVAL_MS, self.retry_connection, None)
    def retry_connection(self, *args):
        '''
        Retry connection on disconnect
        '''
        state = self.avs.pipeline.get_state(0).state
        if state == Gst.State.PLAYING:
            self.img.hide()
            self.retrying = False
            return False
        self.start()
        return True
    def destroy(self, window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        logging.debug("Destroying AV Display, attempting recreation")
        try:
            if not self.avs is None:
                self.avs.stop()
            tmp = AVDisplay(self.index, self.title, self.stream)
            tmp.initial(*graphics.mason.WindowTiler().tile(self.index))
            tmp.show()
        except Exception as exc:
            logging.warning("Failed to stop AV and restart window. %s:%s", type(exc), str(exc))
    def focus_in(self, *args):
        '''
        Focus change event
        '''
        if not self.avs is None:
            logging.debug("Attempting to start Audio")
            self.avs.start_audio()
    def focus_out(self, *args):
        '''
        Focus change event
        '''
        if not self.avs is None:
            logging.debug("Attempting to stop Audio")
            self.avs.stop_audio()
    def menu_callback(self, item):
        '''
        A callback called when a menu item is clicked
        @param item: menu item name passed back
        '''
        logging.debug("Switching audio to: %s", item)
        if not self.avs is None:
            self.avs.switch_audios(item, update_current=True)
    def get_menu_items(self):
        '''
        Responds with the menu items that should be provided
        to select from
        '''
        if self.avs is None:
            return []
        return self.avs.get_audio_streams()
    def get_current_item(self):
        '''
        Responds with the menu items that should be checked
        '''
        if self.avs is None:
            return ""
        return self.avs.get_active_stream()
    def key_pressed(self, window, kevent):
        '''
        Handle number presses for switching audio.
        '''
        streams = self.avs.get_audio_streams()
        if kevent.keyval in [65456, 48] and len(streams) >= 1:
            self.avs.switch_audios(streams[len(streams) - 1], update_current=True)
        if kevent.keyval in [65457, 49] and len(streams) >= 2:
            self.avs.switch_audios(streams[0], update_current=True)
        if kevent.keyval in [65458, 50] and len(streams) >= 3:
            self.avs.switch_audios(streams[1], update_current=True)
