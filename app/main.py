import graphics.gthread
import graphics.display
import av.av
import av.audio

#Main program
if __name__ == "__main__":
    for stream in ["1","2","3","4","5","6","7"]:
        display = graphics.display.AVDisplay(stream)
        display.show()
    graphics.gthread.loop()
