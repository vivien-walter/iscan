import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUI(qtw.QMainWindow):
    def __init__(self, application):
        super(mainGUI, self).__init__()

        # Initialize the properties of the software Main GUI
        self.application = application
        self.title = "iSCAT Image Analysis"
        self.version = "beta" #"v1.0.0"

        # Generate the display
        self.setWindowTitle(self.title + " (" + self.version + ")")
        self.setWindowIcon(qtg.QIcon("pythonlogo.png"))
        self.menuBar = menuBar(self)

        # Generate the variables for all the status
        self.tabDisplay = False
        self.controlPanel = None
        self.subWindows = {
        'correction':None,
        'contrast':None,
        'average':None,
        'statistics':None,
        'auto_settings':None,
        'center':None,
        'calibration':None,
        'diffusion':None
        }
        self.docks = {
        'tracking': None,
        'profiling': None,
        }
        self.interaction_type = 'none'

        # Default calibration for all tabs
        self.spatial_calibration = 1.
        self.time_calibration = 1.

        # Populate the window
        self.createDefaultBackground()

        # Complete the initialisation of the display
        self.statusBar()
        applyStyle( self.application )
        self.show()
        self.setFixedSize(self.size())

    # -----------------------------------
    # Create the blank background display
    def createDefaultBackground(self):

        # Populate the window
        self.centralWidget = interactiveBackgroundWidget(self)

        # Initialise the tab display
        self.setCentralWidget(self.centralWidget)
        self.setMaximumSize(qtc.QSize(637, 656)) #self.sizeHint())

    # -------------------------------
    # Create the control docking menu
    def createControlMenu(self):

        self.controlPanel = frameControlPanel("Image Control", self)
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, self.controlPanel)

    # -------------------------------------
    # Create the tab display to add images
    def createTabDisplay(self):

        # Generate the control panel if none
        if self.controlPanel is None:
            self.createControlMenu()

        # Populate the window
        self.centralWidget.deleteLater()
        self.centralWidget = qtw.QTabWidget()
        self.centralWidget.currentChanged.connect(self.tabIsChanged)

        # Lists for the tab handling
        self.imageTabs = []

        # Initialise the tab display
        self.setCentralWidget(self.centralWidget)

        return True

    ##-\-\-\-\-\-\-\
    ## TAB MANAGEMENT
    ##-/-/-/-/-/-/-/

    # -------------------------------------
    # Add a new image tab to the interface
    def addImageTab(self, imageArray, name="Untitled image"):

        # Create the tab display if none has been generated yet
        if self.tabDisplay is False:
            self.tabDisplay = self.createTabDisplay()

        # Update the tab lists
        calibration = [self.spatial_calibration, self.time_calibration]
        self.imageTabs.append( imageTab(self, name, imageArray, calibration) )

        # Append the tab to the window
        self.centralWidget.addTab(self.imageTabs[-1].widget, self.imageTabs[-1].name)
        self.centralWidget.setCurrentIndex( self.centralWidget.count() - 1 )

    # ----------------------------
    # Action when a tab is changed
    def tabIsChanged(self, index):

        # Load the tab currently selected
        currentImageWidget = self.imageTabs[index].image

        # Close opened windows
        self.closeSubWindows()

        # Refresh the docks
        for dock in self.docks.keys():

            currentDock = self.docks[dock]
            if currentDock is not None:
                currentDock.updateOnTabChange()

        # Update the frame controller
        self.controlPanel.updateTabChanged(currentImageWidget)

    # ---------------------
    # Close the current tab
    def closeImageTab(self):

        # Retrieve the current tab
        currentTab, tabIndex = self.getCurrentTab()

        # Check if data are saved in the current tab
        if currentTab.saved_data:
            if not checkSavedData():
                return 0

        # Close all docks first if the last tab is closed
        if self.centralWidget.count() == 1:
            self.closeAllDocks(keep="none")

        # Close the current tab
        self.centralWidget.removeTab(tabIndex)
        del self.imageTabs[tabIndex]

        # Close opened windows
        self.closeSubWindows()

        # Restart the window if all tabs are closed
        if self.centralWidget.count() == 0:
            self.deleteTabDisplay()

    # ------------------------------------
    # Delete the tab display and the docks
    def deleteTabDisplay(self):

        # Reinitialize the list
        self.imageTabs = []

        # Delete the tab display
        self.centralWidget.deleteLater()
        self.tabDisplay = False

        # Delete all the opened docks
        self.controlPanel.deleteLater()
        self.controlPanel = None

        # Reload the default background
        self.createDefaultBackground()

    ##-\-\-\-\-\-\-\-\
    ## DOCK MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # -----------------------------------
    # Open the dock for particle tracking
    def callTrackingDock(self):

        # Close the other docks
        self.interaction_type = "tracking"
        self.closeAllDocks()

        # Proceed in the tracking dock isn't already open
        if self.docks["tracking"] is None:
            self.docks["tracking"] = trackingControlPanel("Particle Tracking", self)
            self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.docks["tracking"])

        # Resize if all docks have been closed
        self.resizeWindowOnDockAction()

    # -------------------------------------
    # Open the dock for intensity profiling
    def callProfilingDock(self):

        # Close the other docks
        self.interaction_type = "profiling"
        self.closeAllDocks()

        # Proceed in the profiling dock isn't already open
        if self.docks["profiling"] is None:
            self.docks["profiling"] = profilingControlPanel("Intensity Profiler", self)
            self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.docks["profiling"])

        # Resize if all docks have been closed
        self.resizeWindowOnDockAction()

    # ----------------------
    # Close all opened docks
    def closeAllDocks(self, keep=None):

        # Find the dock to save
        if keep is None:
            keep = self.interaction_type
        else:
            self.interaction_type = keep

        # Loop over all sub windows
        for dock in self.docks.keys():

            currentDock = self.docks[dock]
            if currentDock is not None:
                currentDock.close()

        # Resize if all docks have been closed
        self.resizeWindowOnDockAction()

    # -------------------------------------------
    # Resize when a dock is closed or dragged out
    def resizeWindowOnDockAction(self):

        # Update the display
        currentTab, _ = self.getCurrentTab()
        currentTab.image.updateArrays()

        # Force all widgets to repaint
        self.centralWidget.update()
        self.controlPanel.update()
        self.update()

        # Resize the window
        self.resize( self.sizeHint() )

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## OTHER FUNCTIONS AND STYLES
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Return the current tab and its index
    def getCurrentTab(self):

        tabIndex = self.centralWidget.currentIndex()
        return self.imageTabs[tabIndex], tabIndex

    # ---------------------------
    # Close all opened subwindows
    def closeSubWindows(self):

        # Loop over all sub windows
        for window in self.subWindows.keys():

            currentWindow = self.subWindows[window]
            if currentWindow is not None:
                currentWindow.close()

    # ---------------------------
    # Define the separator widget
    def Hseparator(self):
        separator = qtw.QFrame()
        separator.setFrameShape(qtw.QFrame.HLine)
        separator.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        separator.setLineWidth(1)

        return separator

    # ---------------------------
    # Define the separator widget
    def Vseparator(self):
        separator = qtw.QFrame()
        separator.setFrameShape(qtw.QFrame.VLine)
        separator.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        separator.setLineWidth(1)

        return separator


##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Call the main display of the software
def createMainUI():
    main_application = qtw.QApplication([])
    main_gui = mainGUI( main_application )
    main_application.exec_()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.app_style import applyStyle
from iscan.display.default_background import interactiveBackgroundWidget
from iscan.display.error_messages import checkSavedData
from iscan.display.frame_control import frameControlPanel
from iscan.display.image_display import imageTab
from iscan.display.menubar import menuBar
from iscan.display.profiling_control import profilingControlPanel
from iscan.display.tracking_control import trackingControlPanel
