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

        # print plugins

        for p in plugins:
            try:
                host_path = os.path.join(p, 'host.py').replace('\\', '/')
                name, ext = os.path.splitext(host_path)

                host = imp.load_source(name, host_path)

            except IOError, ioe:
                print 'IOError -- ', ioe

            except ImportError, ime:
                print 'ImportError -- ', ime

def main(*args):
    hm = HostManager()

if __name__ == '__main__':
    main()
