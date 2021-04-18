import threading
import sys


class NetworkReadThread(threading.Thread):
    def __init__(self, terminate_queue, chan):
        threading.Thread.__init__(self)
        self.terminate_queue = terminate_queue
        self.chan = chan

    def run(self):
        chan = self.chan
        chan.setblocking(True)
        while True:
            x = chan.recv(1024).decode()
            if len(x) == 0:  # Connection was closed
                break
            sys.stdout.write(x)
            sys.stdout.flush()
        self.terminate_queue.put(None)
