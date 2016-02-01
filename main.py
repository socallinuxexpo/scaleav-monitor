from gthread import loop
from window import Display
from video import Video
#Main program
if __name__ == "__main__":
    for stream in ["1","2"]:
        display = Display(stream)
        stream = Video(display)
        display.run()
        stream.start()
    loop()
