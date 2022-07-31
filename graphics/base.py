'''
A module to encapsulate the base-display code for the monitoring
system's Gtk usage, windowing environment, and interaction code.

@author starchmd
'''
import os
import logging
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import util.log


class BaseDisplay(object):
    '''
    A base display window built on GTK containing a drawing area
    for GStream or anything else to draw in.
    @author starchmd
    @date 2018-02-11 (refactored)
    '''
    def __init__(self, title):
        '''
        Initialize the window
        @param title - name of window
        '''
        self.window = Gtk.Window()
        #Connect callbacks
        self.window.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window.connect("destroy", self.destroy)
        self.window.connect("focus-in-event", self.focus_in)
        self.window.connect("focus-out-event", self.focus_out)
        self.window.connect("key-press-event", self.key_pressed)

        self.window.set_title(title)
        self.title = title
    def initial(self, screen, position, dimension):
        '''
        Set the initial screen, position, and dimensions
        @param screen: screen to display on
        @param position: (x, y) position
        @param dimension: (width, height) dimension of window
        '''
        self.window.resize(*dimension)
        self.window.move(*position)
        self.window.set_screen(screen)
    def show(self):
        '''
        Start the main program
        '''
        self.window.show_all()
    def destroy(self, window):
        '''
        Quit function, GTK quit callback
        @param window - supplied by Gtk, window object
        '''
        pass
    def focus_in(self, *args):
        '''
        Focus change event
        '''
        pass
    def focus_out(self, *args):
        '''
        Focus change event
        '''
        pass
    def key_pressed(self, *args):
        '''
        Do nothing key-press
        '''
        pass
class DrawableDisplay(BaseDisplay):
    '''
    A display that allows for drawing to the window, and represents a single unit of
    display size for the standard "tiled" displays.

    @author starchmd
    @date 2018-02-11
    '''
    def __init__(self, index, title):
        '''
        Construct the drawable display based on its tiling-index and
        title
        @param index: index into tiling display
        @param title: title of the window
        '''
        self.menu = []
        self.index = index
        #Why is super last? Setup is called by parent, *and* index must be set first
        super(DrawableDisplay, self).__init__(title)

        # Create an overlay window to put our 'loading' splash screen on
        self.overlay = Gtk.Overlay()
        self.window.add(self.overlay)
        self.win_splash = Gtk.Box()
        self.overlay.add_overlay(self.win_splash)
        self.img_splash = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "stop.jpg"))
        self.overlay.set_overlay_pass_through(self.win_splash, True)
        self.win_splash.pack_start(self.img_splash, True, True, 0)

        # Create a top level window to hold the drawing and controls windows
        self.win_full_screen = Gtk.Box()
        self.overlay.add(self.win_full_screen)

        #Create a drawable area used to fill with video data
        self.win_video = Gtk.DrawingArea()
        self.win_video.set_double_buffered(True)
        self.win_video.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.win_video.connect("button-press-event", self.build_menu)
        self.win_full_screen.pack_start(self.win_video, True, True, 0)

        # Create a grid object to hold the controls
        self.win_controls = Gtk.Grid()
        self.win_full_screen.pack_end(self.win_controls, False, False, 0)

        # Create the control widgets
        #   Enable controls (R/W)
        self.win_switches = Gtk.Grid()
        self.win_controls.add(self.win_switches)
        self.ctl_enable = Gtk.Button();
        self.img_enable = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "dangernoodle-400x400.jpg"))
        self.ctl_enable.add(self.img_enable);
        # self.label_rw = Gtk.Label(label="enable")
        self.win_switches.attach(self.ctl_enable, 0, 0, 1, 1)
        # self.ctl_rw = Gtk.Switch()
        # self.win_switches.attach(self.ctl_rw, 1, 0, 1, 1)
        #   Toggle video buffering
        self.label_buffering = Gtk.Label(label="Buffering")
        self.win_switches.attach(self.label_buffering, 0, 1, 1, 1)
        self.ctl_buffering = Gtk.Switch()
        self.win_switches.attach(self.ctl_buffering, 1, 1, 1, 1)
        #   Toggle slides
        self.label_slides = Gtk.Label(label="Slides")
        self.win_switches.attach(self.label_slides, 0, 2, 1, 1)
        self.ctl_slides = Gtk.Switch()
        self.win_switches.attach(self.ctl_slides, 1, 2, 1, 1)
        #   Choose view (slide/video/muxed)
        self.label_view = Gtk.Label(label="View")
        self.win_switches.attach(self.label_view, 0, 3, 1, 1)
        self.ctl_view_slides = Gtk.RadioButton.new_with_label_from_widget(None, "Slides")
        self.ctl_view_slides.connect("toggled", self.on_view_toggled, "1")
        self.win_switches.attach(self.ctl_view_slides, 0, 4, 1, 1)
        self.ctl_view_video = Gtk.RadioButton.new_with_label_from_widget(self.ctl_view_slides, "Video")
        self.ctl_view_video.connect("toggled", self.on_view_toggled, "2")
        self.win_switches.attach(self.ctl_view_video, 0, 5, 1, 1)
        self.ctl_view_mixed = Gtk.RadioButton.new_with_label_from_widget(self.ctl_view_slides, "Mixed")
        self.ctl_view_mixed.connect("toggled", self.on_view_toggled, "3")
        self.win_switches.attach(self.ctl_view_mixed, 0, 6, 1, 1)
        # self.ctl_view_mixed.set_active(True)
        #   8 camera controls
        self.win_camera = Gtk.Grid()
        self.win_controls.add(self.win_camera)
        self.ctl_cam_up = Gtk.Button();
        self.img_cam_up = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_up.jpeg"))
        self.ctl_cam_up.add(self.img_cam_up);
        self.win_camera.attach(self.ctl_cam_up, 1, 0, 1, 1)
        self.ctl_cam_down = Gtk.Button();
        self.img_cam_down = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_down.jpeg"))
        self.ctl_cam_down.add(self.img_cam_down);
        self.win_camera.attach(self.ctl_cam_down, 1, 2, 1, 1)
        self.ctl_cam_left = Gtk.Button();
        self.img_cam_left = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_left.jpeg"))
        self.ctl_cam_left.add(self.img_cam_left);
        self.win_camera.attach(self.ctl_cam_left, 0, 1, 1, 1)
        self.ctl_cam_right = Gtk.Button();
        self.img_cam_right = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_right.jpeg"))
        self.ctl_cam_right.add(self.img_cam_right);
        self.win_camera.attach(self.ctl_cam_right, 2, 1, 1, 1)
        self.ctl_cam_in = Gtk.Button();
        self.img_cam_in = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_in.png"))
        self.ctl_cam_in.add(self.img_cam_in);
        self.win_camera.attach(self.ctl_cam_in, 0, 2, 1, 1)
        self.ctl_cam_out = Gtk.Button();
        self.img_cam_out = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_out.jpeg"))
        self.ctl_cam_out.add(self.img_cam_out);
        self.win_camera.attach(self.ctl_cam_out, 2, 2, 1, 1)
        self.ctl_cam_go_home = Gtk.Button();
        self.img_cam_go_home = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_home.jpeg"))
        self.ctl_cam_go_home.add(self.img_cam_go_home);
        self.win_camera.attach(self.ctl_cam_go_home, 2, 3, 1, 1)
        self.ctl_cam_set_home = Gtk.Button();
        self.img_cam_set_home = Gtk.Image.new_from_file(str(Path(__file__).parent.parent / "img" / "button_set.jpeg"))
        self.ctl_cam_set_home.add(self.img_cam_set_home);
        self.win_camera.attach(self.ctl_cam_set_home, 0, 3, 1, 1)
        #   N audio controls and meters
        self.win_audio = Gtk.Grid()
        self.win_controls.add(self.win_audio)
        self.label_audio = Gtk.Label(label="Audio")
        self.win_audio.add(self.label_audio)
        #   Overflow stop/start/choose who
        self.win_overflow = Gtk.Grid()
        self.win_controls.add(self.win_overflow)
        self.label_overflow = Gtk.Label(label="Overflow")
        self.win_overflow.attach(self.label_overflow, 0, 0, 1, 1)
        self.ctl_overflow_stop = Gtk.Button(label="Stop")
        self.win_overflow.attach(self.ctl_overflow_stop, 0, 1, 1, 1)
        self.ctl_overflow_start = Gtk.Button(label="Start")
        self.win_overflow.attach(self.ctl_overflow_start, 0, 2, 1, 1)

        # Calculate the final layout
        self.xid = None
    def on_view_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("View ", name, " was switched to ", state)
    def show(self):
        '''
        Show function
        '''
        super(DrawableDisplay, self).show()
        # Save the XID of the video drawing widget
        self.xid = self.win_video.get_window().get_xid()
    def get_xid(self):
        '''
        Gets the X11 window ID
        '''
        return self.xid
    def build_menu(self, _, event):
        '''
        Builds the menu upon creation during a right click
        @param event: click event triggering this
        '''
        #Ignore all but third button clicks (right click)
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 3:
            return
        #Create a new menu from the responded items
        self.menu = Gtk.Menu()
        for label in self.get_menu_items():
            item = Gtk.CheckMenuItem(label)
            if label == self.get_current_item():
                item.set_active(True)
            item.connect("button-press-event", self.menu_click)
            self.menu.append(item)
        #Force menu to pop up with all items displayed
        self.menu.show_all()
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def get_menu_items(self):
        '''
        List of menu items
        '''
        return []
    def get_current_item(self):
        '''
        Gets menu item to display as checked
        '''
        return None
    def menu_click(self, selected, event):
        '''
        A callback handling the GTK events and passing through to a callback
        that only needs to deal with the menu item name.
        @param selected: menu item clicked
        @param event: mouse event
        '''
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1:
            return
        for item in self.menu:
            item.set_active(False)
        selected.set_active(True)
        self.menu_callback(selected.get_label())
    def menu_callback(self, item):
        '''
        What to do when menu is clicked. Virtual function/
        @param item: menu item name which was clicked
        '''
        pass
