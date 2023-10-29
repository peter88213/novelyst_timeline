"""Timeline sync plugin for novelyst.

Version @release
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_timeline
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
import os
import sys
from pathlib import Path
import tkinter as tk
import locale
import gettext
import webbrowser
from tkinter import messagebox
from datetime import datetime
from novxlib.novx_globals import *
from novxlib.config.configuration import Configuration
from novxlib.file.doc_open import open_document
from novxlib.converter.converter import Converter
from nvtimelinelib.tl_file import TlFile

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getlocale()[0][:2]
try:
    t = gettext.translation('novelyst_timeline', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = 'Timeline'
PLUGIN = f'{APPLICATION} plugin v@release'
INI_FILENAME = 'nv-timeline.ini'
INI_FILEPATH = '.kalliope/nv-timeline/config'


class Plugin():
    """Plugin class for synchronization with Timeline.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        
    """
    VERSION = '@release'
    NOVELYST_API = '5.0'
    DESCRIPTION = 'Synchronize with Timeline'
    URL = 'https://peter88213.github.io/novelyst_timeline'
    _HELP_URL = 'https://peter88213.github.io/novelyst_timeline/usage'

    SETTINGS = dict(
        scene_label='Scene',
        default_date_time='2021-07-26 00:00:00',
        scene_color='170,240,160',
    )
    OPTIONS = dict(
        ignore_unspecific=False,
        dhm_to_datetime=False,
        datetime_to_dhm=False,
    )

    def install(self, ui):
        """Add a submenu to the main menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        self._converter = Converter()
        self._converter.ui = ui

        # Create a submenu
        self._pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._pluginMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Create or update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Edit the timeline'), command=self._launch_application)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _launch_application(self):
        """Launch Timeline with the current project."""
        if self._ui.prjFile:
            timelinePath = f'{os.path.splitext(self._ui.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                if self._ui.lock():
                    open_document(timelinePath)
            else:
                self._ui.set_info_how(_('!No {} file available for this project.').format(APPLICATION))

    def _export_from_novx(self):
        """Update timeline from novelyst.
        """
        if self._ui.prjFile:
            timelinePath = f'{os.path.splitext(self._ui.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                action = _('update')
            else:
                action = _('create')
            if self._ui.ask_yes_no(_('Save the project and {} the timeline?').format(action)):
                self._ui.save_project()
                kwargs = self._get_configuration(self._ui.prjFile.filePath)
                targetFile = TlFile(timelinePath, **kwargs)
                self._converter.export_from_novx(self._ui.prjFile, targetFile)

    def _info(self):
        """Show information about the Timeline file."""
        if self._ui.prjFile:
            timelinePath = f'{os.path.splitext(self._ui.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                try:
                    timestamp = os.path.getmtime(timelinePath)
                    if timestamp > self._ui.prjFile.timestamp:
                        cmp = _('newer')
                    else:
                        cmp = _('older')
                    fileDate = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat(sep=' ')
                    message = _('{0} file is {1} than the novelyst project.\n (last saved on {2})').format(APPLICATION, cmp, fileDate)
                except:
                    message = _('Cannot determine file date.')
            else:
                message = _('No {} file available for this project.').format(APPLICATION)
            messagebox.showinfo(PLUGIN, message)

    def _import_to_novx(self):
        """Update novelyst from timeline.
        """
        if self._ui.prjFile:
            timelinePath = f'{os.path.splitext(self._ui.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if not os.path.isfile(timelinePath):
                self._ui.set_info_how(_('!No {} file available for this project.').format(APPLICATION))
                return

            if self._ui.ask_yes_no(_('Save the project and update it?')):
                self._ui.save_project()
                kwargs = self._get_configuration(timelinePath)
                sourceFile = TlFile(timelinePath, **kwargs)
                self._converter.import_to_novx(sourceFile, self._ui.prjFile)
                message = self._ui.infoHowText

                # Reopen the project.
                self._ui.reloading = True
                # avoid popup message (novelyst v0.52+)
                self._ui.open_project(self._ui.prjFile.filePath)
                self._ui.set_info_how(message)

    def _get_configuration(self, sourcePath):
        #--- Try to get persistent configuration data
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
        kwargs = {}
        kwargs.update(configuration.settings)
        kwargs.update(configuration.options)
        return kwargs


class Converter(Converter):
    """A file converter class that overwrites without asking. 

    Public methods:
        convert(sourceFile, targetFile) -- Convert sourceFile into targetFile.
    """

    def _confirm_overwrite(self, fileName):
        """Return boolean permission to overwrite the target file.
        
        Positional argument:
            fileName -- path to the target file.
        
        Overrides the superclass method.
        """
        return True

