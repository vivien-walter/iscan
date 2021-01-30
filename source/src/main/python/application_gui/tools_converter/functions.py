import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.folder_management import getImageFolderList

from application_gui.common_gui_functions import openWindow
from application_gui.messageboxes.display import errorMessage
from application_gui.progressbar.convert_folder import ConvertFolderProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class convertStackFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACT WITH THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------
    # Browse for a directory
    def browseDirectory(self):

        # Open the browser
        directoryPath = qtw.QFileDialog.getExistingDirectory(self.parent, "Open Directory...")

        # Process only if an image has been selected
        if directoryPath != "":
            folder_list, folder_infos = getImageFolderList(directoryPath)

            # Check that the folder list is not empty
            if len(folder_list) == 0:
                errorMessage('No folder found','No image folder was found in the selected directory.')

            else:
                self.directory = directoryPath
                self.folders = folder_list
                self.infos = folder_infos

                # Refresh the display
                self.browseEntry.lineEdit.setText(directoryPath)
                self.populateTable()

    # ---------------------------------------
    # Populate the table with the information
    def populateTable(self):

        # Delete the previous values
        rowCount = self.foldersTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.foldersTable.removeRow(0)

        # Add all the folders
        self.all_checkboxes = []
        for row_id, crt_folder in enumerate(self.folders):

            # Fill the rows
            self.foldersTable.insertRow(row_id)

            # Make the checkbox
            crt_checkbox = qtw.QCheckBox("Convert?")
            crt_checkbox.setChecked(True)
            self.all_checkboxes.append(crt_checkbox)

            # Get current infos
            crt_infos = self.infos[row_id]

            # Set the bitness
            if crt_infos['max_pv'] > 256:
                _bitness = '16 bits'
            else:
                _bitness = '8 bits'

            # Add the content
            self.foldersTable.setCellWidget(row_id, 0, crt_checkbox)
            self.foldersTable.setItem(row_id, 1, qtw.QTableWidgetItem( crt_folder ))
            self.foldersTable.setItem(row_id, 2, qtw.QTableWidgetItem( str(crt_infos['number']) ))
            self.foldersTable.setItem(row_id, 3, qtw.QTableWidgetItem( _bitness ))

        # Resize the columns
        header = self.foldersTable.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ----------------------------------------
    # Convert the selected folders into stacks
    def convertFolders(self):

        # Only process if the folder is not empty
        if self.directory is not None:

            # Get all the folders to save
            folders_to_save = []
            for i, crt_checkbox in enumerate(self.all_checkboxes):

                if crt_checkbox.isChecked():
                    folders_to_save.append( os.path.join( self.directory,self.folders[i] ) )

            # Process the folders
            if len( folders_to_save ) == 0:
                errorMessage("Empty selection","The current selection of folders to be converted is empty. Select at least one folder to proceed.")

            else:
                # Get the status of the checkbox
                delete_folders = self.deleteFoldersCheckbox.isChecked()

                # Process all the folders
                openWindow(self.parent, ConvertFolderProgressBarWindow, 'progress_bar', folder_list=folders_to_save, delete_folders=delete_folders, scheduler=self)

    # ------------------------------
    # Reset the display after saving
    def resetDisplay(self):

        # Empty the window
        self.directory = None
        self.folders = None
        self.infos = None

        # Delete the previous values in the table
        rowCount = self.foldersTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.foldersTable.removeRow(0)

        # Add all the folders
        self.all_checkboxes = []
        self.browseEntry.lineEdit.setText("")
