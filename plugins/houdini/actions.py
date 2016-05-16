"""
HOUDINI ACTIONS
"""
from vfxAssetManager.base.actions import BaseAction
import os


class AbcImport(BaseAction):
    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        print path
        if self.valid_filetype(path):
            import hou
            name, ext = os.path.splitext((os.path.basename(path)))
            obj = hou.node("/obj")
            abc_node = obj.createNode('alembicarchive', 'abc_%s' % name)
            abc_node.parm('fileName').set(path)
            abc_node.parm('buildHierarchy').pressButton()

            # abc_node.setCurrent()
            abc_node.moveToGoodPosition()
            abc_node.setSelected(True, clear_all_selected=True, show_asset_if_selected=True)


class AbcReference(BaseAction):
    NAME = 'ABC Reference'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            print 'Reference'


class AbcTest(BaseAction):
    NAME = 'ABC Test'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            print 'Test'


class AbcExport(BaseAction):
    NAME = 'Alembic Export'
    FILETYPE = 'abc'
    ACTIONTYPE = 2

    def execute(self, path, **kwargs):
        print 'Test Export'


class VdbExport(BaseAction):
    NAME = 'VDB Export'
    FILETYPE = 'vdb'
    ACTIONTYPE = 2

    def execute(self, path, **kwargs):
        print path
        print 'Test Export'


class VdbImport(BaseAction):
    NAME = 'VDB Import'
    FILETYPE = 'vdb'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


def register_actions(*args):
    return [AbcImport(), AbcReference(), AbcExport(), VdbExport(), VdbImport()]
