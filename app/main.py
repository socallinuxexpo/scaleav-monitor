import graphics.gthread
import graphics.display
import av.av
import av.audio
import time
#Main program
if __name__ == "__main__":
    for stream in ["http://192.168.0.109:8080/mixed","http://192.168.0.103:8080","http://192.168.0.108:8080"]*2:
        display = graphics.display.AVDisplay("Title for:"+stream,stream)
        display.show()
        time.sleep(0.5)
    graphics.gthread.loop()
