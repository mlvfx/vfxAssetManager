import os

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
            print p


def main(*args):
    hm = HostManager()

if __name__ == '__main__':
    main()