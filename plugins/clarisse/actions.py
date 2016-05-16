"""
CLARISSE ACTIONS
"""
from vfxAssetManager.base.actions import BaseAction
import os


class AbcImport(BaseAction):
    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


class TextureImport(BaseAction):
    NAME = 'PNG Import'
    FILETYPE = 'png'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            name, ext = os.path.splitext(os.path.basename(path))
            texture_file = ix.create_object(str(name), 'TextureMapFile')
            texture_file.get_attribute('filename').set_string(str(path))
            print 'Created TextureMapFile: {0}'.format(name)


class VdbImport(BaseAction):
    NAME = 'VDB Import'
    FILETYPE = 'vdb'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


def register_actions(*args):
    return [AbcImport(), TextureImport(), VdbImport()]
