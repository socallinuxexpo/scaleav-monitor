'''
Mothership display application

@author starchmd, mescoops
@date 2018-02-10
'''
from __future__ import print_function
import os
import sys
import ctl.mothership
import graphics.mason
import graphics.mothership
import graphics.gthread
def mothership(config):
    '''
    Creates the Mothership control program based on the room configuration
    file supllied to the configuration
    @param config: configuration file in the following format

    <room number>	<room video url>
    '''
    tiler = graphics.mason.WindowTiler()
    display = graphics.mothership.MothershipDisplay("Mothership Control")
    control = ctl.mothership.MothershipControl(display)
    display.initial(*tiler.unindexed_tile())
    control.configure(config)
    display.show()
    graphics.gthread.loop()
def main():
    '''
    Main program. Hi Lewis!!!
    '''
    config = os.path.join(os.path.dirname(__file__), "..", "config", "rooms")
    if len(sys.argv) > 2:
        print("[ERROR] Too many arguments supplied. Supply configuration or nothing")
        sys.exit(-1)
    elif len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        print("[ERROR] Cannot find configuration", sys.argv[1])
        sys.exit(-1)
    elif len(sys.argv) == 2:
        config = sys.argv[1]
    mothership(config)

if __name__ == "__main__":
    main()
