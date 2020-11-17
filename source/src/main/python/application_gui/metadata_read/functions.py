import os

import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, emptyLayout

from metadata.read_data import readMetadataFile

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class readMetadataFunctions(object):

    ##-\-\-\-\-\-\-\
    ## LOAD METADATA
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Get the metadata from the file
    def loadFromFile(self, file_path):

        # Extract content from file
        self.data_type, _data_content = readMetadataFile(file_path)

        # Get information for the table columns
        _table_dict = _data_content['Frames']
        _example_key = list( _table_dict.keys() )[0]
        self.column_names = list( _table_dict[_example_key].keys() )
        self.n_columns = len(self.column_names)
        self.n_rows = len( list( _table_dict.keys()) )

        # Get the informations from the jobs
        self.data_general = _data_content['General']
        self.data_content = _data_content['Frames']

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Get the current frame ID
    def _get_frame_id(self, current_id):

        # Search for the next frame ID
        seek_id = True
        while seek_id:

            # Get the frame to open
            if self.data_type == 'experiment':
                frame_prefix = 'Frame '
            elif self.data_type == 'fast_record':
                frame_prefix = 'Frame'

            current_frame_id = frame_prefix + str(current_id)

            # Check if the frame exist
            if current_frame_id not in self.data_content.keys():
                current_id += 1
            else:
                seek_id = False

        # Move to the next id
        new_id = current_id + 1

        return current_frame_id, new_id

    # ----------------------------------
    # Populate the general infos section
    def populateGeneral(self):

        # Metadata type
        if self.data_type == 'experiment':
            _metadata_type = 'EXPERIMENT'
            _, _file_name = os.path.split(self.file_path)
        elif self.data_type == 'fast_record':
            _metadata_type = 'FAST RECORD'
            _file_name, _ = os.path.split(self.file_path)
            _, _file_name = os.path.split(_file_name)
        self.generalInfosLayout.addWidget( CLabel(_metadata_type), alignment=qtc.Qt.AlignCenter)
        self.generalInfosLayout.addWidget( qtw.QLabel(_file_name), alignment=qtc.Qt.AlignCenter)

        # Populate all the informations
        self.generalGridWidget = qtw.QWidget()
        self.generalGridLayout = qtw.QGridLayout(self.generalGridWidget)

        for i, name in enumerate(self.data_general.keys()):

            # Name of the section
            self.generalGridLayout.addWidget( CLabel(name), i, 0)

            # Value of the section
            crt_value = qtw.QLabel(self.data_general[name])
            self.generalGridLayout.addWidget( crt_value, i, 1)

        self.generalGridWidget.setLayout(self.generalGridLayout)
        self.generalInfosLayout.addWidget( self.generalGridWidget, alignment=qtc.Qt.AlignLeft)

    # ------------------
    # Populate the table
    def populateTable(self):

        # Delete the previous values
        rowCount = self.contentTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.contentTable.removeRow(0)

        # Fill the table
        frame_id = 0
        if self.n_rows > 0:
            for row_id in range(self.n_rows):

                # Fill the rows
                self.contentTable.insertRow(row_id)

                # Get the current row
                current_frame_id, frame_id = self._get_frame_id(frame_id)
                current_data = self.data_content[current_frame_id]

                # Populate the columns
                for column_id in range(self.n_columns):
                    _column_key = self.column_names[column_id]
                    self.contentTable.setItem(row_id, column_id, qtw.QTableWidgetItem( str(current_data[_column_key]) ))

        # Resize the columns
        header = self.contentTable.horizontalHeader()
        for i in range(self.n_columns):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

    # ----------------------------------------
    # Re-build the window based on new content
    def reconstructWindow(self):

        # Destroy the widget for the table
        emptyLayout(self.generalInfosLayout)

        # Populate the content of the section
        self.populateGeneral()

        # Destroy the widget for the table
        emptyLayout(self.contentTableLayout)

        # Generate the table of servers
        self.contentTable = qtw.QTableWidget(0, self.n_columns)
        self.contentTable.setHorizontalHeaderLabels( self.column_names )

        self.contentTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.contentTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        #self.contentTable.setShowGrid(False)
        self.contentTable.setMinimumHeight(125)
        self.contentTableLayout.addWidget(self.contentTable)

        # Populate the content of the table
        self.populateTable()

        # Set the size
        if self.data_type == 'experiment':
            self.setMinimumSize(700,600)
        elif self.data_type == 'fast_record':
            self.setMinimumSize(500,600)
            self.resize(500,600)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------------
    # Get a new file to open in the window
    def getNewFile(self):

        # Get the metadata
        metadataFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Open Metadata file...", "","Metadata Files (*.xml)")

        # Reload the window if a file has been selected
        if metadataFile:

            # Get the new content
            self.loadFromFile(metadataFile)
            self.file_path = metadataFile

            # Reload the table
            self.reconstructWindow()
