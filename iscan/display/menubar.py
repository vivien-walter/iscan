import sip

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from iscan.display.contrast_control import contrastSettingsPanel
from iscan.display.correction_control import backgroundCorrectionPanel
from iscan.display.statistics_display import profilesAnalysisPanel
from iscan.input_output import saveProfiles, openFolder, openFile

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

    # --------------------------
    # Generate the FILE submenu
    def createFileMenu(self):

        # Initialise
        self.fileMenu = self.mainMenu.addMenu("File")

        # Load a folder
        self.fileMenu.loadFolderButton = qtw.QAction("Open Folder", self.parent)
        self.fileMenu.loadFolderButton.setShortcut("Ctrl+O")
        self.fileMenu.loadFolderButton.setStatusTip("Load and process an image folder.")
        self.fileMenu.loadFolderButton.triggered.connect(self.callOpenFolder)
        self.fileMenu.addAction(self.fileMenu.loadFolderButton)

        # Load a file
        self.fileMenu.loadFileButton = qtw.QAction("Open Image", self.parent)
        self.fileMenu.loadFileButton.setShortcut("Ctrl+Shift+O")
        self.fileMenu.loadFileButton.setStatusTip("Load and process an image folder.")
        self.fileMenu.loadFileButton.triggered.connect(self.callOpenFile)
        self.fileMenu.addAction(self.fileMenu.loadFileButton)

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
        self.imageMenu.addAction(self.imageMenu.imageCorrectionButton)

        # Adjust the contrast
        self.imageMenu.adjustContrastButton = qtw.QAction(
            "Adjust Contrast", self.parent
        )
        self.imageMenu.adjustContrastButton.setShortcut("Ctrl+Shift+C")
        self.imageMenu.adjustContrastButton.setStatusTip(
            "Adjust the brightness and contrast of the image."
        )
        self.imageMenu.adjustContrastButton.triggered.connect(self.callContrastWindow)
        self.imageMenu.addAction(self.imageMenu.adjustContrastButton)

        self.imageMenu.addSeparator()

        # Quit the software
        self.imageMenu.closeTabButton = qtw.QAction("Close Current Tab", self.parent)
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
        self.profileMenu.analyseProfilesButton.triggered.connect(
            self.callStatisticsDisplay
        )
        self.profileMenu.addAction(self.profileMenu.analyseProfilesButton)

        self.profileMenu.addSeparator()

        # Save all the profiles
        self.profileMenu.saveTableButton = qtw.QAction(
            "Save Profiles Table", self.parent
        )
        self.profileMenu.saveTableButton.setShortcut("Ctrl+S")
        self.profileMenu.saveTableButton.setStatusTip(
            "Save the table of results in a .csv file."
        )
        self.profileMenu.saveTableButton.triggered.connect(self.callSaveProfileTable)
        self.profileMenu.addAction(self.profileMenu.saveTableButton)

        # Save all the profiles
        self.profileMenu.saveProfilesButton = qtw.QAction(
            "Save Profile Plots", self.parent
        )
        self.profileMenu.saveProfilesButton.setShortcut("Ctrl+Shift+S")
        self.profileMenu.saveProfilesButton.setStatusTip(
            "Save all the profiles in separated .csv files."
        )
        self.profileMenu.saveProfilesButton.triggered.connect(self.callSaveAllProfiles)
        self.profileMenu.addAction(self.profileMenu.saveProfilesButton)

        self.profileMenu.addSeparator()

        # Save all the profiles
        self.profileMenu.eraseProfilesButton = qtw.QAction(
            "Delete Profiles", self.parent
        )
        self.profileMenu.eraseProfilesButton.setStatusTip(
            "Delete all the profiles from the current image."
        )
        self.profileMenu.eraseProfilesButton.triggered.connect(self.callDeleteData)
        self.profileMenu.addAction(self.profileMenu.eraseProfilesButton)

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

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.correctionWindow is None:
            self.parent.correctionWindow = backgroundCorrectionPanel(self.parent)

    # --------------------------------------
    # Display the contrast correction window
    def callContrastWindow(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Open the window if it has not been opened yet
        if self.parent.contrastWindow is None:
            self.parent.contrastWindow = contrastSettingsPanel(self.parent)

    # ----------------------------------------------
    # Close the current tab and refresh the display
    def closeCurrentTab(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Close the current tab
        tabIndex = self.parent.centralWidget.currentIndex()
        self.parent.centralWidget.removeTab(tabIndex)
        del self.parent.imageTabsImage[tabIndex]
        del self.parent.imageTabsLayout[tabIndex]
        del self.parent.imageTabsNames[tabIndex]
        del self.parent.imageTabs[tabIndex]

        # Reload the default display if it as the last tab open
        if self.parent.centralWidget.count() == 0:

            # Reinitialise the lists
            self.parent.imageTabsImage = []
            self.parent.imageTabsLayout = []
            self.parent.imageTabsNames = []
            self.parent.imageTabs = []

            # Delete the tab display
            self.parent.centralWidget.deleteLater()
            self.parent.isTabDisplayActive = False

            # Delete all the opened docks
            self.parent.controlPanel.deleteLater()
            self.parent.controlPanel = None
            if self.parent.profilingPanel is not None:
                self.parent.profilingPanel.deleteLater()
                self.parent.profilingPanel = None
            if self.parent.trackingPanel is not None:
                self.parent.trackingPanel.deleteLater()
                self.parent.trackingPanel = None

            # Reload the default background
            self.parent.createEmptyBackground()

    # ------------------------------
    # Save all profiles in the table
    def callSaveProfileTable(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Check that the profiler menu is open
        if self.parent.profilingPanel is None:

            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Warning)
            msg.setText("ERROR: Option unavailable")
            msg.setInformativeText("""Please open the profiling tool first.""")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            returnValue = msg.exec_()

        # Proceed
        else:
            self.parent.profilingPanel.saveTableInFile()

    # --------------------------------------
    # Display the contrast correction window
    def callStatisticsDisplay(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        if self.parent.statisticWindow is None:
            self.parent.statisticWindow = profilesAnalysisPanel(self.parent)

    # --------------------------------
    # Save all profiles in the memory
    def callSaveAllProfiles(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Retrieve the saved data
        tabIndex = self.parent.centralWidget.currentIndex()
        profileNumbers = len(self.parent.imageTabsImage[tabIndex].savedData)

        # Check if data has already been saved in the memory
        if profileNumbers == 0:

            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Warning)
            msg.setText("ERROR: Not enough data")
            msg.setInformativeText("""At least one profile is required.""")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            returnValue = msg.exec_()

        else:
            saveProfiles(self.parent, self.parent.imageTabsImage[tabIndex].savedData)

    # -------------------------------------------------------
    # Delete all the saved profiles and data from the memory
    def callDeleteData(self):

        # Check if tab display is open
        if not self.parent.isTabDisplayActive:
            self.noImageErrorMessage()
            return 0

        # Retrieve the saved data
        tabIndex = self.parent.centralWidget.currentIndex()
        currentImage = self.parent.imageTabsImage[tabIndex]
        profileNumbers = len(currentImage.savedData)

        # Remove all the informations stored in the memory
        if profileNumbers != 0:
            currentImage.savedProfiles = []
            currentImage.savedData = []

            # Update the table and graph
            self.parent.profilingPanel.populateTable()
            currentImage.updateArrays()

    # ---------------------------------------------------
    # Display the error message when no image are opened
    def noImageErrorMessage(self):

        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Warning)
        msg.setText("ERROR: No opened image")
        msg.setInformativeText("""Open an image first.""")
        msg.setWindowTitle("ERROR")
        msg.setStandardButtons(qtw.QMessageBox.Ok)
        returnValue = msg.exec_()
