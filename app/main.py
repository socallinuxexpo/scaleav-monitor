import graphics.gthread
import graphics.display
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
    for stream in sys.argv[1:4]:
        title = urllib.parse.urlparse(stream).hostname
        title = "No Title" if title is None else title.split(".")[0]
        logging.info("Starting GTK display for {0} [{1}]".format(title,stream))
        display = graphics.display.AVDisplay("{0} [{1}]".format(title,stream),stream)
        display.show()
        #display.start()
        #time.sleep(2)
    logging.info("Entering GTheard loop")
    graphics.gthread.loop()
