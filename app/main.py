'''
main.py
Description:  Creates a GTK window, attaches a gstreamer AV stream then goes
                  into the GTK main loop to service events and video frames
Called by:    bin/run
Arguments:    A single argument of the stream URL to display
'''

import sys
import urllib.parse
import logging
import graphics.gthread     # Use: loop()
import graphics.display     # Use: AVDisplay(), show()
import graphics.mason


logging.basicConfig(level=logging.DEBUG)
def main():
    '''
    Main program. Hi Lewis!!!
    '''
    if len(sys.argv) <= 1:
        print("Error: supply stream URL.\nUsage:\n\t{0} <url> [<url>...]".format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(-1)
    tiler = graphics.mason.WindowTiler()
    for position, stream in zip(sys.argv[1:len(sys.argv):2], sys.argv[2:len(sys.argv):2]):
        position = int(position)
        title = urllib.parse.urlparse(stream).hostname
        title = "No Title" if title is None else title.split(".")[0]
        logging.info("Starting GTK display for {0} [{1}] at {2}".format(title, stream, position))
        display = graphics.display.AVDisplay(position, "{0} [{1}]".format(title, stream), stream)
        display.initial(*tiler.tile(position))
        display.show()
    logging.info("Entering GTheard loop")
    graphics.gthread.loop()
if __name__ == "__main__":
    main()
