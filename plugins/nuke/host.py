"""
Host app for maya, check if we are in maya.
"""
from vfxAssetManager.base.host import BaseHost
import sys


class HostApp(BaseHost):
    ID = 'Nuke'

    def get_host(self):
        return 'Nuke' in sys.executable       
