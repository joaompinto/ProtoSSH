import os
import paramiko
import re
import sys
from queue import Queue
from .network import NetworkReadThread
from .keyboard import KeyboardReadThread


class SSHClient:

    LOGIN_REGEX = ["Last login:", "[@#$:>]"]

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.recv_lcount = 0

    def connect(self, hostname, port=22, username=None, password=None):
        client = self.client
        client.connect(hostname, port=port, username=username, password=password)

    def run_terminal(self):
        self.invoke_shell()  # Start a tty
        self.wait_for_server_data(self.LOGIN_REGEX, verbose=True)
        self.interactive_shell()

    def invoke_shell(self):
        chan = self.client.invoke_shell(term=os.getenv("TERM") or "vt100")
        chan.transport.set_keepalive(10)
        self.chan = chan

    def wait_for_server_data(self, match_list, verbose=False):
        """ Read server data until getting data wich matches a regex from the match_list """
        chan = self.chan
        data = ""
        while True:
            x = chan.recv(1024).decode()
            self.recv_lcount += x.count("\n")
            if len(x) == 0:
                sys.exit(3)
            data += x
            if verbose:
                sys.stdout.write(x)
                sys.stdout.flush()
            for i in range(len(match_list)):
                if re.search(match_list[i], data):
                    return i

    def interactive_shell(self):
        chan = self.chan
        terminate_queue = Queue()

        net_thread = NetworkReadThread(terminate_queue, chan)
        net_thread.setDaemon(True)
        net_thread.start()

        kbd_thread = KeyboardReadThread(terminate_queue, chan)
        kbd_thread.setDaemon(True)
        kbd_thread.start()

        _ = terminate_queue.get()
