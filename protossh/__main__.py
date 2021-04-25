from .ssh import SSHClient
from .console import set_ansi_mode


set_ansi_mode()
c = SSHClient()
c.connect("localhost", 3333, "root", "root")
c.run_terminal()
