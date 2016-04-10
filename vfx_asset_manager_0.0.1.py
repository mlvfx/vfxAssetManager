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

        self.current_project = {'project': '', 'project_folder': ''}
        self.current_variant = {'variant': '', 'variant_folder': ''}
        self.current_subvariant = {'subvariant': '', 'subvariant_folder': ''}
        self.current_asset = {'asset': '', 'asset_folder': ''}

        main_widget = QtGui.QWidget()
        self. main_layout = QtGui.QHBoxLayout()
        self._clean_layouts(self.main_layout)
        main_widget.setLayout(self.main_layout)

        self.setCentralWidget(main_widget)

        self.variants = self._variant_layout()
        self.variants.addWidget(QtGui.QLabel('Projects:'))
        self.projects_combo = QtGui.QComboBox()        
        self.variants.addWidget(self.projects_combo)
        self.variants.addWidget(QtGui.QLabel('Published Folder - Variants:'))
        self.tree_browser_widget = QtGui.QTreeWidget()
        self.tree_browser_widget.setHeaderHidden(True)
        self.variants.addWidget(self.tree_browser_widget)        
        self.variant_list_widget = QtGui.QListWidget()
        self.variants.addWidget(self.variant_list_widget)

        self.subvariants = self._subvariant_layout()
        self.subvariants.addWidget(QtGui.QLabel('SubVariants:'))
        self.subvariant_list_widget = QtGui.QListWidget()
        self.subvariants.addWidget(self.subvariant_list_widget)

        self.assets = self._asset_layout()
        self.assets.addWidget(QtGui.QLabel('Assets:'))
        self.assets_list_widget = QtGui.QListWidget()
        self.assets.addWidget(self.assets_list_widget)

        self._populate_projects()
        self._populate_variants()        

        self.projects_combo.currentIndexChanged.connect(self._populate_variants)
        self.variant_list_widget.currentTextChanged.connect(self._populate_subvariants)
        self.subvariant_list_widget.currentTextChanged.connect(self._populate_assets)

        # scene = QtGui.QGraphicsScene()
        # scene.addText("Hello, world!")
        # view = QtGui.QGraphicsView(scene)

        # widget = QdContactSheet()
        # images = ['G:/Maya/e3r/sourceimages/blu_03/Blu_03_Body_diff_1k.png', 'G:/Maya/e3r/sourceimages/blu_03/Blu_03_Pants_diff_1k.png', 'G:/Maya/e3r/sourceimages/blu_03/Blu_03_Pants_diff_1k.png', 'G:/Maya/e3r/sourceimages/blu_03/Blu_03_Pants_diff_1k.png', 'G:/Maya/e3r/sourceimages/blu_03/Blu_03_Pants_diff_1k.png' ]# list of images you want to view as thumbnails
        # images.sort()
        # widget.load(images)

        # button = QtGui.QPushButton('Hi')

        # main_layout.addWidget(view)
        # main_layout.addWidget(button)

    def test_tree_browser(self):
        self.dirmodel = QtGui.QFileSystemModel()
        self.dirmodel.setRootPath(PROJECTS_FOLDER)
        # Don't show files, just folders
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)

        self.folder_view = QtGui.QTreeView(parent=self);
        self.folder_view.setModel(self.dirmodel)
        self.folder_view.clicked[QtCore.QModelIndex].connect(self.clicked) 
        # Don't show columns for size, file type, and last modified
        self.folder_view.setHeaderHidden(True)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.selectionModel = self.folder_view.selectionModel()

        self.variants.addWidget(self.folder_view)

    def clicked(self, index):
        #get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dirmodel.filePath(index)
        print dir_path
        ###############################################
        #Here's my problem: How do I set the dir_path
        #for the file_view widget / the filemodel?
        ###############################################
        # self.filemodel.setRootPath(dir_path)

    def get_projects(self, filepath):        
        projects = os.listdir(filepath)
        return [p for p in projects if not FolderHelper().is_hidden(os.path.join(filepath, p))]

    def get_variants(self):
        print self.current_project['project_folder']
        print os.path.join(self.current_project['project_folder'], PUBLISH_FOLDER).replace("\\","/")
        return self._get_files(os.path.join(self.current_project['project_folder'], PUBLISH_FOLDER).replace("\\","/"))

    def get_subvariants2(self, variant):  
        path = os.path.join(self.current_project['project_folder'], 
                                                  PUBLISH_FOLDER,
                                                  variant).replace("\\","/")

        return self._get_files(path)

    def get_subvariants(self):  
        self.current_variant['variant_folder'] = os.path.join(self.current_project['project_folder'], 
                                                              PUBLISH_FOLDER,
                                                              self.current_variant['variant']).replace("\\","/")

        return self._get_files(self.current_variant['variant_folder'])

    def get_assets(self):   
        self.current_subvariant['subvariant_folder'] = os.path.join(self.current_project['project_folder'], 
                                                              PUBLISH_FOLDER,
                                                              self.current_variant['variant_folder'],
                                                              self.current_subvariant['subvariant']).replace("\\","/")

        return self._get_files(self.current_subvariant['subvariant_folder'])

    def _populate_projects(self):
        for p in self.get_projects(PROJECTS_FOLDER):
            self.projects_combo.addItem(p)

        index = self.projects_combo.findText(DEFAULT_PROJECT, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.projects_combo.setCurrentIndex(index)

    def _populate_variants(self):
        self.current_project['project'] = self.projects_combo.currentText()
        self.current_project['project_folder'] = os.path.join(PROJECTS_FOLDER, self.current_project['project']).replace("\\","/")

        self.variant_list_widget.clear()

        for v in self.get_variants():
            item = QtGui.QTreeWidgetItem([v, None])
            self.tree_browser_widget.insertTopLevelItem(0, item)

            for sv in self.get_subvariants2(v):
                if os.path.isdir(sv):
                    child_item = QtGui.QTreeWidgetItem([sv, None])
                    item.addChild(child_item)

    def _populate_subvariants(self):
        self.current_variant['variant'] = self.variant_list_widget.currentItem().text()
        self.subvariant_list_widget.clear()

        for v in self.get_subvariants():
            self.subvariant_list_widget.addItem(v)

    def _populate_assets(self):
        self.current_subvariant['subvariant'] = self.subvariant_list_widget.currentItem().text() or ''

        self.assets_list_widget.clear()

        for v in self.get_assets():
            self.assets_list_widget.addItem(v)

    def _populate_asset_info(self):
        self.current_asset['asset'] = self.assets_list_widget.currentItem().text() or ''
        print self.current_asset

    def _variant_layout(self):
        variant_widget = QtGui.QWidget()
        variant_vlayout = QtGui.QVBoxLayout(variant_widget)
        self._clean_layouts(variant_vlayout)

        create_variant_button = QtGui.QPushButton('Create Variant')
        # create_variant_button.clicked.connect(self.create_variant)

        self.main_layout.addWidget(variant_widget)

        return variant_vlayout

    def _subvariant_layout(self):
        subvariant_widget = QtGui.QWidget()
        subvariant_layout = QtGui.QVBoxLayout(subvariant_widget)
        self._clean_layouts(subvariant_layout)

        self.main_layout.addWidget(subvariant_widget)

        return subvariant_layout

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

    def _clean_layouts(self, layout):
        m = 3
        layout.setContentsMargins(m, m, m, m)
        layout.setAlignment(QtCore.Qt.AlignTop)

    # def create_folder(self, folder_type):
    #     if folder_type == 'variant':
    #         newpath = 


    #     if not os.path.exists(newpath):
    #         os.makedirs(newpath)


class HostApp(object):
    @staticmethod
    def in_clarrise():
        if 'Clarisse' in sys.executable:
            return True
        else:
            return False

    @staticmethod
    def in_maya():
        if 'Maya' in sys.executable:
            return True
        else:
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

    if HostApp.in_clarrise():
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

if __name__ == '__main__':
    main()