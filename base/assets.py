from PySide import QtGui
import os
import uuid


class Location(QtGui.QTreeWidgetItem):
    ID = uuid.uuid4()

    def __init__(self, parent, name, path):
        super(Location, self).__init__(parent)

        self.setText(0, name)
        self._path = path.replace("\\", "/")

    def get_name(self):
        return self.text(0)

    def get_path(self):
        return self._path

    def is_file(self):
        return os.path.isfile(self.get_path())

    def is_dir(self):
        return not os.path.isfile(self.get_path())


class Asset(QtGui.QListWidgetItem):
    FILETYPE = None
    ACTIONS = []

    def __init__(self, parent, name, path):
        super(Asset, self).__init__(parent)

        self.setText(name)
        self._path = path.replace("\\", "/")

        name, ext = os.path.splitext(self._path)
        self.FILETYPE = ext.replace('.', '')

    def get_name(self):
        return self.text()

    def get_path(self):
        return self._path

    def get_actions(self):
        return self.ACTIONS

    def add_actions(self, actions):
        self.ACTIONS = actions
