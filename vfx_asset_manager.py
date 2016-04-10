import sys
import os
import inspect
import fnmatch
import pprint

if not 'G:/Scripts/' in sys.path:
    sys.path.append('G:/Scripts/')

from PySide import QtCore
from PySide import QtGui

import vfxAssetManager.ui.contact_sheet as contact_sheet
reload(contact_sheet)

PROJECTS_FOLDER = 'G:/'
PUBLISH_FOLDER = 'published'
DEFAULT_PROJECT = 'EelCreek'


class VFXAssetManager(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(VFXAssetManager, self).__init__(parent)
        self.setWindowTitle("VFX Asset Manager")
        self.resize(700, 500)

        with open('G:/Scripts/vfxAssetManager/ui/style/darkorange.stylesheet', 'r') as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)

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
        self.breadcrumb = QBreadcrumb(parent=self.folder_tree_widget)
        self.assets.addWidget(self.breadcrumb)
        self.assets.addWidget(QtGui.QLabel('Assets:'))
        self.asset_list_widget = self._list_widget(parent=self.assets)     

        self.texture_widget = contact_sheet.QdContactSheet()
        self.assets.addWidget(self.texture_widget)  
        self.export_abc_button = QtGui.QPushButton('Export Alembic')
        self.export_abc_button.clicked.connect(self.abc_export)
        self.assets.addWidget(self.export_abc_button)
        self.path_layout = self._path_layout(parent=self.assets)     

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

    def abc_export(self):
        """
        Exports an alembic file, action based on app context        
        """
        export_path = self.path_line.text()        
        if os.path.isfile(export_path):
            export_path = os.path.split(self.path_line.text())[0]

        if not os.path.isdir(export_path):
            print 'No found directory'
            return
        
        if HostApp.in_maya():
            selection = cmds.ls(sl=True)
            if selection:
                text, ok = QtGui.QInputDialog.getText(self, 'Export Alembic', 'Output To - %s' % export_path)
                if ok and text:
                    name = '%s.abc' % text
                    output_path = os.path.join(export_path, name).replace("\\","/")
                    selection_command = '-root ' + ' -root '.join(selection)    
                    file_output = '-file {0}'.format(output_path)    
                    options_str = '-uvWrite -worldSpace -dataFormat ogawa'
                    frame_str = '-frameRange {0} {1}'.format(cmds.playbackOptions(q=True, min=True),
                                                             cmds.playbackOptions(q=True, max=True))                                            
                       
                    job_command = '{0} {1} {2} {3}'.format(frame_str, 
                                                           options_str, 
                                                           selection_command, 
                                                           file_output)

                    cmds.AbcExport(j=job_command)
                    asset = Asset(None, name, output_path)
                    self.asset_list_widget.addItem(asset)
                    self.selected_asset(asset)

    def selected_asset(self, item):
        """
        Triggers when an asset is selected in the asset tree,
        provides information to the info section

        Args:
            item(Asset): pass in an Asset object
        """
        print item.get_path() 
        self.path_line.setText(item.get_path())

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

    def _populate_projects(self):
        for p in self.get_projects(PROJECTS_FOLDER):
            self.projects_combo.addItem(p)

        index = self.projects_combo.findText(DEFAULT_PROJECT, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.projects_combo.setCurrentIndex(index)

    def _populate_variants(self):
        self.folder_tree_widget.clear()

        self.current_locations['project'] = self.projects_combo.currentText()
        self.current_locations['project_folder'] = self._join_path(PROJECTS_FOLDER, self.current_locations['project'])
        self.current_locations['project_pub_folder'] = self._join_path(self.current_locations['project_folder'], PUBLISH_FOLDER)

        folder_directoy = {}
        root_dir = self.current_locations['project_folder'].rstrip(os.sep)
        start = root_dir.rfind(os.sep) + 1

        parent_item = self.folder_tree_widget

        for root, dirnames, filenames in os.walk(root_dir):
            folders = root[start:].split(os.sep)

            try:
                if not folders[-2] == root_dir:
                    parent_item = folder_directoy.get(folders[-2])
                else:
                    parent_item = self.folder_tree_widget      
            except IndexError:
                parent_item = self.folder_tree_widget            

            if not folders[-1] == root_dir:
                folder_directoy[folders[-1]] = Variant(parent=parent_item, 
                                              name=folders[-1], 
                                              path=root)

    def _populate_assets(self, item):
        self.breadcrumb.set_breadcrumb_label(item)

        self.asset_list_widget.clear()
        self.path_line.setText(item.get_path())

        for asset in self._get_files(item.get_path(), pattern='*.abc'):
            name = os.path.basename(asset)
            if os.path.isfile(asset): 
                self.asset_list_widget.addItem(Asset(None, name, asset))

        images = self._get_files(item.get_path(), pattern='*.png')
        images.sort()
        self.texture_widget.load(images)            

    def _populate_asset_info(self):
        self.current_locations['asset'] = self.asset_list_widget.currentItem().text() or ''
        print self.current_locations['asset']

    def tester(self):
        # self._populate_assets(self.folder_tree_widget.currentItem())
        print self.folder_tree_widget.currentItem().get_name()

    def _tree_widget(self, parent):
        tree_browser_widget = QtGui.QTreeWidget()
        tree_browser_widget.itemClicked.connect(self._populate_assets)
        tree_browser_widget.itemSelectionChanged.connect(self.tester)
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

    def _path_layout(self, parent):
        path_widget = QtGui.QWidget()
        path_layout = QtGui.QHBoxLayout(path_widget)
        self._clean_layouts(path_layout)

        path_layout.addWidget(QtGui.QLabel('Path:'))
        self.path_line = QtGui.QLineEdit('...')
        self.path_line.setReadOnly(True)
        path_layout.addWidget(self.path_line)

        parent.addWidget(path_widget)

        return path_layout

    def _get_files(self, folder, pattern='*.abc'):
        matches = []

        if os.path.isdir(folder):
            for root, dirnames, filenames in os.walk(folder):
                for filename in fnmatch.filter(filenames, pattern):
                    matches.append(os.path.join(root, filename).replace("\\","/"))

            return matches
            # folders = os.listdir(folder)
            # return [f for f in folders if not FolderHelper().is_hidden(os.path.join(folder, f))]
        else:
            return matches

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
        self._path = path.replace("\\","/")

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
        self._path = path.replace("\\","/")

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
    def in_nuke():
        return 'Nuke' in sys.executable

    @staticmethod
    def in_maya():
        return 'Maya' in sys.executable

    @staticmethod
    def in_shell():
        return 'python' in sys.executable
        # try:
        #     return sys.stdout.isatty()
        # except AttributeError:
        #     return False


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


class QBreadcrumb(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QBreadcrumb, self).__init__(parent)        
        self.parent = parent
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(2)
        m = 3
        self.layout.setContentsMargins(m, m, m, m)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.buttons = []
        self.dividers = []

        num_of_buttons = 5
        for value in range(num_of_buttons):
            self._add_button()        

    def set_breadcrumb_label(self, *args):
        
        button_activators = [args[-1]]
        parent = args[-1].parent()
        if parent:
            button_activators.append(parent)
            while parent.parent() is not None:
                parent = parent.parent()
                button_activators.append(parent)

        if button_activators:
            button_activators.reverse()
            for idx, item in enumerate(button_activators):
                self.buttons[idx].setText(item.get_name())
                self.buttons[idx].setVisible(True)
                self.dividers[idx].setVisible(True)
                self.buttons[idx].clicked.connect(lambda: self._select_in_tree(item))

    def _select_in_tree(self, item):
        # print self.parent, item.get_name()
        self.parent.setCurrentItem(item)

    def _add_button(self):
        button = QtGui.QPushButton('..')
        button.setFixedWidth(70)
        button.setVisible(False)
        self.layout.addWidget(button)
        self._add_divider()
        self.buttons.append(button)

    def _add_divider(self):
        divider = QtGui.QLabel('>')
        divider.setFixedWidth(8)
        divider.setVisible(False)
        self.layout.addWidget(divider)
        self.dividers.append(divider)


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

    if HostApp.in_nuke():
        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()

    if HostApp.in_maya():
        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()

    if HostApp.in_shell():
        app = QtGui.QApplication(sys.argv)
        vfx_asset_manager = VFXAssetManager()
        vfx_asset_manager.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()