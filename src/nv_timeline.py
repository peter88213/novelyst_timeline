"""Timeline sync plugin for noveltree.

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from datetime import datetime
import gettext
import locale
import os
from pathlib import Path
import sys
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.novx_globals import norm_path
from novxlib.config.configuration import Configuration
from novxlib.file.doc_open import open_document
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import Error
from novxlib.novx_globals import _
from nvtimelinelib.tl_file import TlFile
import tkinter as tk

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getlocale()[0][:2]
try:
    t = gettext.translation('nv_timeline', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:
    pass

APPLICATION = 'Timeline'
PLUGIN = f'{APPLICATION} plugin v@release'
INI_FILENAME = 'nv_timeline.ini'
INI_FILEPATH = '.noveltree/config'


class Plugin():
    """Plugin class for synchronization with Timeline."""
    VERSION = '@release'
    NOVELYST_API = '0.7'
    DESCRIPTION = 'Synchronize with Timeline'
    URL = 'https://peter88213.github.io/nv_timeline'
    _HELP_URL = 'https://peter88213.github.io/nv_timeline/usage'

    SETTINGS = dict(
        section_label='Section',
        section_color='170,240,160',
        new_event_spacing='1'
    )
    OPTIONS = {}

    def install(self, model, view, controller, prefs):
        """Add a submenu to the main menu.
        
        Positional arguments:
            controller -- reference to the main controller instance of the application.
            view -- reference to the main view instance of the application.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Create a submenu
        self._pluginMenu = tk.Menu(self._ui.mainMenu, tearoff=0)
        position = self._ui.mainMenu.index('end')
        self._ui.mainMenu.insert_cascade(position, label=APPLICATION, menu=self._pluginMenu)
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Create or update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Edit the timeline'), command=self._launch_application)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from Timeline...'), command=self._create_novx)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='normal')

    def _create_novx(self):
        """Create a noveltree project from a timeline."""
        timelinePath = filedialog.askopenfilename(
            filetypes=[(TlFile.DESCRIPTION, TlFile.EXTENSION)],
            defaultextension=TlFile.EXTENSION,
            )
        if not timelinePath:
            return

        self._ctrl.c_close_project()
        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{NovxFile.EXTENSION}'
        kwargs = self._get_configuration(timelinePath)
        source = TlFile(timelinePath, **kwargs)
        target = NovxFile(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        message = ''
        try:
            source.novel = Novel(tree=NvTree())
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.c_open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(message)

    def _export_from_novx(self):
        """Update or create a timeline from the noveltree project."""
        if not self._mdl.prjFile:
            return

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        if not self._mdl.prjFile.filePath:
            if not self._ctrl.c_save_project():
                return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            action = _('update')
        else:
            action = _('create')
        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Save the project and {} the timeline?').format(action)):
                return

            self._ctrl.c_save_project()
        elif action == _('update'):
            if not self._ui.ask_yes_no(_('Update the timeline?')):
                return

        kwargs = self._get_configuration(self._mdl.prjFile.filePath)
        target = TlFile(timelinePath, **kwargs)
        source = self._mdl.prjFile
        message = ''
        try:
            source.novel = Novel(tree=NvTree())
            target.novel = Novel(tree=NvTree())
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
        finally:
            self._ui.set_status(message)

    def _get_configuration(self, sourcePath):
        """Return a dictionary with persistent configuration data."""
        sourceDir = os.path.dirname(sourcePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/{INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/{INI_FILENAME}', f'{sourceDir}/{INI_FILENAME}']
        configuration = Configuration(self.SETTINGS, self.OPTIONS)
        for iniFile in iniFiles:
            configuration.read(iniFile)
        configData = {}
        configData.update(configuration.settings)
        configData.update(configuration.options)
        return configData

    def _import_to_novx(self):
        """Update the noveltree project from a timeline."""
        if not self._mdl.prjFile:
            return

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))
            return

        if self._mdl.isModified and not self._ui.ask_yes_no(_('Save the project and update it?')):
            return

        self._ctrl.c_save_project()
        kwargs = self._get_configuration(timelinePath)
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.prjFile
        message = ''
        try:
            target.novel = Novel(tree=NvTree())
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.c_open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        finally:
            self._ui.set_status(f'{message}')

    def _info(self):
        """Show information about the Timeline file."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            try:
                timestamp = os.path.getmtime(timelinePath)
                if timestamp > self._mdl.prjFile.timestamp:
                    cmp = _('newer')
                else:
                    cmp = _('older')
                fileDate = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat(sep=' ')
                message = _('{0} file is {1} than the noveltree project.\n (last saved on {2})').format(APPLICATION, cmp, fileDate)
            except:
                message = _('Cannot determine file date.')
        else:
            message = _('No {} file available for this project.').format(APPLICATION)
        messagebox.showinfo(PLUGIN, message)

    def _launch_application(self):
        """Launch Timeline with the current project."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            if self._ctrl.lock():
                open_document(timelinePath)
        else:
            self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))

