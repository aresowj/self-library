import os
import platform

def ping(host):
    """Ping a host, return True if succeed."""

    # figure out the current running platform and adjust 
    # parameter to ping command.
    if platform.system().lower()=="windows":
        ping_str = "ping -n 1 -w 2000 " + host
    else:
        ping_str = "ping -c 1 -t 1 " + host

    return os.system(ping_str) == 0
