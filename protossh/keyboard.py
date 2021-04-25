import threading
from getch import getch

# TODO: Query host for the supported terminal mode
# https://vt100.net/docs/vt510-rm/DECRQM


class KeyboardReadThread(threading.Thread):

    # Translate keyboard scan codes to ANSI key codes
    #   Key codes: http://microvga.com/ansi-keycodes
    #   ANSI sequences: https://notes.burke.libbey.me/ansi-escape-codes/
    EXTENDED_KEY_MAP = {
        72: '\x1b[A',   # up arrow
        75: '\x1b[D',   # left arrow
        77: '\x1b[C',   # right arrow
        80: '\x1b[B',   # down arrow
    }  # up

    def __init__(self, terminate_queue, chan):
        threading.Thread.__init__(self)
        self.terminate_queue = terminate_queue
        self.chan = chan

    def get_extended_key_map(self, read_key):
        new_key = self.EXTENDED_KEY_MAP.get(ord(read_key), f"<{read_key.decode()}>")
        return new_key

    def run(self):
        is_extended_key = False
        while True:
            read_key = getch()
            send_key = read_key

            if is_extended_key:
                send_key = self.get_extended_key_map(read_key)
                is_extended_key = False

            if read_key == b'\x00':
                is_extended_key = True
                continue

            self.sendall(send_key)
        self.terminate_queue.put(None)

    def sendall(self, content):
        """ try to send to the remote end """
        try:
            self.chan.sendall(content)
        except ex:
            print(ex, file=sys.stderr)
            self.terminate_queue.put(None)