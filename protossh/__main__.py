import argparse

from .ssh import SSHClient
from .console import set_ansi_mode


parser = argparse.ArgumentParser()
parser.add_argument("destination")
args = parser.parse_args()


set_ansi_mode()
c = SSHClient()
c.connect(args.destination)
c.run_terminal()
