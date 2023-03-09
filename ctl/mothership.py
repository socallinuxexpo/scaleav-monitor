'''
Mothership control code

@author starchmd, mescoops
@date 2018-02-10
'''
import os
import sys
import subprocess
import functools
import re
class MothershipControl(object):
    '''
    Control class for mothership
    @author starchmd, mescoops
    @date 2018-02-10
    '''
    COMMENT_REG = re.compile(r"(#|!|;).*")
    def __init__(self, display):
        '''
        Construct the control
        '''
        self.rooms = {}
        self.display = display
        self.display.set_callbacks(self.shutdown, self.restart_all)
    def configure(self, config):
        '''
        This will configure the application based on the
        passed in configuration file path
        @param config: configuration path
        '''
        self.display.lock()
        seq = 1
        with open(config, "r") as fptr:
            for line in fptr.readlines():
                line = self.COMMENT_REG.sub("", line)
                line =line.strip()
                spl = line.split()
                if line == "": continue
                if len(spl) != 2:
                    print("[ERROR] invalid config line: {0}:{1}".format(config, seq), file=sys.stderr)
                    continue
                power = spl[0].lower() == "on" #specfies room status at boot or reload
                index = str(seq - 1)
                host = spl[1]
                self.rooms[seq] = {"index": index, "process": None, "host": host}
                self.display.add_room(host, functools.partial(self.start, seq),
                                      functools.partial(self.stop, seq), power)
                seq = seq + 1
        self.display.unlock()
    def start(self, key):
        '''
        Starts a service of given host
        @param key: key to index for host to start
        '''
        if not self.rooms[key]["process"] is None and self.rooms[key]["process"].poll() is None:
            raise Exception("Restarting running job: {0}-{1}".format(key, self.rooms[key]["host"]))
        self.rooms[key]["process"] = subprocess.Popen(["python3", "-m", "app.main",
                                                       self.rooms[key]["index"],
                                                       self.rooms[key]["host"]],
                                                      cwd=os.path.join(os.path.dirname(__file__),
                                                                       ".."))
    def restart_all(self):
        '''
        Restarts all processes
        '''
        self.display.lock()
        self.stop_all()
        for key in self.rooms:
            self.start(key)
        self.display.unlock()
    def stop(self, key):
        '''
        Starts a service of given host
        @param key: key to index for host to start
        '''
        if self.rooms[key]["process"] is None:
            return
        self.rooms[key]["process"].kill()
        self.rooms[key]["process"].wait()
    def stop_all(self):
        '''
        Stops all processes
        '''
        for key in self.rooms:
            self.stop(key)
    def shutdown(self):
        '''
        Shutdown processes
        '''
        self.display.lock()
        self.stop_all()
        sys.exit(0)
