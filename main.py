from window import Display
from stream import Stream

#Main program
if __name__ == "__main__":
    display = Display()
    stream = Stream(display)

    display.run()
    stream.run()

    display.loop()
