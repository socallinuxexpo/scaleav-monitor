from gthread import loop
from window import Display
from video import Video
from audio import Audio
#Main program
if __name__ == "__main__":
    for stream in ["1","2"]:
        display = Display(stream)
        stream = Video(display)
        audio = Audio()
        display.run()
        stream.start()
        audio.start()
    loop()
