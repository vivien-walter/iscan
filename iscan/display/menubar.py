import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## MENUBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/


class menuBar:
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent
        self.mainMenu = self.parent.menuBar()
        self.mainMenu.setNativeMenuBar(False)

        # Call the different submenus
        self.createFileMenu()
        self.createImageMenu()
        self.createProfileMenu()
        self.createTrackingMenu()

    # --------------------------
    # Generate the FILE submenu
    def createFileMenu(self):

        # Initialise
        self.fileMenu = self.mainMenu.addMenu("File")

        # Open a file submenu
        self.fileMenu.openSubMenu = qtw.QMenu('Open...', self.parent)

        # Load a folder
        self.fileMenu.loadFolderButton = qtw.QAction("Open Folder", self.parent)
        self.fileMenu.loadFolderButton.setShortcut("Ctrl+O")
        self.fileMenu.loadFolderButton.setStatusTip("Load and process an image folder.")
        self.fileMenu.loadFolderButton.triggered.connect(self.callOpenFolder)
        self.fileMenu.openSubMenu.addAction(self.fileMenu.loadFolderButton)

        # Load a file
        self.fileMenu.loadFileButton = qtw.QAction("Open Image", self.parent)
        self.fileMenu.loadFileButton.setStatusTip("Load and process an image folder.")
        self.fileMenu.loadFileButton.triggered.connect(self.callOpenFile)
        self.fileMenu.openSubMenu.addAction(self.fileMenu.loadFileButton)

        self.fileMenu.addMenu(self.fileMenu.openSubMenu)

        # Save a file submenu
        self.fileMenu.saveSubMenu = qtw.QMenu('Save...', self.parent)

        # Save a stack
        self.fileMenu.saveStackButton = qtw.QAction("Save Stack", self.parent)
        self.fileMenu.saveStackButton.setShortcut("Ctrl+S")
        self.fileMenu.saveStackButton.setStatusTip("Save an image stack.")
        #self.fileMenu.saveStackButton.triggered.connect(self.callOpenFolder)
        self.fileMenu.saveSubMenu.addAction(self.fileMenu.saveStackButton)

        # Save a single image
        self.fileMenu.saveImageButton = qtw.QAction("Save Image", self.parent)
        self.fileMenu.saveImageButton.setStatusTip("Save the current image.")
        #self.fileMenu.saveImageButton.triggered.connect(self.callOpenFile)
        self.fileMenu.saveSubMenu.addAction(self.fileMenu.saveImageButton)

        self.fileMenu.addMenu(self.fileMenu.saveSubMenu)

        self.fileMenu.addSeparator()

        # Quit the software
        self.fileMenu.closeButton = qtw.QAction("Quit", self.parent)
        self.fileMenu.closeButton.setShortcut("Ctrl+Q")
        self.fileMenu.closeButton.setStatusTip("Close the software.")
        self.fileMenu.closeButton.triggered.connect(qtw.qApp.quit)
        self.fileMenu.addAction(self.fileMenu.closeButton)

    # --------------------------
    # Generate the IMAGE submenu
    def createImageMenu(self):

        # Initialise
        self.imageMenu = self.mainMenu.addMenu("Image")

        # Image correction submenu
        self.imageMenu.imageCorrectionSubmenu = qtw.QMenu("Image Correction", self.parent)

        # Background correct the image
        self.imageMenu.imageCorrectionButton = qtw.QAction(
            "Background Correction", self.parent
        )
        self.imageMenu.imageCorrectionButton.setShortcut("Shift+C")
        self.imageMenu.imageCorrectionButton.setStatusTip(
            "Apply a background correction to the image."
        )
        self.imageMenu.imageCorrectionButton.triggered.connect(
            self.callCorrectionWindow
        )
        self.imageMenu.imageCorrectionSubmenu.addAction(self.imageMenu.imageCorrectionButton)

        # Adjust the contrast
        self.imageMenu.adjustContrastButton = qtw.QAction(
            "Adjust Contrast", self.parent
        )
        self.imageMenu.adjustContrastButton.setShortcut("Ctrl+Shift+C")
        self.imageMenu.adjustContrastButton.setStatusTip(
            "Adjust the brightness and contrast of the image."
        )
        self.imageMenu.adjustContrastButton.triggered.connect(self.callContrastWindow)
        self.imageMenu.imageCorrectionSubmenu.addAction(self.imageMenu.adjustContrastButton)

        self.imageMenu.addSeparator()

        # Average frames
        self.imageMenu.averageImageButton = qtw.QAction(
            "Average Frames", self.parent
        )
        self.imageMenu.averageImageButton.setStatusTip(
            "Average the frames of the image stack."
        )
        self.imageMenu.averageImageButton.triggered.connect(self.callAverageWindow)
        self.imageMenu.imageCorrectionSubmenu.addAction(self.imageMenu.averageImageButton)

        self.imageMenu.addMenu(self.imageMenu.imageCorrectionSubmenu)

        # Spatial and time calibration of the stack
        self.imageMenu.imageCalibrationButton = qtw.QAction(
            "Image Calibration", self.parent
        )
        self.imageMenu.imageCalibrationButton.setStatusTip(
            "Calibrate the spatial and time resolution of the image stack."
        )
        self.imageMenu.imageCalibrationButton.triggered.connect(self.callCalibrationWindow)
        self.imageMenu.addAction(self.imageMenu.imageCalibrationButton)

        self.imageMenu.addSeparator()

        # Quit the software
        self.imageMenu.closeTabButton = qtw.QAction("Close Current Tab", self.parent)
        self.imageMenu.closeTabButton.setShortcut("Ctrl+Shift+Q")
        self.imageMenu.closeTabButton.setStatusTip(
            "Close the current tab displayed on the screen."
        )
        self.imageMenu.closeTabButton.triggered.connect(self.closeCurrentTab)
        self.imageMenu.addAction(self.imageMenu.closeTabButton)

    # --------------------------
    # Generate the PROFILE submenu
    def createProfileMenu(self):

        # Initialise
        self.profileMenu = self.mainMenu.addMenu("Profiles")

        # Analyse the stats
        self.profileMenu.analyseProfilesButton = qtw.QAction(
            "Profiles Statistics", self.parent
        )
        self.profileMenu.analyseProfilesButton.setStatusTip(
            "Analyse the profiles stored in memory."
        )
        self.profileMenu.analyseProfilesButton.triggered.connect( self.callStatisticsDisplay )
        self.profileMenu.addAction(self.profileMenu.analyseProfilesButton)

        self.profileMenu.addSeparator()

        # Save profile submenu
        self.profileMenu.saveProfileSubmenu = qtw.QMenu("Save Profiles...", self.parent)

        # Save all the profiles
        self.profileMenu.saveTableButton = qtw.QAction(
            "Save Table", self.parent
        )
        self.profileMenu.saveTableButton.setStatusTip(
            "Save the table of results in a .csv file."
        )
        self.profileMenu.saveTableButton.triggered.connect(self.callSaveProfileTable)
        self.profileMenu.saveProfileSubmenu.addAction(self.profileMenu.saveTableButton)

        # Save all the profiles
        self.profileMenu.saveProfilesButton = qtw.QAction(
            "Save Plots", self.parent
        )
        self.profileMenu.saveProfilesButton.setStatusTip(
            "Save all the profiles in separated .csv files."
        )
        self.profileMenu.saveProfilesButton.triggered.connect(self.callSaveAllProfiles)
        self.profileMenu.saveProfileSubmenu.addAction(self.profileMenu.saveProfilesButton)

        self.profileMenu.addMenu(self.profileMenu.saveProfileSubmenu)

        # Save all the profiles
        self.profileMenu.eraseProfilesButton = qtw.QAction(
            "Delete Profiles", self.parent
        )
        self.profileMenu.eraseProfilesButton.setStatusTip(
            "Delete all the profiles from the current image."
        )
        self.profileMenu.eraseProfilesButton.triggered.connect(self.callDeleteProfileData)
        self.profileMenu.addAction(self.profileMenu.eraseProfilesButton)

    # --------------------------
    # Generate the TRACKING submenu
    def createTrackingMenu(self):

        # Initialise
        self.trackingMenu = self.mainMenu.addMenu("Tracking")

        # Track everything
        self.trackingMenu.trackPyButton = qtw.QAction(
            "General Tracking", self.parent
        )
        self.trackingMenu.trackPyButton.setStatusTip(
            "Process the whole image with TrackPy."
        )
        self.trackingMenu.trackPyButton.triggered.connect(self.getAllPaths)
        self.trackingMenu.addAction(self.trackingMenu.trackPyButton)

        self.trackingMenu.addSeparator()

        # Path operation submenu
        self.trackingMenu.pathOperationMenu = qtw.QMenu('Path Operations...', self.parent)

        self.trackingMenu.centerPathButton = qtw.QAction(
            "Center Path", self.parent
        )
        self.trackingMenu.centerPathButton.setStatusTip(
            "Open a new image centered on the current path."
        )
        self.trackingMenu.centerPathButton.triggered.connect(self.callCenterPath)
        self.trackingMenu.pathOperationMenu.addAction(self.trackingMenu.centerPathButton)

        # Track everything
        self.trackingMenu.computeDiffusionButton = qtw.QAction(
            "Compute Diffusion", self.parent
        )
        self.trackingMenu.computeDiffusionButton.setStatusTip(
            "Measure the coefficient of diffusion."
        )
        self.trackingMenu.computeDiffusionButton.triggered.connect(self.callDiffusitivityDisplay)
        self.trackingMenu.pathOperationMenu.addAction(self.trackingMenu.computeDiffusionButton)

        self.trackingMenu.addMenu(self.trackingMenu.pathOperationMenu)

        # Path operation submenu
        self.trackingMenu.savePathMenu = qtw.QMenu('Save Path...', self.parent)

        self.trackingMenu.saveCsvButton = qtw.QAction(
            "As CSV", self.parent
        )
        self.trackingMenu.saveCsvButton.setStatusTip(
            "Save the current path in a .csv file."
        )
        self.trackingMenu.saveCsvButton.triggered.connect(self.callSaveCsvFile)
        self.trackingMenu.savePathMenu.addAction(self.trackingMenu.saveCsvButton)

        # Track everything
        self.trackingMenu.saveXmlButton = qtw.QAction(
            "As XML", self.parent
        )
        self.trackingMenu.saveXmlButton.setStatusTip(
            "Save the current path in a .xml file."
        )
        self.trackingMenu.saveXmlButton.triggered.connect(self.callSaveXmlFile)
        self.trackingMenu.savePathMenu.addAction(self.trackingMenu.saveXmlButton)

        self.trackingMenu.addMenu(self.trackingMenu.savePathMenu)

        self.trackingMenu.addSeparator()

        # Delete all paths
        self.trackingMenu.deletePathButton = qtw.QAction(
            "Delete Paths", self.parent
        )
        self.trackingMenu.deletePathButton.setStatusTip(
            "Delete all the paths in the memory of the current image."
        )
        self.trackingMenu.deletePathButton.triggered.connect(self.callDeletePathData)
        self.trackingMenu.addAction(self.trackingMenu.deletePathButton)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## FUNCTIONS USED IN THE MENU BAR
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Open the selected folder
    def callOpenFolder(self):
        openFolder(self.parent)

    # -----------------------
    # Open the selected file
    def callOpenFile(self):
        openFile(self.parent)

    # --------------------------------------
    # Display the contrast correction window
    def callCorrectionWindow(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.subWindows['correction'] is None:
            self.parent.subWindows['correction'] = backgroundCorrectionPanel(self.parent)
        else:
            errorAlreadyOpen()

    # --------------------------------------
    # Display the contrast correction window
    def callContrastWindow(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.subWindows['contrast'] is None:
            self.parent.subWindows['contrast'] = contrastSettingsPanel(self.parent)
        else:
            errorAlreadyOpen()

    # --------------------------------------
    # Display the contrast correction window
    def callAverageWindow(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.subWindows['average'] is None:
            self.parent.subWindows['average'] = frameAveragingPanel(self.parent)
        else:
            errorAlreadyOpen()

    # --------------------------------------
    # Display the contrast correction window
    def callCalibrationWindow(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.subWindows['calibration'] is None:
            self.parent.subWindows['calibration'] = imageCalibrationPanel(self.parent)
        else:
            errorAlreadyOpen()

    # ----------------------------------------------
    # Close the current tab and refresh the display
    def closeCurrentTab(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        self.parent.closeImageTab()

    # -------------------------------------
    # Display the profile statistics window
    def callStatisticsDisplay(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        if self.parent.subWindows['statistics'] is None:

            # Retrieve the current tab being displayed
            currentTab, _ = self.parent.getCurrentTab()
            if len( currentTab.image.profile_saved ) < 2:
                errorMessage("ERROR: Not enough data", """At least two profiles need to be saved in the memory to perform statistics.""")
                return 0

            self.parent.subWindows['statistics'] = profilesAnalysisPanel(self.parent)

        else:
            errorAlreadyOpen()

    # ------------------------------
    # Save all profiles in the table
    def callSaveProfileTable(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.saveProfileTable()

    # --------------------------------
    # Save all profiles in the memory
    def callSaveAllProfiles(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.saveAllProfiles()

    # ----------------------------------------
    # Delete the profiles stored in the memory
    def callDeleteProfileData(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.clearAllProfiles()

    # ------------------------------------------
    # Automatic track all particles in the stack
    def getAllPaths(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        trackingDock = self.parent.docks['tracking']
        if trackingDock is None:
            errorMessage("ERROR: Tracking dock not open", """This function requires the tracking particle dock to be opened.""")
            return 0

        # Retrieve the settings
        trackingParameters = trackingDock.getAutomaticParameters()
        trackingParameters['invert'] = not self.parent.controlPanel.brightSpotCheckBox.isChecked()

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image
        generateAutomaticPaths(currentImage, currentImage.stack.array, tracking_option=trackingParameters)

        # Refresh the display
        trackingDock.updateOnTabChange()

    # -------------------------------------
    # Display the profile statistics window
    def callCenterPath(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        if self.parent.subWindows['center'] is None:

            # Retrieve the current tab being displayed
            currentTab, _ = self.parent.getCurrentTab()
            if currentTab.image.path_active is None:
                errorMessage("ERROR: Not enough data", """At least one path needs to be saved in the memory to center the image on it.""")
                return 0

            if currentTab.image.path_active.positions is None:
                errorMessage("ERROR: No positions", """There is no position to center on in the selected path.""")
                return 0

            if currentTab.image.path_active.positions.shape[0] != currentTab.image.stack.n_frames:
                errorMessage("ERROR: Not enough positions", """The position of the particle should be given on all frame to center the image on it.
Use the Path Completion function to fill the path.""")
                return 0

            self.parent.subWindows['center'] = centerPathPanel(self.parent)

        else:
            errorAlreadyOpen()

    # -------------------------------------
    # Display the profile statistics window
    def callDiffusitivityDisplay(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        if self.parent.subWindows['diffusion'] is None:

            # Retrieve the current tab being displayed
            currentTab, _ = self.parent.getCurrentTab()
            if currentTab.image.path_active is None:
                errorMessage("ERROR: Not enough data", """At least one path needs to be saved in the memory to center the image on it.""")
                return 0

            if currentTab.image.path_active.positions is None:
                errorMessage("ERROR: No positions", """There is no position to center on in the selected path.""")
                return 0

            if currentTab.image.path_active.positions.shape[0] != currentTab.image.stack.n_frames:
                errorMessage("ERROR: Not enough positions", """The position of the particle should be given on all frame to center the image on it.
Use the Path Completion function to fill the path.""")
                return 0

            self.parent.subWindows['diffusion'] = diffusitivityMeasurementPanel(self.parent)

        else:
            errorAlreadyOpen()

    # ------------------------------------
    # Save the current path in a .csv file
    def callSaveCsvFile(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        trackingDock = self.parent.docks['tracking']
        if trackingDock is None:
            errorMessage("ERROR: Tracking dock not open", """This function requires the tracking particle dock to be opened.""")
            return 0

        # Call the save function of the tracking dock
        trackingDock.saveCurrentPath(file_type='csv')

    # ------------------------------------
    # Save the current path in a .csv file
    def callSaveXmlFile(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        trackingDock = self.parent.docks['tracking']
        if trackingDock is None:
            errorMessage("ERROR: Tracking dock not open", """This function requires the tracking particle dock to be opened.""")
            return 0

        # Call the save function of the tracking dock
        trackingDock.saveCurrentPath(file_type='xml')

    # -------------------------------------
    # Delete the paths stored in the memory
    def callDeletePathData(self):
        if self.parent.tabDisplay is False:
            errorNoImage()
            return 0

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.clearAllPaths()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.average_window import frameAveragingPanel
from iscan.display.calibration_window import imageCalibrationPanel
from iscan.display.center_window import centerPathPanel
from iscan.display.contrast_window import contrastSettingsPanel
from iscan.display.correction_window import backgroundCorrectionPanel
from iscan.display.diffusitivity_window import diffusitivityMeasurementPanel
from iscan.display.error_messages import errorNoImage, errorAlreadyOpen, errorMessage
from iscan.display.statistics_window import profilesAnalysisPanel
from iscan.input_output.open_images import openFile, openFolder
from iscan.operations.particle_tracking import generateAutomaticPaths
