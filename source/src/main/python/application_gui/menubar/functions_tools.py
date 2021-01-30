import os
from pathlib import Path

import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

from application_gui.metadata_read.display import readMetadataWindow
from application_gui.metadata_seek.popup import seekMetadataPopup
from application_gui.tools_converter.display import convertStackWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarToolsFunctions(object):

    ##-\-\-\-\-\
    ## TOOLS MENU
    ##-/-/-/-/-/

    # --------------------
    # Read a metadata file
    def callReadMetadataWindow(self):

        # Get the metadata
        metadataFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Open Metadata file...", "","Metadata Files (*.xml)")

        # Open the window if a file has been selected
        if metadataFile:
            openWindow(self.parent, readMetadataWindow, 'read_metadata', file_path=metadataFile)

    # --------------------------------------------------
    # Seek information in the metadata files in a folder
    def callSeekMetadataWindow(self):

        # Get the metadata
        metadataFolder = qtw.QFileDialog.getExistingDirectory(self.parent, "Search in folder...")

        # Open the window if a folder has been selected
        if metadataFolder:

            # List all files
            data_files = [ x for x in Path(metadataFolder).rglob('*.xml') ]

            # Raise an error if no files could be found
            if len(data_files) == 0:
                pass # NOTE: Add error message here

            # Open the file
            else:
                openWindow(self.parent, seekMetadataPopup, 'seek_metadata_popup', files_list=data_files)

    # -------------------------
    # Convert folders to stacks
    def callConvertFolderWindow(self):
        openWindow(self.parent, convertStackWindow, 'convert_stacks')
