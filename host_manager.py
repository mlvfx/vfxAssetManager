import os
import imp
import sys

PROJECT_FOLDER = os.path.dirname(__file__)


def find_plugins(): 
    plugins_folder = os.path.join(PROJECT_FOLDER, 'plugins').replace('\\', '/')

    if os.path.isdir(plugins_folder):
        plugins = os.listdir(plugins_folder)

        if plugins:
            for plugin in plugins:
                yield os.path.join(plugins_folder, plugin).replace('\\', '/')


class HostManager(object):
    def __init__(self):
        plugins = find_plugins()
        self.host_app = None
        self.host_actions = []

        # print plugins

        for p in plugins:
            try:
                host_path = os.path.join(p, 'host.py').replace('\\', '/')
                name, ext = os.path.splitext(host_path)

                host = imp.load_source(name, host_path)
                host_app = host.HostApp()

                if host_app.INHOST:
                    self.host_app = host_app
                    action_path = os.path.join(p, 'actions.py').replace('\\', '/')
                    name, ext = os.path.splitext(action_path)

                    action = imp.load_source(name, action_path)
                    self.host_actions = action.register_actions()

            except IOError, ioe:
                print 'IOError -- ', ioe

            except ImportError, ime:
                print 'ImportError -- ', ime

    def get_hostapp(self):
        return self.host_app

    def get_actions(self):
        return self.host_actions