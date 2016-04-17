import os
from vfxAssetManager.base.constants import ActionType
from PySide import QtGui


class BaseAction(object):
    NAME = 'BaseAction'
    FILETPYE = 'abc'
    ACTIONTYPE = ActionType.Menu

    def __init__(self):
        pass

    def valid_filetype(self, path, *args):
        print args
        name, ext = os.path.splitext(path)

        return ext.replace('.', '') == self.FILETPYE

    def execute(self):
        raise NotImplementedError


def filename_input(title='Name Input', outputtext='Text: '):
    def name_decorate(func):
        def func_wrapper(self, path):
            text, ok = QtGui.QInputDialog.getText(None, title, outputtext+path)
            if ok and text:
                output_path = '{0}/{1}'.format(path, text)
                return func(self, output_path)
        return func_wrapper
    return name_decorate
