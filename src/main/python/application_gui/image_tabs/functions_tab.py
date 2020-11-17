from copy import deepcopy
import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.image_class import ImageCollection
from image_processing.modifications import getSubstackSelection, makeSubstack
from trajectory.management import substackTrajectory

from application_gui.common_gui_functions import CAnimationControl

class mainTabFunctions:

    ##-\-\-\-\-\-\-\
    ## EVENT LISTENER
    ##-/-/-/-/-/-/-/

    # -----------------------------
    # React when the tab is changed
    def tabChanged(self, index):

        # Stop the animation
        if self.parent.animation_on:
            self.parent.toggleAnimation(stop=True)

        # Get the number of frames
        n_frames = self.displayedTabs[index].image_class.n_frames
        i_frame = self.displayedTabs[index].image_class.frame
        is_stack = n_frames > 1

        # Edit the number of frames
        self.parent.animationControl.setCurrentFrame(i_frame)
        self.parent.animationControl.setNFrames(n_frames)

        # Update the display
        self.parent.animationSlider.setEnabled(is_stack)
        self.parent.animationControl.setEnabled(is_stack)

        if is_stack:
            self.parent.animationSlider.setMaximum(n_frames-1)
            self.parent.animationControl.lineEdit.setValidator(qtg.QIntValidator(1, n_frames))
        else:
            self.parent.animationSlider.setMaximum(1)
        self.parent.animationSlider.setValue(i_frame)

    # ---------------------------
    # React when a key is pressed
    def keyPressEvent(self, event):

        # Zoom up
        if event.key() == qtc.Qt.Key_Plus:
            self.changeZoom()

        # Zoom down
        if event.key() == qtc.Qt.Key_Minus:
            self.changeZoom(dezoom=True)

        # Next frame
        if event.key() == qtc.Qt.Key_Period or event.key() == qtc.Qt.Key_Greater:
            self.changeFrame()

        # Previous frame
        if event.key() == qtc.Qt.Key_Comma or event.key() == qtc.Qt.Key_Less:
            self.changeFrame(go_back=True)

        event.accept()

    # -------------------------------------
    # Display the selected image in the tab
    def eventFilter(self, object, event):

        try:
            # Right click on the tab bar of the widget
            if object == self.tabBar() and event.type() == qtc.QEvent.MouseButtonPress:
                if event.button() == qtc.Qt.RightButton:

                    # Execute the action
                    self.showTabMenu(event)

                    # Return True to satisfy the event filter
                    return True

        # Handle exceptions and return True to satisfy the event filter
        except:
            pass
        return False

    ##-\-\-\-\
    ## TAB MENU
    ##-/-/-/-/

    # --------------------
    # Display the tab menu
    def showTabMenu(self, event):

        # Get the current tab
        tab_id = self.currentIndex()

        # Display the menu
        contextMenu = qtw.QMenu()

        # Rename the selected tab
        renameTabAction = contextMenu.addAction("Rename")
        renameTabAction.triggered.connect(lambda : self.renameTab(tab_id=tab_id))

        # Copy the selected tab
        copyTabAction = contextMenu.addAction("Copy")
        copyTabAction.triggered.connect(lambda : self.copyTab(tab_id=tab_id))

        contextMenu.addSeparator()

        # Close the selected tab
        renameTabAction = contextMenu.addAction("Close")
        renameTabAction.triggered.connect(lambda : self.closeTab(tab_id=tab_id))

        action = contextMenu.exec_(qtg.QCursor.pos())

    # ----------------------
    # Rename the current tab
    def renameTab(self, tab_id=0):

        # Get the user input
        new_name, is_ok = qtw.QInputDialog.getText( self, 'Rename Tab', 'Enter the new name:', text=self.displayedTabs[tab_id].image_class.name )

        if is_ok and new_name != "":

            # Update the class
            self.displayedTabs[tab_id].image_class.name = new_name

            # Change the displayed name
            self.setTabText(tab_id, new_name)

    # ------------------------------------
    # Make a substack from the current tab
    def substackTab(self, tab_id=0):

        # Get the user selection
        _frame_text = """Enter a range (e.g. 2-14), a range with increment
(e.g. 1-100-2) or a list (e.g. 7,9,25,27)"""
        selection, is_ok = qtw.QInputDialog.getText( self.parent, 'Substack Maker', _frame_text, text="" )

        if is_ok:

            # Convert the input into a list of frames
            selected_frames = getSubstackSelection(selection)

            # Get the previous array
            old_array = self.displayedTabs[tab_id].image_class.image.source
            old_class = self.displayedTabs[tab_id].image_class

            # Make the new frame selection
            substack_array = makeSubstack(old_array, selected_frames)

            # Get the new class name
            old_name = old_class.name.strip() + " (substack)"
            new_name, is_ok = qtw.QInputDialog.getText( self, 'Copy Tab', 'Enter the new name:', text=old_name )
            if not is_ok:
                new_name = old_name

            # Make a new class and replace the values
            new_class = ImageCollection(substack_array, name=new_name)
            new_class.scale = old_class.scale
            new_class.zoom = old_class.zoom
            new_class.contrast_limits = old_class.contrast_limits
            new_class.bitness = old_class.bitness

            # Prepare the image for display
            new_class.rescaleForDisplay()

            # Add the trajectory if needed
            if old_class.trajectory is not None:
                new_trajectory = substackTrajectory(old_class.trajectory, selected_frames)
                new_class.trajectory = new_trajectory

            # Create the new tab
            self.newTab(new_class)

    # --------------------
    # Copy the current tab
    def copyTab(self, tab_id=0):

        # Generate the new name
        old_name = self.displayedTabs[tab_id].image_class.name.strip() + " (copy)"

        # Get the user input
        new_name, is_ok = qtw.QInputDialog.getText( self, 'Copy Tab', 'Enter the new name:', text=old_name )

        if is_ok and new_name != "":

            # Copy the image class
            new_class = deepcopy( self.displayedTabs[tab_id].image_class )
            new_class.name = new_name

            # Create the new tab
            self.newTab(new_class)

    # ------------------------------------------------
    # Delete the current tab and empty the image array
    def closeTab(self, tab_id=0):

        # Get the image class to delete later
        _class_to_delete = self.displayedTabs[tab_id].image_class

        # Delete the tab
        self.displayedTabs[tab_id].tabWidget.close()
        self.displayedTabs[tab_id].tabWidget.deleteLater()
        del self.displayedTabs[tab_id]

        # Remove the index
        self.removeTab(tab_id)

        # Delete the class
        del _class_to_delete

        # Check if the last tab has been closed
        if len(self.displayedTabs) <= 0:
            self.parent.resetActions()
            self.parent.image_on = False

    ##-\-\-\-\-\-\-\-\-\
    ## IMAGE INTERACTION
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Change the zoom of the current image
    def changeZoom(self, dezoom=False, tab_id=None, new_zoom=None):

        # Get the current tab
        if tab_id is None:
            tab_id = self.currentIndex()

        # Get the current zoom value
        old_zoom = self.displayedTabs[tab_id].image_class.zoom

        # Edit the zoom value
        if new_zoom is None:
            if dezoom:
                new_zoom = old_zoom * .95
            else:
                new_zoom = old_zoom * 1.05

        # Apply the zoom
        self.displayedTabs[tab_id].image_class.zoom = new_zoom

        # Refresh the display
        self.displayedTabs[tab_id].displayImage()

    # --------------------------------
    # Change the zoom to fit the frame
    def zoomToFitFrame(self, tab_id=None):

        # Get the current tab
        if tab_id is None:
            tab_id = self.currentIndex()

        # Get the dimension of the current tab
        widget_width = self.displayedTabs[tab_id].scrollArea.frameGeometry().width()
        widget_height = self.displayedTabs[tab_id].scrollArea.frameGeometry().height()

        # Get the dimension of the image
        image_height, image_width = self.displayedTabs[tab_id].image_class.size.tuple

        # Get the zoom factor
        new_zoom = np.amin( [widget_width / image_width, widget_height / image_height] )

        # Apply the zoom
        self.changeZoom(tab_id=tab_id, new_zoom=new_zoom)

    # --------------------------
    # Change the displayed frame
    def changeFrame(self, go_back=False, new_frame=None):

        # Get the current tab and the current displayed frame
        tab_id = self.currentIndex()
        old_frame = self.displayedTabs[tab_id].image_class.frame

        # New frame
        if new_frame is None:
            if go_back:
                new_frame = old_frame - 1
            else:
                new_frame = old_frame + 1

        # Apply the frame
        self.displayedTabs[tab_id].image_class.setFrame(frame_id=new_frame)

        # Refresh the display
        self.displayedTabs[tab_id].displayImage()

        # Refresh the animation control
        i_frame = self.displayedTabs[tab_id].image_class.frame
        self.parent.animationControl.setCurrentFrame(i_frame)
        self.parent.animationSlider.setValue(i_frame)
