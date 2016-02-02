import graphics.gthread
import graphics.window
import av.video
import av.audio
#Main program
if __name__ == "__main__":
    for stream in ["1","2"]:
        display = graphics.window.Display(stream)
        stream = av.video.Video(display)
        audio = av.audio.Audio()
        display.run()
        stream.start()
        audio.start()
    graphics.gthread.loop()
