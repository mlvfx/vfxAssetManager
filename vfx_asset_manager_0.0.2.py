import sys
import os
import glob

from PySide import QtCore
from PySide import QtGui
# execfile('C:/Users/tkdmatt/Downloads/test.py')

PROJECTS_FOLDER = 'G:/'
PUBLISH_FOLDER = 'published'
DEFAULT_PROJECT = 'EelCreek'


class VFXAssetManager(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(VFXAssetManager, self).__init__(parent)
        self.setWindowTitle("VFX Asset Manager")
        self.resize(700, 500)

        # Default values
        self.current_locations = {'project': '', 'project_folder': '', 
                                  'project_pub_folder': '',
                                  'variant': '', 'variant_folder': '',
                                  'asset': '', 'asset_folder': ''}

        # Main layout widgets
        main_widget = QtGui.QWidget()
        self. main_layout = QtGui.QHBoxLayout()
        self._clean_layouts(self.main_layout)
        main_widget.setLayout(self.main_layout)

        # Set the main layout
        self.setCentralWidget(main_widget)

        # Setup the variants vbox
        self.variants = self._variant_layout()        
        self.variants.addWidget(QtGui.QLabel('Projects:'))
        self.projects_combo = QtGui.QComboBox()        
        self.variants.addWidget(self.projects_combo)
        self.variants.addWidget(QtGui.QLabel('Published Folder - Variants:'))
        self.folder_tree_widget = self._tree_widget(parent=self.variants)

        # Setup the assets vbox
        self.assets = self._asset_layout()
        self.assets.addWidget(QtGui.QLabel('Assets:'))
        self.asset_list_widget = self._list_widget(parent=self.assets)        

        # Initial population
        self._populate_projects()
        self._populate_variants()        

        # Signal for project changes
        self.projects_combo.currentIndexChanged.connect(self._populate_variants)

    def abc_import(self, item):
        """
        Imports an alembic file, action based on app context

        Args:
            item(Asset): pass in an Asset object
        """
        item.abc_import()

    def selected_asset(self, item):
        """
        Triggers when an asset is selected in the asset tree,
        provides information to the info section

        Args:
            item(Asset): pass in an Asset object
        """
        print item.get_path()

    def selected_asset_rightclicked(self, QPos):
        """
        Action used when an asset is rightclicked

        Args:
            QPos(QPosition): location where the right click happened
        """
        item = self.asset_list_widget.itemAt(QPos)
        if item is not None:
            menu = QtGui.QMenu("Context Menu", self)
            abc_import_action = QtGui.QAction('ABC Import', 
                                              self, 
                                              triggered=lambda: self.abc_import(item))
            menu.addAction(abc_import_action)
            ret = menu.exec_(self.asset_list_widget.mapToGlobal(QPos))

    def get_projects(self, filepath):        
        projects = os.listdir(filepath)
        return [p for p in projects if not FolderHelper().is_hidden(self._join_path(filepath, p))]

    def get_variants(self):
        return self._get_files(self._join_path(self.current_locations['project_folder'], PUBLISH_FOLDER))

    def get_subvariants(self, variant):  
        path = self._join_path(self.current_locations['project_folder'], 
                                                  PUBLISH_FOLDER,
                                                  variant)

        return self._get_files(path)

    def get_assets(self, path):
        return self._get_files(path)

    def _populate_projects(self):
        for p in self.get_projects(PROJECTS_FOLDER):
            self.projects_combo.addItem(p)

        index = self.projects_combo.findText(DEFAULT_PROJECT, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.projects_combo.setCurrentIndex(index)

    def _populate_variants(self):
        self.current_locations['project'] = self.projects_combo.currentText()
        self.current_locations['project_folder'] = self._join_path(PROJECTS_FOLDER, self.current_locations['project'])
        self.current_locations['project_pub_folder'] = self._join_path(self.current_locations['project_folder'], PUBLISH_FOLDER)

        for v in self.get_variants():
            try:
                item = Variant(self.folder_tree_widget, v, self.current_locations['project_pub_folder'])               

                for sv in self.get_subvariants(v):
                    sub_variant_path = item.get_path()
                    print self._join_path(sub_variant_path, sv)
                    if not os.path.isfile(self._join_path(sub_variant_path, sv)): 
                        child_item = Variant(None, sv, sub_variant_path)
                        if child_item.is_dir():                        
                            item.addChild(child_item)
            except Exception, ex:
                print ex

    def _populate_assets(self, item):
        self.asset_list_widget.clear()

        for asset in self.get_assets(item.get_path()):
            if os.path.isfile(self._join_path(item.get_path(), asset)): 
                self.asset_list_widget.addItem(Asset(None, asset, item.get_path()))

    def _populate_asset_info(self):
        self.current_locations['asset'] = self.asset_list_widget.currentItem().text() or ''
        print self.current_locations['asset']

    def _tree_widget(self, parent):
        tree_browser_widget = QtGui.QTreeWidget()
        tree_browser_widget.itemClicked.connect(self._populate_assets)
        tree_browser_widget.setHeaderHidden(True)
        parent.addWidget(tree_browser_widget)

        return tree_browser_widget

    def _list_widget(self, parent):
        list_widget = QtGui.QListWidget()
        list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(self.selected_asset_rightclicked)
        list_widget.itemClicked.connect(self.selected_asset)
        parent.addWidget(list_widget)

        return list_widget

    def _variant_layout(self):
        variant_widget = QtGui.QWidget()
        variant_widget.setFixedWidth(200)
        variant_vlayout = QtGui.QVBoxLayout(variant_widget)
        self._clean_layouts(variant_vlayout)

        create_variant_button = QtGui.QPushButton('Create Variant')

        self.main_layout.addWidget(variant_widget)

        return variant_vlayout

    def _asset_layout(self):
        asset_widget = QtGui.QWidget()
        asset_layout = QtGui.QVBoxLayout(asset_widget)
        self._clean_layouts(asset_layout)

        self.main_layout.addWidget(asset_widget)

        return asset_layout

    def _get_files(self, folder):
        if os.path.isdir(folder):
            folders = os.listdir(folder)
            return [f for f in folders if not FolderHelper().is_hidden(os.path.join(folder, f))]
        else:
            return []

    def _join_path(self, *args):
        return os.path.join(*args).replace("\\","/")

    def _clean_layouts(self, layout):
        m = 3
        layout.setContentsMargins(m, m, m, m)
        layout.setAlignment(QtCore.Qt.AlignTop)


class Variant(QtGui.QTreeWidgetItem):
    def __init__(self, parent, name, path):
        super(Variant, self).__init__(parent)

        self.setText(0, name)
        self._path = os.path.join(path, name).replace("\\","/")

    def get_name(self):
        return self.text(0)

    def get_path(self):
        return self._path

    def is_file(self):
        return os.path.isfile(self.get_path())

    def is_dir(self):
        return not os.path.isfile(self.get_path())


class Asset(QtGui.QListWidgetItem):
    def __init__(self, parent, name, path):
        super(Asset, self).__init__(parent)

        self.setText(name)
        self._path = os.path.join(path, name).replace("\\","/")

    def get_name(self):
        return self.text()

    def get_path(self):
        return self._path 

    def abc_import(self):
        if HostApp.in_maya():
            import maya.cmds as cmds
            cmds.AbcImport(str(self.get_path()))

        if HostApp.in_clarisse():
            import ix
            ix.import_scene(str(self.get_path()))


class HostApp(object):
    @staticmethod
    def in_clarisse():
        return 'Clarisse' in sys.executable

    @staticmethod
    def in_maya():
        return 'Maya' in sys.executable

    @staticmethod
    def in_shell():
        try:
            return sys.stdout.isatty()
        except AttributeError:
            return False


class FolderHelper(object):
    def is_hidden(self, filepath):
        name = os.path.basename(os.path.abspath(filepath))
        return name.startswith('.') or self.has_hidden_attribute(filepath)

    def has_hidden_attribute(self, filepath):
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
            assert attrs != -1
            result = bool(attrs & 2)
        except (AttributeError, AssertionError):
            result = False
        return result


def main(*args):
    global vfx_asset_manager

    try:
        vfx_asset_manager.close()
    except:
        pass

    if HostApp.in_clarisse():
        import pyqt_clarisse

        try:
            app = QtGui.QApplication(["Clarisse"])
        except:
            app = QtGui.QApplication.instance()

        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()

        pyqt_clarisse.exec_(app)

    if HostApp.in_maya():
        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()

    if HostApp.in_shell():
        app = QtGui.QApplication(sys.argv)
        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()
        sys.exit(app.exec_())

    print 'open VFX Asset Manager'

if __name__ == '__main__':
    main()