import threading
from .console import TerminalStream

BUFFER_SIZE = 4096


class NetworkReadThread(threading.Thread):
    def __init__(self, terminate_queue, chan):
        threading.Thread.__init__(self)
        self.terminate_queue = terminate_queue
        self.chan = chan
        # If the output is long, multi-byte encoded characters may be split
        # across calls to recv, so decode incrementally.
        self.stream = TerminalStream()

    def run(self):
        chan = self.chan
        chan.setblocking(True)
        while True:
            data = chan.recv(BUFFER_SIZE)
            if len(data) == 0:  # Connection was closed
                break
            self.stream.feed(data)
        self.terminate_queue.put(None)
