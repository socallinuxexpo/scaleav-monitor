from window import Display
from stream import Stream
from gthread import loop
#Main program
if __name__ == "__main__":
    for stream in ["1","2"]:
        display = Display(stream)
        stream = Stream(display)
        display.run()
        stream.run()
    loop()
