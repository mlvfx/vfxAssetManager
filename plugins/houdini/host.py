"""
Host app for maya, check if we are in maya.
"""
from vfxAssetManager.base.host import BaseHost
import sys


class HostApp(BaseHost):
    ID = 'Houdini'

    def get_host(self):
        return 'houdini' in sys.executable
