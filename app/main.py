import graphics.gthread
import graphics.window
import av.av
import av.audio

#Main program
if __name__ == "__main__":
    for stream in ["1","2"]:
        display = graphics.window.Display(stream)
        audio = av.audio.Audio()
        stream = av.av.AV(display,audio)
        display.run()
        audio.start()
        stream.start()
    graphics.gthread.loop()
