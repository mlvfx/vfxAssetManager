from vfxAssetManager.base.action import BaseAction
import os


class AbcImport(BaseAction):
    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        print path
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


class AbcReference(BaseAction):
    NAME = 'ABC Reference'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


class VdbImport(BaseAction):
    NAME = 'VDB Import'
    FILETYPE = 'vdb'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


def register_actions(*args):
    return [AbcImport(), AbcReference(), VdbImport()]
