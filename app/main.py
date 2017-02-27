import graphics.gthread
import graphics.display
import av.av
import av.audio
import sys
import time
import urllib.parse
#Main program
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: please supplu stream URL.\nUsage:\n\t{0} <url> [<url>...]".format(sys.argv[0]),file=sys.stderr)
        sys.exit(-1)
    for stream in sys.argv[1:]:
        title = urllib.parse.urlparse(stream).hostname
        title = "No Title" if title is None else title.split(".")[0]
        display = graphics.display.AVDisplay("{0} [{1}]".format(title,stream),stream)
        display.show()
        time.sleep(0.5)
    graphics.gthread.loop()
