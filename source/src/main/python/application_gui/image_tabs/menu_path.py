import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from trajectory.processing import findPathID, deletePath, deletePoint

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## MENU FOR THE PATH CONTROL
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class pathControlMenu:

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACT WITH THE PATH
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Display the context menu for path
    def showPathMenu(self, event_position):

        # Get the list of particles on the given frame
        crt_positions = self.image_class.trajectory.positions
        crt_positions = crt_positions[crt_positions['frame'] == self.image_class.frame]

        # Get the path of the ID
        path_id = findPathID(event_position, crt_positions)

        # Display the context menu
        contextMenu = qtw.QMenu()

        # Path submenu
        pathSubMenu = contextMenu.addMenu("Path "+str(path_id)+"...")

        # Delete path
        deletePathAction = pathSubMenu.addAction('Delete Path')
        deletePathAction.triggered.connect(lambda : self.deleteSelectedPath(path_id=path_id))

        # Show only the selected path
        if self.parent.disptrack_conf.current_position or self.parent.disptrack_conf.current_path:
            showPathAction = pathSubMenu.addAction('Show all')
            showPathAction.triggered.connect(self.showAllPaths)

        else:
            showPathAction = pathSubMenu.addAction('Show only...')
            showPathAction.triggered.connect(lambda : self.showOnlyCurrentPath(path_id=path_id))

        pathSubMenu.addSeparator()

        # Edit point
        #editPointAction = pathSubMenu.addAction('Edit Point')

        # Delete point
        deletePointAction = pathSubMenu.addAction('Delete Point')
        deletePointAction.triggered.connect(lambda : self.deleteSelectedPoint(path_id=path_id))

        action = contextMenu.exec_(qtg.QCursor.pos())

    ##-\-\-\-\
    ## ACTIONS
    ##-/-/-/-/

    # ------------------------
    # Delete the selected path
    def deleteSelectedPath(self, path_id):

        # Delete the path from the trajectory
        deletePath(path_id, self.image_class.trajectory)

        # Refresh the display
        self.refreshPathList()
        self.displayImage()

    # ---------------------
    # Display all the paths
    def showAllPaths(self):

        # Modify the config
        self.parent.disptrack_conf.current_position = False
        self.parent.disptrack_conf.current_path = False

        # Change the combo box selection
        _combobox = self.parent.docks['tracking'].pathSelectionEntry.comboBox
        _index = _combobox.findText('All', qtc.Qt.MatchFixedString)
        if _index >= 0:
             _combobox.setCurrentIndex(_index)

    # --------------------------
    # Show only the current path
    def showOnlyCurrentPath(self, path_id):

        # Modify the config
        self.parent.disptrack_conf.current_position = True
        self.parent.disptrack_conf.current_path = True

        # Change the combo box selection
        _combobox = self.parent.docks['tracking'].pathSelectionEntry.comboBox
        _index = _combobox.findText(str(path_id), qtc.Qt.MatchFixedString)
        if _index >= 0:
             _combobox.setCurrentIndex(_index)

    # ------------------------
    # Delete the selected path
    def deleteSelectedPoint(self, path_id):

        # Delete the path from the trajectory
        deletePoint(path_id, self.image_class.trajectory, self.image_class.frame)

        # Refresh the display
        self.refreshPathList()
        self.displayImage()
