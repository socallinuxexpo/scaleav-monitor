'''
Mothership display application

@author lestarch, mescoops
@date 2018-02-10
'''
from __future__ import print_function
import os
import sys
import ctl.mothership
import graphics.mason
import graphics.mothership
import graphics.gthread
import time
def mothership(config):
    '''
    Creates the Mothership control program based on the room configuration
    file supllied to the configuration
    @param config: configuration file in the following format
    
    <room number>	<room video url>
    '''
    position = 3
    tiler = graphics.mason.WindowTiler()
    display = graphics.mothership.MothershipDisplay(position, "Mothership Control")
    control = ctl.mothership.MothershipControl(display)
    display.initial(*tiler.tile(position))
    control.configure(config)
    display.show()
    graphics.gthread.loop()

if __name__ == "__main__":
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
