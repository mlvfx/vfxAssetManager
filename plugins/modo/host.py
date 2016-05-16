"""
Host app for modo, check if we are in modo.
"""
from vfxAssetManager.base.host import BaseHost
import sys
from PySide import QtGui


class HostApp(BaseHost):
    ID = 'Modo'
    FILETYPES = ['abc']

    def get_host(self):
        return 'modo' in sys.executable

    def start_QApp(self):
        pass