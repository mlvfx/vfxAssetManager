"""
Host app for maya, check if we are in maya.
"""
from vfxAssetManager.base.host import BaseHost
import sys


class HostApp(BaseHost):
    ID = 'Maya'
    FILETYPES = ['abc', 'png', 'tiff']

    def get_host(self):
        return 'Maya' in sys.executable

    def start_QApp(self):
        pass
