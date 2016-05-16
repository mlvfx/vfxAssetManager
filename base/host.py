import sys
from PySide import QtGui


class BaseHost(object):
    ID = 'python'
    INHOST = False
    FILETYPES = ['abc']

    def __init__(self):
        self.INHOST = self.get_host()

    def get_host(self):
        return 'python' in sys.executable

    def start_QApp(self):
        try:
            app = QtGui.QApplication(sys.argv)
            # app = QtGui.QApplication(["python"])
        except RuntimeError:
            app = QtGui.QApplication.instance()

        sys.exit(app.exec_())
