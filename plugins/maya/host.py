"""
Host app for maya, check if we are in maya.
"""
import sys


class HostApp(object):
    @staticmethod
    def in_maya():
        return 'Maya' in sys.executable