import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.menubar.functions_file import menuBarFileFunctions
from application_gui.menubar.functions_process import menuBarProcessFunctions
from application_gui.menubar.functions_analyze import menuBarAnalyzeFunctions
from application_gui.menubar.functions_tools import menuBarToolsFunctions
from application_gui.menubar.functions_window import menuBarWindowFunctions
from application_gui.menubar.functions_help import menuBarHelpFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## MENUBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class menuBar (menuBarFileFunctions, menuBarProcessFunctions, menuBarAnalyzeFunctions, menuBarToolsFunctions, menuBarWindowFunctions, menuBarHelpFunctions):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent
        self.mainMenu = self.parent.menuBar()
        self.mainMenu.setNativeMenuBar(True)

        # Call the different submenus
        self.createFileMenu()
        self.createProcessMenu()
        self.createAnalyzeMenu()
        self.createToolsMenu()
        self.createWindowMenu()
        self.createHelpMenu()

    ##-\-\-\-\-\-\-\-\-\-\
    ## INTERFACE GENERATION
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Generate the FILE submenu
    def createFileMenu(self):

        # Initialise
        self.fileMenu = self.mainMenu.addMenu("File")

        # Open an image
        self.fileMenu.openImageButton = qtw.QAction("Open...", self.parent)
        self.fileMenu.openImageButton.setShortcut("Ctrl+O")
        self.fileMenu.openImageButton.setStatusTip("Open image or stack.")
        self.fileMenu.openImageButton.triggered.connect(self.callOpenImageWindow)
        self.fileMenu.addAction(self.fileMenu.openImageButton)

        # Open recent files
        self.fileMenu.openRecentSubMenu = qtw.QMenu('Open Recent', self.parent)
        self.fileMenu.openRecentSubMenu.aboutToShow.connect(self.generateOpenRecentList)

        self.fileMenu.addMenu(self.fileMenu.openRecentSubMenu)

        self.fileMenu.addSeparator()

        # Close an image
        self.fileMenu.closeImageButton = qtw.QAction("Close", self.parent)
        self.fileMenu.closeImageButton.setShortcut("Ctrl+W")
        self.fileMenu.closeImageButton.setStatusTip("Close the current tab.")
        self.fileMenu.closeImageButton.triggered.connect(self.callCloseCurrentTab)
        self.fileMenu.addAction(self.fileMenu.closeImageButton)

        # Close all images
        self.fileMenu.closeAllButton = qtw.QAction("Close All", self.parent)
        self.fileMenu.closeAllButton.setShortcut("Ctrl+Shift+W")
        self.fileMenu.closeAllButton.setStatusTip("Close all the tabs.")
        self.fileMenu.closeAllButton.triggered.connect(self.callCloseAllTabs)
        self.fileMenu.addAction(self.fileMenu.closeAllButton)

        # Save image menu
        self.fileMenu.saveAsSubMenu = qtw.QMenu('Save As', self.parent)

        # Single frame
        self.fileMenu.saveSingleFrame = qtw.QAction("Single Frame(s)...", self.parent)
        self.fileMenu.saveSingleFrame.setShortcut("Ctrl+S")
        self.fileMenu.saveSingleFrame.triggered.connect(self.callSaveSingleFrame)
        self.fileMenu.saveAsSubMenu.addAction(self.fileMenu.saveSingleFrame)

        # Gif...
        self.fileMenu.saveWholeStack = qtw.QAction("Stack...", self.parent)
        self.fileMenu.saveWholeStack.setShortcut("Ctrl+Shift+S")
        self.fileMenu.saveWholeStack.triggered.connect(self.callSaveStack)
        self.fileMenu.saveAsSubMenu.addAction(self.fileMenu.saveWholeStack)

        # Avi...
        self.fileMenu.saveAsAvi = qtw.QAction("AVI...", self.parent)
        #self.fileMenu.saveAsAvi.triggered.connect(self.callSaveVideo)
        #self.fileMenu.saveAsSubMenu.addAction(self.fileMenu.saveAsAvi)

        self.fileMenu.addMenu(self.fileMenu.saveAsSubMenu)

        self.fileMenu.addSeparator()

        # Quit the software
        self.fileMenu.closeButton = qtw.QAction("Quit", self.parent)
        self.fileMenu.closeButton.setShortcut("Ctrl+Q")
        self.fileMenu.closeButton.setStatusTip("Close the software.")
        self.fileMenu.closeButton.triggered.connect(self.parent.close)
        self.fileMenu.addAction(self.fileMenu.closeButton)

    # ----------------------------
    # Generate the PROCESS submenu
    def createProcessMenu(self):

        # Initialise
        self.processMenu = self.mainMenu.addMenu("Process Image")

        # Open a adjust submenu
        self.processMenu.adjustSubMenu = qtw.QMenu('Adjust...', self.parent)

        # Background correction
        self.processMenu.backgroundCorrectionButton = qtw.QAction("Background Correction", self.parent)
        self.processMenu.backgroundCorrectionButton.setStatusTip("Remove the background of the image by averaging.")
        self.processMenu.backgroundCorrectionButton.triggered.connect(self.callBackgroundCorrection)
        self.processMenu.adjustSubMenu.addAction(self.processMenu.backgroundCorrectionButton)

        # Brightness and contrast correction
        self.processMenu.contrastCorrectionButton = qtw.QAction("Brightness/Contrast...", self.parent)
        self.processMenu.contrastCorrectionButton.setShortcut("Ctrl+Shift+C")
        self.processMenu.contrastCorrectionButton.setStatusTip("Correct the brightness and contrast of the displayed image.")
        self.processMenu.contrastCorrectionButton.triggered.connect(self.callBrightnessCorrection)
        self.processMenu.adjustSubMenu.addAction(self.processMenu.contrastCorrectionButton)

        # Intensity fluctuation correction
        self.processMenu.fluctuationCorrectionButton = qtw.QAction("Intensity Fluctuations...", self.parent)
        self.processMenu.fluctuationCorrectionButton.setStatusTip("Correct the intensity fluctuations.")
        self.processMenu.fluctuationCorrectionButton.triggered.connect(self.callIntensityFluctuations)
        self.processMenu.adjustSubMenu.addAction(self.processMenu.fluctuationCorrectionButton)

        self.processMenu.adjustSubMenu.addSeparator()

        # Convert dark to bright spots
        self.processMenu.darkToBrightButton = qtw.QAction("Dark to bright...", self.parent)
        self.processMenu.darkToBrightButton.setStatusTip("Transform all dark spots into bright ones.")
        self.processMenu.darkToBrightButton.triggered.connect(self.callDarkToBright)
        self.processMenu.adjustSubMenu.addAction(self.processMenu.darkToBrightButton)

        self.processMenu.addMenu(self.processMenu.adjustSubMenu)

        # Average frames
        self.processMenu.frameAveragingButton = qtw.QAction("Frame Averaging...", self.parent)
        self.processMenu.frameAveragingButton.setStatusTip("Average frames together to process the signal.")
        self.processMenu.frameAveragingButton.triggered.connect(self.callFrameAveraging)
        self.processMenu.addAction(self.processMenu.frameAveragingButton)

        self.processMenu.addSeparator()

        # Make a substack
        self.processMenu.makeSubstackButton = qtw.QAction("Make Substack...", self.parent)
        self.processMenu.makeSubstackButton.setStatusTip("Make a substack of the current stack.")
        self.processMenu.makeSubstackButton.triggered.connect(self.callMakeSubstack)
        self.processMenu.addAction(self.processMenu.makeSubstackButton)

        # Open a crop submenu
        self.processMenu.cropSubMenu = qtw.QMenu('Crop...', self.parent)

        # Crop an image
        self.processMenu.cropImageButton = qtw.QAction("Crop Selection", self.parent)
        self.processMenu.cropImageButton.setShortcut("Ctrl+Shift+X")
        self.processMenu.cropImageButton.setStatusTip("Crop the image on the current tab.")
        self.processMenu.cropImageButton.triggered.connect(self.callCropCurrentImage)
        self.processMenu.cropSubMenu.addAction(self.processMenu.cropImageButton)

        # Crop on the selected particle
        self.processMenu.centerCropButton = qtw.QAction("Center and Crop...", self.parent)
        self.processMenu.centerCropButton.setStatusTip("Center and crop the image around the selected path.")
        self.processMenu.centerCropButton.triggered.connect(self.callCenterCropWindow)
        self.processMenu.cropSubMenu.addAction(self.processMenu.centerCropButton)

        self.processMenu.addMenu(self.processMenu.cropSubMenu)

        # Duplicate an image
        self.processMenu.duplicateImageButton = qtw.QAction("Duplicate...", self.parent)
        self.processMenu.duplicateImageButton.setShortcut("Ctrl+Shift+D")
        self.processMenu.duplicateImageButton.setStatusTip("Duplicate the current tab.")
        self.processMenu.duplicateImageButton.triggered.connect(self.callDuplicateCurrentTab)
        self.processMenu.addAction(self.processMenu.duplicateImageButton)

        # Rename an image
        self.processMenu.renameImageButton = qtw.QAction("Rename...", self.parent)
        self.processMenu.renameImageButton.setStatusTip("Rename the current tab.")
        self.processMenu.renameImageButton.triggered.connect(self.callRenameCurrentTab)
        self.processMenu.addAction(self.processMenu.renameImageButton)

        # Open a zoom
        self.processMenu.zoomSubMenu = qtw.QMenu('Zoom', self.parent)

        # Zoom in
        self.processMenu.zoomInButton = qtw.QAction("In", self.parent)
        self.processMenu.zoomInButton.setShortcut("+")
        self.processMenu.zoomInButton.setStatusTip("Zoom in on the current tab by 5%.")
        self.processMenu.zoomInButton.triggered.connect(lambda : self.callZoomInOutCurrentTab(dezoom=False))
        self.processMenu.zoomSubMenu.addAction(self.processMenu.zoomInButton)

        # Zoom out
        self.processMenu.zoomOutButton = qtw.QAction("Out", self.parent)
        self.processMenu.zoomOutButton.setShortcut("-")
        self.processMenu.zoomOutButton.setStatusTip("Zoom out on the current tab by 5%.")
        self.processMenu.zoomOutButton.triggered.connect(lambda : self.callZoomInOutCurrentTab(dezoom=True))
        self.processMenu.zoomSubMenu.addAction(self.processMenu.zoomOutButton)

        # Zoom back to real scale
        self.processMenu.zoomOriginalButton = qtw.QAction("Original Scale", self.parent)
        self.processMenu.zoomOriginalButton.setShortcut("Ctrl+4")
        self.processMenu.zoomOriginalButton.setStatusTip("Zoom to original scale of the image.")
        self.processMenu.zoomOriginalButton.triggered.connect(self.callZoomBack)
        self.processMenu.zoomSubMenu.addAction(self.processMenu.zoomOriginalButton)

        # Zoom to fit the screen
        self.processMenu.zoomFullButton = qtw.QAction("View 100%", self.parent)
        self.processMenu.zoomFullButton.setShortcut("Ctrl+5")
        self.processMenu.zoomFullButton.setStatusTip("Zoom to fit the whole image on the widget.")
        self.processMenu.zoomFullButton.triggered.connect(self.callZoomToFit)
        self.processMenu.zoomSubMenu.addAction(self.processMenu.zoomFullButton)

        # Zoom to the given value
        self.processMenu.zoomSetButton = qtw.QAction("Set...", self.parent)
        self.processMenu.zoomSetButton.setStatusTip("Zoom to the selected value.")
        self.processMenu.zoomSetButton.triggered.connect(self.callZoomToValue)
        self.processMenu.zoomSubMenu.addAction(self.processMenu.zoomSetButton)

        self.processMenu.addMenu(self.processMenu.zoomSubMenu)

    # ----------------------------
    # Generate the ANALYZE submenu
    def createAnalyzeMenu(self):

        # Initialise
        self.analyzeMenu = self.mainMenu.addMenu("Analyze")

        # Open particle detection window
        self.analyzeMenu.detectParticlesButton = qtw.QAction("Detect Particles...", self.parent)
        self.analyzeMenu.detectParticlesButton.setStatusTip("Detect particles in the image.")
        self.analyzeMenu.detectParticlesButton.triggered.connect(self.callParticleDetectionWindow)
        self.analyzeMenu.addAction(self.analyzeMenu.detectParticlesButton)

        # Load a trajectory in the image class
        self.analyzeMenu.loadTrajectoryButton = qtw.QAction("Load Trajectory", self.parent)
        self.analyzeMenu.loadTrajectoryButton.setStatusTip("Load a trajectory in the open tab.")
        self.analyzeMenu.loadTrajectoryButton.triggered.connect(self.callLoadTrajectory)
        self.analyzeMenu.addAction(self.analyzeMenu.loadTrajectoryButton)

        self.analyzeMenu.addSeparator()

        # Open recent files
        self.analyzeMenu.signalSubMenu = qtw.QMenu('Get Intensity...', self.parent)

        # Analyse the properties of the signals
        self.analyzeMenu.signalAnalysisButton = qtw.QAction("Measure Signals", self.parent)
        self.analyzeMenu.signalAnalysisButton.setStatusTip("Read the properties of the signals on the image.")
        self.analyzeMenu.signalAnalysisButton.triggered.connect(self.callSignalAnalysisWindow)
        self.analyzeMenu.signalSubMenu.addAction(self.analyzeMenu.signalAnalysisButton)

        # Evolution of the signal over time
        self.analyzeMenu.signalEvolutionButton = qtw.QAction("Signals Evolution", self.parent)
        self.analyzeMenu.signalEvolutionButton.setStatusTip("Evolution of the signals properties over time.")
        #self.analyzeMenu.signalEvolutionButton.triggered.connect(self.callParticleDetectionWindow)
        #self.analyzeMenu.signalSubMenu.addAction(self.analyzeMenu.signalEvolutionButton)

        # Evolution of the signal over time
        self.analyzeMenu.signalVsAveragingButton = qtw.QAction("Versus Averaging", self.parent)
        self.analyzeMenu.signalVsAveragingButton.setStatusTip("Evolution of the signals versus frame averaging.")
        self.analyzeMenu.signalVsAveragingButton.triggered.connect(self.callSignalAveragingWindow)
        self.analyzeMenu.signalSubMenu.addAction(self.analyzeMenu.signalVsAveragingButton)

        self.analyzeMenu.addMenu(self.analyzeMenu.signalSubMenu)

        # Analyse the properties of the signals
        self.analyzeMenu.getDiffusivityButton = qtw.QAction("Diffusivity", self.parent)
        self.analyzeMenu.getDiffusivityButton.setStatusTip("Measure the diffusivity of the tracked particles.")
        self.analyzeMenu.getDiffusivityButton.triggered.connect(self.callDiffusitivityAnalysisWindow)
        self.analyzeMenu.addAction(self.analyzeMenu.getDiffusivityButton)

        self.analyzeMenu.addSeparator()

        self.analyzeMenu.setScaleButton = qtw.QAction("Set Scale...", self.parent)
        self.analyzeMenu.setScaleButton.setStatusTip("Detect particles in the image.")
        self.analyzeMenu.setScaleButton.triggered.connect(self.callSetScaleWindow)
        self.analyzeMenu.addAction(self.analyzeMenu.setScaleButton)

    # --------------------------
    # Generate the TOOLS submenu
    def createToolsMenu(self):

        # Initialise
        self.toolsMenu = self.mainMenu.addMenu("Tools")

        # Open a file submenu
        self.toolsMenu.metadataSubMenu = qtw.QMenu('Metadata...', self.parent)

        # Read a metadata file
        self.toolsMenu.readDataButton = qtw.QAction("Read Metadata", self.parent)
        self.toolsMenu.readDataButton.setStatusTip("Read a Metadata file.")
        self.toolsMenu.readDataButton.triggered.connect(self.callReadMetadataWindow)
        self.toolsMenu.metadataSubMenu.addAction(self.toolsMenu.readDataButton)

        # Process all the metadata file in a folder
        self.toolsMenu.searchDataButton = qtw.QAction("Search in Files", self.parent)
        self.toolsMenu.searchDataButton.setStatusTip("Read all the metadata files in a folder.")
        self.toolsMenu.searchDataButton.triggered.connect(self.callSeekMetadataWindow)
        self.toolsMenu.metadataSubMenu.addAction(self.toolsMenu.searchDataButton)

        self.toolsMenu.addMenu(self.toolsMenu.metadataSubMenu)

    # ---------------------------
    # Generate the WINDOW submenu
    def createWindowMenu(self):

        # Initialise
        self.windowMenu = self.mainMenu.addMenu("Window")

        # Open particle detection window
        self.windowMenu.trajectoryControllerButton = qtw.QAction("Trajectory Controller", self.parent)
        self.windowMenu.trajectoryControllerButton.setShortcut("Ctrl+Shift+T")
        self.windowMenu.trajectoryControllerButton.setStatusTip("Open the trajectory manager dock.")
        self.windowMenu.trajectoryControllerButton.triggered.connect(self.callTrajectoryManagerDock)
        self.windowMenu.addAction(self.windowMenu.trajectoryControllerButton)

        self.windowMenu.addSeparator()

    # -------------------------
    # Generate the HELP submenu
    def createHelpMenu(self):

        # Initialise
        self.helpMenu = self.mainMenu.addMenu("Help")

        # Open iSCAN help
        self.helpMenu.iscanHelpButton = qtw.QAction("iSCAN Help...", self.parent)
        self.helpMenu.iscanHelpButton.setStatusTip("Open online help for iSCAN.")
        self.helpMenu.iscanHelpButton.triggered.connect(self.openiSCANBrowser)
        self.helpMenu.addAction(self.helpMenu.iscanHelpButton)

        # Submenu for TrackPy help
        self.helpMenu.trackpySubMenu = qtw.QMenu('TrackPy Help...', self.parent)

        # Open Locate help
        self.helpMenu.locateHelpButton = qtw.QAction("Locate", self.parent)
        self.helpMenu.locateHelpButton.setStatusTip("Open online help for the trackpy.locate function.")
        self.helpMenu.locateHelpButton.triggered.connect(self.openTrackpyLocateBrowser)
        self.helpMenu.trackpySubMenu.addAction(self.helpMenu.locateHelpButton)

        # Open Batch help
        self.helpMenu.batchHelpButton = qtw.QAction("Batch", self.parent)
        self.helpMenu.batchHelpButton.setStatusTip("Open online help for the trackpy.batch function.")
        self.helpMenu.batchHelpButton.triggered.connect(self.openTrackpyBatchBrowser)
        self.helpMenu.trackpySubMenu.addAction(self.helpMenu.batchHelpButton)

        # Open Link help
        self.helpMenu.linkHelpButton = qtw.QAction("Link", self.parent)
        self.helpMenu.linkHelpButton.setStatusTip("Open online help for the trackpy.link function.")
        self.helpMenu.linkHelpButton.triggered.connect(self.openTrackpyLinkBrowser)
        self.helpMenu.trackpySubMenu.addAction(self.helpMenu.linkHelpButton)

        # Open Filter_stubs help
        self.helpMenu.filterStubsHelpButton = qtw.QAction("Filter Stubs", self.parent)
        self.helpMenu.filterStubsHelpButton.setStatusTip("Open online help for the trackpy.filter_stubs function.")
        self.helpMenu.filterStubsHelpButton.triggered.connect(self.openTrackpyFilterBrowser)
        self.helpMenu.trackpySubMenu.addAction(self.helpMenu.filterStubsHelpButton)

        self.helpMenu.addMenu(self.helpMenu.trackpySubMenu)

        self.helpMenu.addSeparator()

        # Open the User settings
        self.helpMenu.userSettingsButton = qtw.QAction("User Settings", self.parent)
        self.helpMenu.userSettingsButton.setStatusTip("Edit the default user settings.")
        self.helpMenu.userSettingsButton.triggered.connect(self.callUserSettingsWindow)
        self.helpMenu.addAction(self.helpMenu.userSettingsButton)

        # Open particle detection window
        self.helpMenu.trackerManagerButton = qtw.QAction("Set Trackers...", self.parent)
        self.helpMenu.trackerManagerButton.setStatusTip("Manage the trackers saved in the memory.")
        self.helpMenu.trackerManagerButton.triggered.connect(self.callTrackerManagerWindow)
        self.helpMenu.addAction(self.helpMenu.trackerManagerButton)

        self.helpMenu.addSeparator()

        # Open the About menu
        self.helpMenu.aboutButton = qtw.QAction("About iSCAN...", self.parent)
        self.helpMenu.aboutButton.setStatusTip("General informations on the software.")
        self.helpMenu.aboutButton.triggered.connect(self.callAboutiSCANWindow)
        self.helpMenu.addAction(self.helpMenu.aboutButton)
