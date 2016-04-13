import os


class BaseAction(object):
    FILETPYE = 'abc'

    def __init__(self):
        pass

    def valid_filetype(self, path, *args):
        print args
        name, ext = os.path.splitext(path)

        return ext.replace('.', '') == self.FILETPYE

    def execute(self):
        raise NotImplementedError