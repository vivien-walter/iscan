from PIL import ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.image_tabs.menu_path import pathControlMenu

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## TAB DISPLAY FOR THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageDisplayFunctions( pathControlMenu ):

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACT WITH THE IMAGE
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Interact with the image on a mouse click
    def actionOnClick(self, event=None):

        # Get the click position
        event_position = event.pos().x(), event.pos().y()

        # Get the status of the trajectory sidebar
        if self.parent.docks["tracking"] is not None and self.image_class.trajectory is not None:
            self.showPathMenu(event_position)

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## MODIFY THE TRAJECTORY
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Refresh the list of path
    def refreshPathList(self, path_list=None):

        # Refresh the path list
        if path_list is None:
            self.image_class.path_list = list( self.image_class.trajectory.listTracks().astype(str) )
            self.image_class.path_list.insert(0, 'All')
        else:
            self.image_class.path_list = path_list

        # Edit the content of the combobox
        self.parent.docks["tracking"].pathSelectionEntry.replaceList( self.image_class.path_list )

    ##-\-\-\-\-\-\-\-\-\
    ## DISPLAY THE IMAGE
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Display the selected image in the tab
    def displayImage(self, particles=None, diameter=10):

        # Extract the required values
        zoom = self.image_class.zoom
        self.initialHeight, self.initialWidth = self.image_class.size.tuple

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( self.image_class.image.frame ))
        )

        # Rescale the pixmap
        width, height = (
            int(self.initialWidth * zoom),
            int(self.initialHeight * zoom),
        )
        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # ------------------------
        # Add drawing on the image

        # Tracking preview
        if particles is not None:
            self.drawPositions(particles, diameter=diameter)

        # Tracking display
        else:
            if self.image_class.trajectory is not None and self.parent.show_trajectory:
                self.drawTrajectory()

        # Update the display
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )
        self.scrollAreaImage.adjustSize()

    ##-\-\-\-\-\-\-\-\-\
    ## DRAW ON THE IMAGE
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Get the conditions for custom displays
    def _get_conditions(self):

        # Show only current selection
        if self.parent.docks['tracking'] is not None:

            # Check the selection on the combobox
            _is_all = self.parent.docks['tracking'].pathSelectionEntry.comboBox.currentText() == 'All'
            if not _is_all:
                selected_id = int(self.parent.docks['tracking'].pathSelectionEntry.comboBox.currentText())
            else:
                selected_id = -1

            # Set the booleans for the position
            show_one_position = self.parent.disptrack_conf.current_position and not _is_all
            color_one_position = self.parent.disptrack_conf.color_position and not _is_all and not show_one_position

            # Set the booleans for the path
            show_one_path = self.parent.disptrack_conf.current_path and not _is_all
            color_one_path = self.parent.disptrack_conf.color_path and not _is_all and not show_one_path

        else:
            show_one_position = False
            color_one_position = False
            show_one_path = False
            color_one_path = False
            selected_id = -1

        return [show_one_position, color_one_position], [show_one_path, color_one_path], selected_id

    # --------------------------------
    # Draw the particles on the screen
    def drawPositions(self, particles=None, ids=None, diameter=10, custom_display=None, selected_id = -1):

        # Conditions for color display
        if ids is not None and custom_display is not None:
            show_one_position, color_one_position = custom_display
        else:
            show_one_position = color_one_position = False

        # Extract the zoom value
        zoom = self.image_class.zoom

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Draw all the different elements
        for i, position in enumerate(particles):

            # Get the default settings
            color = qtc.Qt.red
            _show_current = True

            # Check the conditions
            if ids is not None:

                # Show the current particles
                _show_current = not show_one_position or ids[i] == selected_id

                # Color the particles
                if not show_one_position and color_one_position and ids[i] != selected_id:
                    color = qtc.Qt.blue

            # Display the current particle
            if _show_current:

                # Extract the position
                y, x  = position

                # Rescale the object position
                x *= zoom
                y *= zoom

                # Get the circle limits
                radius = diameter/2 * zoom
                xmin, ymin = x - radius, y - radius

                # Draw the point on the canvas
                painter.setPen(qtg.QPen(color, 3*zoom, qtc.Qt.SolidLine))
                painter.drawEllipse(xmin,ymin,2*radius,2*radius)

        painter.end()

    # ---------------------------
    # Draw the path on the screen
    def drawPath(self, particle_path, color=qtc.Qt.red):

        # Extract the zoom value
        zoom = self.image_class.zoom

        # Rescale the path
        particle_path = particle_path * zoom

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        painter.setPen(qtg.QPen(color, 3*zoom, qtc.Qt.SolidLine))

        # Generate the path based on the given list
        coord_path = [qtc.QPoint(x,y) for (y,x) in particle_path]
        painter.drawPolyline(qtg.QPolygon(coord_path))

        painter.end()

    # ---------------------------------
    # Draw the trajectory on the screen
    def drawTrajectory(self):

        # Get the custom display conditions
        position_conditions, path_conditions, selected_id = self._get_conditions()

        # Plot the tracks
        if self.parent.disptrack_conf.show_paths and self.image_class.n_frames > 1:

            # Extract the conditions
            show_one_path, color_one_path = path_conditions

            # Plot the lines
            for path_id in self.image_class.trajectory.listTracks():

                # Get the default settings
                color = qtc.Qt.red
                _show_current = not show_one_path or path_id == selected_id

                # Color the particles
                if not show_one_path and color_one_path and path_id != selected_id:
                    color = qtc.Qt.blue

                # Select the path
                if _show_current:
                    crt_path = self.image_class.trajectory.positions
                    crt_path = crt_path[crt_path['particle'] == path_id]
                    crt_path = crt_path[['y','x']]

                    # Plot the path
                    self.drawPath(crt_path.to_numpy(), color=color)

        # Plot the positions
        if self.parent.disptrack_conf.show_positions:

            # Get the current frame
            frame = self.image_class.frame

            # Refine the trajectory to get the current frame
            crt_positions = self.image_class.trajectory.positions
            crt_positions = crt_positions[crt_positions['frame'] == frame]
            crt_ids = crt_positions['particle'].to_numpy()
            crt_positions = crt_positions[['y','x']].to_numpy()

            # Plot the positions
            self.drawPositions(particles=crt_positions, ids=crt_ids, diameter=21, custom_display=position_conditions, selected_id=selected_id) # Use 21 as defaut diameter
