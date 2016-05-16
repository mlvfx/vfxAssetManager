"""
Host app for maya, check if we are in maya.
"""
from vfxAssetManager.base.host import BaseHost
import sys
from PySide import QtGui


class HostApp(BaseHost):
    ID = 'Clarisse'
    FILETYPES = ['abc', 'png', 'tiff', 'vdb']

    def get_host(self):
        return 'Clarisse' in sys.executable

    def start_QApp(self):
        import pyqt_clarisse

        try:
            app = QtGui.QApplication(["Clarisse"])
        except:
            app = QtGui.QApplication.instance()

        pyqt_clarisse.exec_(app)
