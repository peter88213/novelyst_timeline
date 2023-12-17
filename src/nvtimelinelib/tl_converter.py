"""Provide a converter class for novelyst and Timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv-timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from novxlib.novx_globals import *
from novxlib.converter.converter import Converter
from novxlib.novx.novx_file import NovxFile
from novxlib.model.novel import Novel
from nvtimelinelib.tl_file import TlFile


class TlConverter(Converter):
    """A converter class for novelyst and Timeline."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.

        The direction of the conversion is determined by the source file type.
        Only novelyst project files and Timeline files are accepted.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)
        if fileExtension == TlFile.EXTENSION:
            # Source is a timeline
            sourceFile = TlFile(sourcePath, **kwargs)
            targetFile = NovxFile(f'{fileName}{NovxFile.EXTENSION}', **kwargs)
            if os.path.isfile(f'{fileName}{NovxFile.EXTENSION}'):
                # Update existing novelyst project from timeline
                self.import_to_novx(sourceFile, targetFile)
            else:
                # Create new novelyst project from timeline
                self.create_novx(sourceFile, targetFile)
        elif fileExtension == NovxFile.EXTENSION:
            # Update existing timeline from novelyst project
            sourceFile = NovxFile(sourcePath, **kwargs)
            targetFile = TlFile(f'{fileName}{TlFile.EXTENSION}', **kwargs)
            self.export_from_novx(sourceFile, targetFile)
        else:
            # Source file format is not supported
            self.ui.set_info_how(f'!{_("File type is not supported")}: "{norm_path(sourcePath)}".')

