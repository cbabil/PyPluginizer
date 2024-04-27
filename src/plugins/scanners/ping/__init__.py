import os
from src.plugins.scanners.ping.plugin import Ping


def get_version():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "./VERSION")) as f:
        return f.read().strip()


__version__ = get_version()


__all__ = ['__version__', 'Ping']
