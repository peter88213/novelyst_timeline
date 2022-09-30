#!/usr/bin/env python3
"""Install the yw-timeline script and set up the registry files
for extending the yWriter and Timeline context menus. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-timeline
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import stat
from shutil import copytree
from shutil import copyfile
from shutil import rmtree
from pathlib import Path
from string import Template
import gettext
import locale
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('reg', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPNAME = 'yw_timeline_novelyst'
VERSION = ' @release'
APP = f'{APPNAME}.py'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
SAMPLE_PATH = 'sample/'
SUCCESS_MESSAGE = '''
$Appname is installed here:
$Apppath
'''

root = Tk()
processInfo = Label(root, text='')
message = []


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(pywriterPath):
    """Install the script."""

    # Create a general PyWriter installation directory, if necessary.
    os.makedirs(pywriterPath, exist_ok=True)
    installDir = f'{pywriterPath}{APPNAME}'
    cnfDir = f'{installDir}{INI_PATH}'
    os.makedirs(cnfDir, exist_ok=True)

    # Install configuration files, if needed.
    try:
        with os.scandir(SAMPLE_PATH) as files:
            for file in files:
                if not os.path.isfile(f'{cnfDir}{file.name}'):
                    copyfile(f'{SAMPLE_PATH}{file.name}', f'{cnfDir}{file.name}')
                    output(f'Copying "{file.name}"')
                else:
                    output(f'Keeping "{file.name}"')
    except:
        pass


def install_plugin(pywriterPath):
    """Install a novelyst plugin if novelyst is installed."""
    plugin = f'yw_timeline_novelyst.py'
    if os.path.isfile(f'./{plugin}'):
        novelystDir = f'{pywriterPath}novelyst'
        pluginDir = f'{novelystDir}/plugin'
        output(f'Installing novelyst plugin at "{os.path.normpath(pluginDir)}"')
        os.makedirs(pluginDir, exist_ok=True)
        copyfile(plugin, f'{pluginDir}/{plugin}')
        output(f'Copying "{plugin}"')
    else:
        output('Error: novelyst plugin file not found.')

    # Install the localization files.
    copytree('locale', f'{novelystDir}/locale', dirs_exist_ok=True)
    output(f'Copying "locale"')


if __name__ == '__main__':
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("800x600")
    root.title(f'Install {APPNAME}{VERSION}')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    pywriterPath = f'{homePath}/.pywriter/'
    try:
        install(pywriterPath)
    except Exception as ex:
        output(str(ex))
    novelystDir = f'{pywriterPath}novelyst'
    if os.path.isdir(novelystDir):
        try:
            install_plugin(pywriterPath)
            install(pywriterPath)
        except Exception as ex:
            output(str(ex))
    else:
        messagebox.showwarning('The novelyst applilcation seems not to be installed. please install first.')

    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
