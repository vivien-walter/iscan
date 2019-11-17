import numpy as np
import os
import sys

from PIL import Image, ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from iscan.display.background_main import interactiveBackgroundWidget
from iscan.display.frame_control import frameControlPanel
from iscan.display.image import imageWidget
from iscan.display.menubar import menuBar
from iscan.display.profiling_control import profilingControlPanel


##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUI(qtw.QMainWindow):
    def __init__(self):
        super(mainGUI,self).__init__()

        # Initialize the properties of the software Main GUI
        self.title = 'iSCAT Analysis'
        self.version = 'v0.1'
        self.currentFrame = 0

        # Generate the display
        self.setWindowTitle(self.title + ' ('+self.version+')')
        self.setWindowIcon(qtg.QIcon('pythonlogo.png'))
        self.menuBar = menuBar(self)

        # Initialise the different control panel
        self.controlPanel = None
        self.trackingPanel = None
        self.profilingPanel = None
        self.correctionWindow = None
        self.contrastWindow = None
        self.statisticWindow = None
        self.isTabDisplayActive = False

        # Populate the window
        self.createEmptyBackground()

        # Complete the initialisation of the display
        self.statusBar()
        self.show()

    #------------------------------------
    # Create the blank background display
    def createEmptyBackground(self):

        # Populate the window
        self.centralWidget = interactiveBackgroundWidget(self)

        # Initialise the tab display
        self.setCentralWidget(self.centralWidget)

    #--------------------------------
    # Create the control docking menu
    def createControlMenu(self):

        self.controlPanel = frameControlPanel("Image Control", self)
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, self.controlPanel)

    #-------------------------------------
    # Create the tab display to add images
    def createTabDisplay(self):

        # Generate the control panel if none
        if self.controlPanel is None:
            self.createControlMenu()

        # Populate the window
        self.centralWidget = qtw.QTabWidget()
        self.centralWidget.currentChanged.connect(self.tabIsChanged)

        # Lists for the tab handling
        self.imageTabs = []
        self.imageTabsNames = []
        self.imageTabsLayout = []
        self.imageTabsImage = []

        # Initialise the tab display
        self.setCentralWidget(self.centralWidget)

        self.isTabDisplayActive = True

    #-------------------------------------
    # Generate the profiling dock controls
    def startProfilingMode(self):

        self.profilingPanel = profilingControlPanel("Intensity Profiler", self)
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.profilingPanel)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## OTHER FUNCTIONS AND STYLES
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    #----------------------------
    # Define the separator widget
    def Hseparator(self):
        separator = qtw.QFrame()
        separator.setFrameShape(qtw.QFrame.HLine)
        separator.setSizePolicy(qtw.QSizePolicy.Expanding,qtw.QSizePolicy.Minimum)
        separator.setLineWidth(1)

        return separator

    #----------------------------
    # Define the separator widget
    def Vseparator(self):
        separator = qtw.QFrame()
        separator.setFrameShape(qtw.QFrame.VLine)
        separator.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        separator.setLineWidth(1)

        return separator

    #-------------------------------------
    # Add a new image tab to the interface
    def addImageTab(self, frames, name="Untitled image", minPV=None, maxPV=None):

        # Update the tab lists
        self.imageTabs.append( qtw.QWidget() )
        self.imageTabsNames.append( name )
        self.imageTabsLayout.append( qtw.QVBoxLayout() )
        self.imageTabsImage.append( imageWidget(self, frames, name, minPV=minPV, maxPV=maxPV) )

        # Populate the tab
        self.imageTabsLayout[-1].setContentsMargins(0, 0, 0, 0)
        self.imageTabsLayout[-1].addWidget( self.imageTabsImage[-1] )
        self.imageTabs[-1].setLayout(self.imageTabsLayout[-1])

        # Append the tab to the window
        self.centralWidget.addTab(self.imageTabs[-1], self.imageTabsNames[-1])

    #-----------------------------
    # Action when a tab is changed
    def tabIsChanged(self, index):

        # Update the zoom of the current image displayed in the tab
        zoomValue = self.imageTabsImage[index].zoom * 100
        self.controlPanel.currentZoomEntry.setText(str(zoomValue))

        # Update the current frame being displayed in the tab
        currentFrame = self.imageTabsImage[index].currentFrame
        self.controlPanel.frameSelectionEntry.setText(str(currentFrame))

        # Update the maximum number of frames in the tab
        maxFrames = len(self.imageTabsImage[index].array)
        self.controlPanel.frameNumberDisplay.setText(str(maxFrames))

        # Update the table display for profiling
        if self.profilingPanel is not None:
            self.profilingPanel.populateTable()

        # Close the statistic display if on and no profile are in memory
        if self.statisticWindow is not None and len(self.imageTabsImage[index].savedData) == 0:
            self.statisticWindow.close()

        # Close the statistic display if on and no profile are in memory
        if self.contrastWindow is not None:
            self.contrastWindow.close()


##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

#--------------------------------------
# Call the main display of the software
def createMainUI():
    main_application = qtw.QApplication([])
    main_gui = mainGUI()
    main_application.exec_()
