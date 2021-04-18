from .ssh import SSHClient
import colorama

colorama.init()

c = SSHClient()
c.connect("localhost", 2222, "root", "root")
c.run_terminal()
