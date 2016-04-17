"""
MAYA ACTIONS
"""
from vfxAssetManager.base.action import BaseAction, filename_input
import os
from PySide import QtGui


class AbcImport(BaseAction):
    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import maya.cmds as cmds
            cmds.AbcImport(str(path))


class AbcExport(BaseAction):
    """
    Exports an alembic file, action based on app context
    """
    NAME = 'Alembic Export'
    FILETYPE = 'abc'
    ACTIONTYPE = 2

    def execute(self, path, **kwargs):
        if os.path.isfile(path):
            path = os.path.split(path)[0]

        if not os.path.isdir(path):
            print 'No found directory'
            return

        self.export(path)

    @filename_input('Export Alembic', 'Output Path: ')
    def export(self, path):
        import maya.cmds as cmds
        selection = cmds.ls(sl=True)
        if selection:
        #     text = NameInput('Export Alembic', 'Output To - %s' % path)
            # text, ok = QtGui.QInputDialog.getText(None, 'Export Alembic', 'Output To - %s' % path)
            # if ok and text:
            name = '%s.abc' % path
            output_path = name.replace("\\", "/")
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
            # asset = Asset(None, name, output_path)
            # self.asset_list_widget.addItem(asset)
            # self.selected_asset(asset)


def register_actions(*args):
    return [AbcImport(), AbcExport()]
