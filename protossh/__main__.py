from .ssh import SSHClient
import os

import os

if os.name == "nt":  # Only if we are running on Windows
    from ctypes import windll

    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)


# if os.name == 'nt':     # Only if we are running on Windows
#    from ctypes import windll
#    k = windll.kernel32
#    k.SetConsoleMode(k.GetStdHandle(-11), 7)

c = SSHClient()
c.connect("localhost", 3333, "root", "root")
c.run_terminal()
