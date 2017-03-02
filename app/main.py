#!/usr/bin/env python3

'''
main.py
Description:  Creates a GTK window, attaches a gstreamer AV stream then goes
                  into the GTK main loop to service events and video frames
Called by:    bin/run
Arguments:    A single argument of the stream URL to display
'''

import graphics.gthread     # Use: loop()
import graphics.display     # Use: AVDisplay(), show()
import av.av
import av.audio
import sys
import time
import urllib.parse
import logging

logging.basicConfig(level=logging.DEBUG)

#Main program
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: please supply stream URL.\nUsage:\n\t{0} <url> [<url>...]".format(sys.argv[0]),file=sys.stderr)
        sys.exit(-1)
    for stream in sys.argv[1:]:
        title = urllib.parse.urlparse(stream).hostname
        title = "No Title" if title is None else title.split(".")[0]
        logging.info("Starting GTK display for {0} [{1}]".format(title,stream))
        display = graphics.display.AVDisplay("{0} [{1}]".format(title,stream),stream)
        display.show()
        time.sleep(0.5)
    logging.info("Entering GTheard loop")
    graphics.gthread.loop()

