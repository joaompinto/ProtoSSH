import argparse

from .ssh import SSHClient
from .console import set_ansi_mode


parser = argparse.ArgumentParser()
parser.add_argument("destination")
parser.add_argument("command", nargs='?', default=None)
parser.add_argument('-K', '--kerberos', action='store_true', help='user kerberos authetication')
parser.add_argument('-p', '--port', type=int, help='ssh server port', default=22)
args = parser.parse_args()


set_ansi_mode()
c = SSHClient()
c.connect(args.destination, args.port, args.kerberos)
if args.command is not None:
    args.command += "\n"
c.run_terminal(args.command)
