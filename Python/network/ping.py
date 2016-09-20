import os
import platform

def ping(host):
    """Ping a host, return True if succeed."""

    # figure out the current running platform and adjust 
    # parameter to ping command.
    params = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + params + " " + host) == 0
