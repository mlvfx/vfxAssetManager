"""
Host app for maya, check if we are in maya.
"""
import sys


class HostApp(object):
    ID = 'Maya'
    INHOST = False

    def in_host(self):
        self.INHOST = HostApp.in_maya()
        return self.INHOST

    @staticmethod
    def in_maya():
        return 'Maya' in sys.executable