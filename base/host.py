import sys


class BaseHost(object):
    ID = 'python'
    INHOST = False

    def __init__(self):
    	self.INHOST = self.get_host()

    def get_host(self):
        return 'python' in sys.executable

    def start_QApp(self):
        pass