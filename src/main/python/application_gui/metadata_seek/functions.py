import numpy as np
import os
import pandas as pd

import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import emptyLayout

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class seekMetadataFunctions(object):

    ##-\-\-\-\-\-\-\
    ## LOAD METADATA
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Get the metadata from the file
    def loadFromFolder(self, file_contents):

        # Get information for the table columns
        _example_key = list( file_contents.keys() )[0]
        _example_dict = file_contents[_example_key]

        # Get the list of info for the General type
        self.info_general_names = list( _example_dict['General'].keys() )

        # Add the rest
        _example_frame_key = list( _example_dict['Frames'].keys() )[0]
        _example_frame_dict = _example_dict['Frames'][_example_frame_key]

        # Add the new list
        self.info_frames_names = list( _example_frame_dict.keys() )
        self.info_names = self.info_general_names + self.info_frames_names

        # Make the list for the general
        all_info_general = []
        for file_path in file_contents.keys():

            # Process all the infos
            crt_dir, crt_file = os.path.split(file_path)
            crt_info_general = [crt_dir, crt_file]
            for info_name in self.info_general_names:
                crt_info_general.append( file_contents[file_path]['General'][info_name] )

            all_info_general.append( crt_info_general )

        # Convert into pandas Data frame
        all_info_general = np.array(all_info_general)
        self.info_general = pd.DataFrame(all_info_general, columns=['Folder','File']+self.info_general_names)

        # Make the list for the frames
        all_info_frames = []
        for file_path in file_contents.keys():

            # Process all the frames
            crt_dir, crt_file = os.path.split(file_path)
            for frame_name in file_contents[file_path]['Frames'].keys():

                # Process all the infos
                crt_info_frames = [ crt_dir, crt_file, frame_name ]
                for info_name in self.info_frames_names:
                    crt_info_frames.append( file_contents[file_path]['Frames'][frame_name][info_name] )

                all_info_frames.append( crt_info_frames )

        # Convert into pandas Data frame
        all_info_frames = np.array(all_info_frames)
        self.info_frames = pd.DataFrame(all_info_frames, columns=['Folder','File','Frame']+self.info_frames_names)

    # ------------------------------------------------------
    # Get the current selection from the combo box selection
    def getCurrentSelection(self, data_name):

        # Check if general
        if data_name in self.info_general_names:
            self.column_header = ['File',data_name,'Folder']
            self.current_dataset = self.info_general[ self.column_header ]

        else:
            self.column_header = ['File','Frame',data_name,'Folder']
            self.current_dataset = self.info_frames[ self.column_header ]

        self.n_columns = len(self.column_header)
        self.n_rows = len(self.current_dataset.index)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # -----------------------------------
    # Populate the table with the content
    def populateTable(self):

        # Delete the previous values
        rowCount = self.contentTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.contentTable.removeRow(0)

        # Fill the table
        if self.n_rows > 0:
            for row_id in range(self.n_rows):

                # Fill the rows
                self.contentTable.insertRow(row_id)

                # Populate the columns
                for column_id in range(self.n_columns):
                    _column_key = self.column_header[column_id]
                    _current_data = self.current_dataset[_column_key].loc[row_id]

                    self.contentTable.setItem(row_id, column_id, qtw.QTableWidgetItem( str(_current_data) ))

        # Resize the columns
        header = self.contentTable.horizontalHeader()
        for i in range(self.n_columns):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

    # ------------------
    # Generate the table
    def generateTable(self):

        # Empty the layout
        emptyLayout(self.contentTableLayout)

        # Get the information to display
        current_name = self.dataSelectionComboBox.currentText()
        self.getCurrentSelection(current_name)

        # Generate the table of servers
        self.contentTable = qtw.QTableWidget(0, self.n_columns)
        self.contentTable.setHorizontalHeaderLabels( self.column_header )

        self.contentTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.contentTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        #self.contentTable.setShowGrid(False)
        self.contentTable.setMinimumHeight(125)
        self.contentTableLayout.addWidget(self.contentTable)

        # Populate the content of the table
        self.populateTable()

    ##-\-\-\-\-\-\
    ## USER ACTION
    ##-/-/-/-/-/-/

    # -----------------------------------
    # Save the selected content in a file
    def saveContent(self):

        # Get the file name to save
        dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Selection as...","selection","Comma-Separated Values (*.csv);;Microsoft Excel (*.xlsx)")

        # Proceed to save the file
        if dataFile:

            # Save the file in the appropriate format
            _, file_extension = os.path.splitext(dataFile)

            if file_extension == '.csv':
                self.current_dataset.to_csv(dataFile)

            elif file_extension == '.xlsx':
                with pd.ExcelWriter(dataFile) as writer:
                    self.current_dataset.to_excel(writer)
