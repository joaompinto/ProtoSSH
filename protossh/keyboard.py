import threading
from getch import getch


class KeyboardReadThread(threading.Thread):
    def __init__(self, terminate_queue, chan):
        threading.Thread.__init__(self)
        self.terminate_queue = terminate_queue
        self.chan = chan

    def run(self):
        while True:
            key = getch()
            # Handle CTRL-C while running in debug mode
            # if key == b"\x03":
            #    break
            self.chan.sendall(key)
        self.terminate_queue.put(None)
