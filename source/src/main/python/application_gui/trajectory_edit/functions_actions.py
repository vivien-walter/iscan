from functools import partial
import numpy as np
import pandas as pd
from PIL import Image, ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.messageboxes.display import warningProceedMessage

from image_processing.modifications import cropMiniature

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class PathEditorActionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INITIALISE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------
    # Load the selected path
    def getPath(self, path_id=0):

        # Change the saved status
        self.is_saved = True

        # Get the path id
        self.current_path = path_id

        # Get the positions
        crt_positions = self.image_class.trajectory.positions
        self.current_track = crt_positions[crt_positions['particle'] == self.current_path]

        # Assign the index
        self.current_track.set_index(self.current_track['frame'].to_numpy(), inplace=True)

    ##-\-\-\-\-\-\-\-\-\
    ## POPULATE THE TABLE
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Process the signals taken from the trajectory
    def populateTable(self):

        # Delete the previous values
        rowCount = self.frameTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.frameTable.removeRow(0)

        colCount = self.frameTable.columnCount()
        if colCount > 0:
            for i in range(colCount):
                self.frameTable.removeColumn(0)

        # Populate the table
        self.frameTable.insertRow(0)
        self.frame_buttons = []

        # Loop over the number of frames
        for i in range(self.n_frames):

            # Insert a column
            self.frameTable.insertColumn(i)

            # Make the checkbox
            crt_checkbox = qtw.QPushButton("")
            crt_checkbox.setFixedWidth(30)
            crt_checkbox.clicked.connect(partial(self.changeFrame, frame_id=i))
            self.frame_buttons.append(crt_checkbox)

            # Add the content
            self.frameTable.setCellWidget(0, i, crt_checkbox)

        # Resize the columns
        header = self.frameTable.horizontalHeader()
        for i in range(self.n_frames):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

        # Initialise the display
        self.refreshFrameList()

    # ----------------------------
    # Edit the color of the frames
    def refreshFrameList(self):

        # Get the list of active frames
        frame_list = self.current_track['frame'].to_numpy()

        # Loop over all the buttons
        for i, crt_checkbox in enumerate(self.frame_buttons):

            if i == self.current_frame and i in frame_list:
                crt_color = 'red'
            elif i == self.current_frame:
                crt_color = 'blue'
            elif i in frame_list:
                crt_color = 'orange'
            else:
                crt_color = 'grey'

            crt_checkbox.setStyleSheet("background-color: "+crt_color)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE FRAMES
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Change the current frame being displayed
    def changeFrame(self, frame_id=0):

        # Update the current selected frame
        if frame_id != self.current_frame:
            self.current_frame = frame_id

            # Get the position to draw
            self.current_position = self.current_track[self.current_track['frame'] == self.current_frame]
            try:
                self.current_position = self.current_position[['y','x']].to_numpy()[0]
                self.new_position = np.copy(self.current_position)
            except:
                self.current_position = None
                self.new_position = None

            # Update the entry
            self.frameSelectionEntry.setText(str(frame_id+1))

            # Refresh the display
            self.displayImage()
            self.refreshFrameList()

    ##-\-\-\-\-\-\-\-\-\-\
    ## UPDATE THE POSITION
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------
    # Move the cursor
    def moveCursor(self, move):

        if self.new_position is not None:

            # Get the relative movement
            dy, dx = move

            # Get the new position
            self.new_position = self.new_position + np.array([dy, dx])

            # Refresh the image
            self.displayImage()

    # --------------------------------
    # Reset the position of the cursor
    def resetCursor(self):

        if self.current_position is not None:

            # Initialise the new position
            self.new_position = np.copy(self.current_position)

            # Refresh the image
            self.displayImage()

    # ------------------------------------------
    # Save the cursor position in the trajectory
    def saveCursor(self):

        # Edit the list
        if self.current_position is not None:

            # Save the new_position
            self.current_position = self.new_position

            # Get the id of the row to replace
            row_id = self.current_track.index[(self.current_track['frame'] == self.current_frame).to_list() ][0]

            # Replace X and Y
            self.current_track.at[row_id, 'y'], self.current_track.at[row_id, 'x'] = self.current_position

        # Append to the list
        else:

            # Save the new_position
            self.current_position = self.new_position

            # Replace X and Y
            self.current_track.loc[self.current_frame] = {'y':self.current_position[0], 'x':self.current_position[1], 'frame':int(self.current_frame), 'particle':int(self.current_path)}
            self.current_track.sort_index(inplace=True)

        # Change the saved status
        self.is_saved = False

        # Refresh the frame list
        self.refreshFrameList()
        self.displayImage()

    # ---------------------------
    # Delete the current position
    def deletePosition(self):

        if self.current_position is not None:

            # Get the id of the row to replace
            row_id = self.current_track.index[(self.current_track['frame'] == self.current_frame).to_list() ][0]

            # Drop the position from the dataframe
            self.current_track.drop(index=row_id, inplace=True)

            # Reset the variables
            self.new_position = None
            self.current_position = None

            # Change the saved status
            self.is_saved = False

            # Refresh the frame list
            self.refreshFrameList()
            self.displayImage()

    # ----------------------------------------------------
    # Fill all the empty frames with the current positions
    def fillAllPositions(self):

        # Save the current position
        self.saveCursor()

        # Fill all the next frames if they are empty
        save_frames = True
        scanned_frame = self.current_frame

        # Update frame positions
        while save_frames:
            scanned_frame += 1

            # Append the position
            if scanned_frame not in self.current_track['frame'].unique() and scanned_frame < len( self.image_class.image.display ):

                # Write X and Y
                self.current_track.loc[scanned_frame] = {'y':self.current_position[0], 'x':self.current_position[1], 'frame':int(scanned_frame), 'particle':int(self.current_path)}
                self.current_track.sort_index(inplace=True)

            else:
                save_frames = False

        # Refresh the frame list
        self.refreshFrameList()
        self.displayImage()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------------
    # Create a new empty path
    def createNewPath(self):

        # Check if the modification has been saved yet
        proceed = True
        if not self.is_saved:
            proceed = warningProceedMessage('Modification not saved','The modification on the current path have not been saved yet. Are you sure you want to create a new path?')

        if proceed:

            # Create a new empty dataframe
            new_path = pd.DataFrame({'y':[],'x':[],'frame':np.array([]).astype(int),'particle':np.array([]).astype(int)})

            # Reset the variables
            self.new_position = None
            self.current_position = None

            # Drop the position from the dataframe
            self.current_track = new_path
            self.current_path = int( len( self.image_class.trajectory.positions['particle'].unique() ) )

            # Manage the frame refresh
            crt_frame = self.current_frame
            self.current_frame = -1

            # Change the saved status
            self.is_saved = False

            # Refresh the display
            self.changeFrame(frame_id = crt_frame)

    # -----------------------------------
    # Change the selected path to process
    def changePath(self):

        # Get the path ID
        path_id = int( self.pathSelectionBox.currentText() )

        if path_id != self.current_path:

            # Check if the modification has been saved yet
            proceed = True
            if not self.is_saved:
                proceed = warningProceedMessage('Modification not saved','The modification on the current path have not been saved yet. Are you sure you want to load a new path?')

            if proceed:

                # Manage the frame refresh
                crt_frame = self.current_frame
                self.current_frame = -1

                # Load the path
                self.getPath(path_id = path_id)
                self.changeFrame(frame_id = crt_frame)

    # -----------------------------------------------
    # Save the current modification in the trajectory
    def savePath(self):

        # Remove the previously exisiting path from the trajectory
        if self.current_path in self.image_class.trajectory.positions['particle'].unique():
            self.image_class.trajectory.positions = self.image_class.trajectory.positions[self.image_class.trajectory.positions['particle'] != self.current_path]

        # Append the track to the trajectory
        self.image_class.trajectory.positions = pd.concat([self.image_class.trajectory.positions, self.current_track], ignore_index=True)

        # Refresh the current display
        self.pathSelectionBox.clear()
        self.pathSelectionBox.addItems( self.image_class.trajectory.listTracks().astype(str) )

        # Change the saved status
        self.is_saved = True

        # Retrieve the current tab ID
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Refresh the main display
        self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()
