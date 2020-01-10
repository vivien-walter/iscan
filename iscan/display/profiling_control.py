import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

sns.set(style="darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.0})

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PIL import Image, ImageQt

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class profilingControlPanel(qtw.QDockWidget):
    def __init__(self, name, parent):
        super(profilingControlPanel, self).__init__(name, parent)

        # Initialize the display
        self.parent = parent

        # Extract the array and its properties
        currentTab, _ = self.parent.getCurrentTab()
        self.array = currentTab.image.stack.frame
        self.position = None

        # Generate the display
        self.mainWidget = qtw.QWidget()
        self.mainWidget.setMinimumWidth(550)
        self.widgetLayout = qtw.QHBoxLayout(self.mainWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        # -----------------------
        # Populate the left panel
        self.leftPanelWidget = qtw.QWidget()
        self.leftPanelLayout = qtw.QVBoxLayout(self.leftPanelWidget)
        # self.leftPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.createSelectionSnapshot(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createProfileDisplay(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createLineSettings(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createFitFunctions(self.leftPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.leftPanelLayout.addWidget(emptyWidget)

        self.leftPanelWidget.setLayout(self.leftPanelLayout)
        self.widgetLayout.addWidget(self.leftPanelWidget)

        self.widgetLayout.addWidget(self.parent.Vseparator())

        # -------------------------
        # Populate the right panel
        self.rightPanelWidget = qtw.QWidget()
        self.rightPanelLayout = qtw.QVBoxLayout(self.rightPanelWidget)
        # self.rightPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.createParametersInput(self.rightPanelLayout)
        self.rightPanelLayout.addWidget(self.parent.Hseparator())
        self.createFitResults(self.rightPanelLayout)
        self.rightPanelLayout.addWidget(self.parent.Hseparator())
        self.createResultsTable(self.rightPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget2 = qtw.QWidget()
        emptyWidget2.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.rightPanelLayout.addWidget(emptyWidget2)

        self.rightPanelWidget.setLayout(self.rightPanelLayout)
        self.widgetLayout.addWidget(self.rightPanelWidget)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setWidget(self.mainWidget)
        self.setFloating(False)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, *args, **kwargs):
        super(qtw.QDockWidget, self).closeEvent(*args, **kwargs)
        self.parent.docks['profiling'] = None
        self.parent.resizeWindowOnDockAction()

    # ---------------------------------------------
    # Generate the display of the current selection
    def createSelectionSnapshot(self, parentWidget):

        # Generate the widget
        self.selectionSnapshotWidget = qtw.QWidget()
        self.selectionSnapshotLayout = qtw.QVBoxLayout(self.selectionSnapshotWidget)
        self.selectionSnapshotLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Current Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.selectionSnapshotLayout.addWidget(widgetName)

        # Create the display
        self.captionCanvas = qtw.QLabel(self.selectionSnapshotWidget)
        self.captionCanvas.setAlignment(qtc.Qt.AlignCenter)
        self.selectionSnapshotLayout.addWidget(self.captionCanvas)

        # Create the position display
        self.currentPositionDisplay = qtw.QLineEdit()
        self.currentPositionDisplay.setEnabled(False)
        self.currentPositionDisplay.setStatusTip(
            "Current position used for the center of the profile."
        )
        self.selectionSnapshotLayout.addWidget(self.currentPositionDisplay)

        # Display the widget
        self.selectionSnapshotWidget.setLayout(self.selectionSnapshotLayout)
        parentWidget.addWidget(self.selectionSnapshotWidget)

    # -----------------------------------
    # Generate the display of the profile
    def createProfileDisplay(self, parentWidget):

        # Generate the widget
        self.profileDisplayWidget = qtw.QWidget()
        self.profileDisplayLayout = qtw.QVBoxLayout(self.profileDisplayWidget)
        self.profileDisplayLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Intensity Profile")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.profileDisplayLayout.addWidget(widgetName)

        # Histogram in a matplotlib figure
        self.profileFigure = plt.Figure(figsize=(3, 2), dpi=50)
        self.profileCanvas = FigureCanvas(self.profileFigure)

        # Set up the figure and axis
        self.profileAxis = self.profileFigure.add_subplot(111)
        self.profileAxis.clear()
        self.profileFigure.subplots_adjust(0, 0, 1, 1)
        self.profileAxis.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        self.profileAxis.tick_params(
            axis="y", which="both", left=False, right=False, labelleft=False
        )

        self.profileCanvas.setStatusTip(
            "Intensity profile at the given location, angle and length."
        )
        self.profileDisplayLayout.addWidget(self.profileCanvas)

        # Checkbox for the pre-fit display
        self.prefitDisplayCheckBox = qtw.QCheckBox("Show pre-fit")
        self.prefitDisplayCheckBox.setChecked(True)
        #self.prefitDisplayCheckBox.toggled.connect(self.plotProfile)
        self.prefitDisplayCheckBox.setStatusTip(
            "Display the pre-fitted function based on the given initial fit parameters."
        )
        self.profileDisplayLayout.addWidget(self.prefitDisplayCheckBox)

        # Display the widget
        self.profileDisplayWidget.setLayout(self.profileDisplayLayout)
        parentWidget.addWidget(self.profileDisplayWidget)

    # -----------------------------------------
    # Generate the controls of the profile line
    def createLineSettings(self, parentWidget):

        # Generate the widget
        self.lineSettingsWidget = qtw.QWidget()
        self.lineSettingsLayout = qtw.QVBoxLayout(self.lineSettingsWidget)
        self.lineSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Line Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.lineSettingsLayout.addWidget(widgetName)

        # Sliders
        self.angleSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.angleSlider.setMinimum(-89.9)  # Set to -89.9 and 89.9 to avoid crashes
        self.angleSlider.setMaximum(89.9)
        self.angleSlider.setValue(0)
        self.angleSlider.valueChanged.connect(self.createProfileLine)
        self.angleSlider.setStatusTip(
            "Modify the angle of the profile line on the image."
        )
        self.lineSettingsLayout.addWidget(qtw.QLabel("Angle"))
        self.lineSettingsLayout.addWidget(self.angleSlider)

        self.lengthSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.lengthSlider.setMinimum(60)  # All the following values are arbitrary
        self.lengthSlider.setMaximum(1200)
        self.lengthSlider.setValue(200)
        self.lengthSlider.valueChanged.connect(self.createProfileLine)
        self.lengthSlider.setStatusTip(
            "Modify the length of the profile line on the image."
        )
        self.lineSettingsLayout.addWidget(qtw.QLabel("Length"))
        self.lineSettingsLayout.addWidget(self.lengthSlider)

        # Display the widget
        self.lineSettingsWidget.setLayout(self.lineSettingsLayout)
        parentWidget.addWidget(self.lineSettingsWidget)

    # ------------------------------------------
    # Generate the selection of the fit function
    def createFitFunctions(self, parentWidget):

        # Generate the widget
        self.fitFunctionWidget = qtw.QWidget()
        self.fitFunctionLayout = qtw.QGridLayout(self.fitFunctionWidget)
        self.fitFunctionLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Fit Process")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.fitFunctionLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Fit function selection
        currentRow += 1
        self.functionGroupButton = qtw.QButtonGroup(self.fitFunctionWidget)

        self.sincFunctionRadiobutton = qtw.QRadioButton("Sinc")
        self.sincFunctionRadiobutton.setChecked(True)
        self.sincFunctionRadiobutton.toggled.connect(self.fitProfile)
        self.sincFunctionRadiobutton.setStatusTip(
            "Select the sine cardinal function for profile fitting."
        )
        self.gaussFunctionRadiobutton = qtw.QRadioButton("Gauss")
        self.gaussFunctionRadiobutton.toggled.connect(self.fitProfile)
        self.gaussFunctionRadiobutton.setStatusTip(
            "Select the gaussian function for profile fitting."
        )
        self.functionGroupButton.addButton(self.sincFunctionRadiobutton)
        self.fitFunctionLayout.addWidget(self.sincFunctionRadiobutton, currentRow, 0)
        self.functionGroupButton.addButton(self.gaussFunctionRadiobutton)
        self.fitFunctionLayout.addWidget(self.gaussFunctionRadiobutton, currentRow, 1)

        # Button to start the fit
        currentRow += 1

        self.makeFitButton = qtw.QPushButton("FIT")
        self.makeFitButton.clicked.connect(self.fitProfile)
        self.makeFitButton.setStatusTip("Fit the profile with the current settings.")
        self.fitFunctionLayout.addWidget(self.makeFitButton, currentRow, 0, 1, -1)

        # Button to store the results of the fit
        currentRow += 1

        self.storeFitButton = qtw.QPushButton("Store results")
        self.storeFitButton.clicked.connect(self.storeProfile)
        self.storeFitButton.setEnabled(False)
        self.storeFitButton.setStatusTip(
            "Store the result of the fit in the table to save it later."
        )
        self.fitFunctionLayout.addWidget(self.storeFitButton, currentRow, 0, 1, -1)

        # Display the widget
        self.fitFunctionWidget.setLayout(self.fitFunctionLayout)
        parentWidget.addWidget(self.fitFunctionWidget)

    # -----------------------------------------------------------
    # Generate the manual input and display of the fit parameters
    def createParametersInput(self, parentWidget):

        # Generate the widget
        self.fitParametersWidget = qtw.QWidget()
        self.fitParametersLayout = qtw.QFormLayout(self.fitParametersWidget)
        self.fitParametersLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Fit Parameters")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.fitParametersLayout.addRow(widgetName, qtw.QWidget())

        self.amplitudeEntry = qtw.QLineEdit()
        self.amplitudeEntry.returnPressed.connect(self.plotProfile)
        self.amplitudeEntry.setStatusTip("Input for the amplitude of the profile.")
        self.amplitudeOutput = qtw.QLineEdit()
        self.amplitudeOutput.setEnabled(False)
        self.amplitudeOutput.setStatusTip("Output for the amplitude of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Amplitude"), self.amplitudeEntry)
        self.fitParametersLayout.addRow("", self.amplitudeOutput)

        self.centerEntry = qtw.QLineEdit()
        self.centerEntry.returnPressed.connect(self.plotProfile)
        self.centerEntry.setStatusTip("Input for the center of the profile.")
        self.centerOutput = qtw.QLineEdit()
        self.centerOutput.setEnabled(False)
        self.centerOutput.setStatusTip("Output for the center of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Center"), self.centerEntry)
        self.fitParametersLayout.addRow("", self.centerOutput)

        self.widthEntry = qtw.QLineEdit()
        self.widthEntry.returnPressed.connect(self.plotProfile)
        self.widthEntry.setStatusTip("Input for the width of the profile.")
        self.widthOutput = qtw.QLineEdit()
        self.widthOutput.setEnabled(False)
        self.widthOutput.setStatusTip("Output for the width of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Width"), self.widthEntry)
        self.fitParametersLayout.addRow("", self.widthOutput)

        self.offsetEntry = qtw.QLineEdit()
        self.offsetEntry.returnPressed.connect(self.plotProfile)
        self.offsetEntry.setStatusTip("Input for the offset of the profile.")
        self.offsetOutput = qtw.QLineEdit()
        self.offsetOutput.setEnabled(False)
        self.offsetOutput.setStatusTip("Output for the offset of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Offset"), self.offsetEntry)
        self.fitParametersLayout.addRow("", self.offsetOutput)

        # Display the widget
        self.fitParametersWidget.setLayout(self.fitParametersLayout)
        parentWidget.addWidget(self.fitParametersWidget)

    # ---------------------------------------------
    # Generate the display of the result of the fit
    def createFitResults(self, parentWidget):

        # Generate the widget
        self.imageValuesWidget = qtw.QWidget()
        self.imageValuesLayout = qtw.QFormLayout(self.imageValuesWidget)
        self.imageValuesLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Image Values")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.imageValuesLayout.addRow(widgetName, qtw.QWidget())

        self.contrastOutput = qtw.QLineEdit()
        self.contrastOutput.setEnabled(False)
        self.contrastOutput.setStatusTip("Contrast of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("Contrast (%)"), self.contrastOutput)

        self.noiseOutput = qtw.QLineEdit()
        self.noiseOutput.setEnabled(False)
        self.noiseOutput.setStatusTip("Noise of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("Noise (%)"), self.noiseOutput)

        self.snrOutput = qtw.QLineEdit()
        self.snrOutput.setEnabled(False)
        self.snrOutput.setStatusTip("Signal-to-Noise Ratio of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("SNR"), self.snrOutput)

        # Display the widget
        self.imageValuesWidget.setLayout(self.imageValuesLayout)
        parentWidget.addWidget(self.imageValuesWidget)

    # ---------------------------------------------
    # Generate the display of the result of the fit
    def createResultsTable(self, parentWidget):

        # Generate the widget
        self.resultsDisplayWidget = qtw.QWidget()
        self.resultsDisplayLayout = qtw.QVBoxLayout(self.resultsDisplayWidget)
        self.resultsDisplayLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Analysis Results")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.resultsDisplayLayout.addWidget(widgetName)

        # Table for the results
        self.resultsTable = qtw.QTableWidget(0, 21)
        self.resultsTable.setHorizontalHeaderLabels(
            [
                "Name",
                "Contrast",
                "ContrastErr",
                "Noise",
                "NoiseErr",
                "SNR",
                "SNRErr",
                "Frame",
                "X",
                "Y",
                "Angle",
                "Length",
                "Fit",
                "Amplitude",
                "AErr",
                "Center",
                "CErr",
                "Width",
                "WErr",
                "Offset",
                "OErr",
            ]
        )
        self.resultsTable.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.resultsTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.resultsTable.cellDoubleClicked.connect(self.tableIsDoubleClicked)
        self.resultsTable.itemSelectionChanged.connect(self.tableSelectionChanged)
        self.resultsDisplayLayout.addWidget(self.resultsTable)

        # Save button
        self.saveButton = qtw.QPushButton("Save Results")
        self.saveButton.clicked.connect(self.saveTableInFile)
        self.saveButton.setStatusTip("Save the table of results in a .csv file.")
        self.resultsDisplayLayout.addWidget(self.saveButton)

        # Display the widget
        self.resultsDisplayWidget.setLayout(self.resultsDisplayLayout)
        parentWidget.addWidget(self.resultsDisplayWidget)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------
    # Update the display of the initial parameters
    def updateInitialParameters(self, parameters):

        # Extract the parameters
        amplitude, width, center, offset = parameters

        # Update the display
        self.amplitudeEntry.setText(str(round(amplitude, 3)))
        self.centerEntry.setText(str(round(center, 3)))
        self.widthEntry.setText(str(round(width, 3)))
        self.offsetEntry.setText(str(round(offset, 3)))

    # -------------------------------------------
    # Update the display of the fitted parameters
    def updateFittedParameters(self, fitParameters, fitErrors):

        # Extract the parameters
        amplitude, width, center, offset = fitParameters
        aErr, wErr, cErr, oErr = fitErrors

        # Update the display
        amplitudeText = str(round(amplitude, 3)) + " ± " + str(round(aErr, 3))
        self.amplitudeOutput.setText(amplitudeText)

        centerText = str(round(center, 3)) + " ± " + str(round(cErr, 3))
        self.centerOutput.setText(centerText)

        widthText = str(round(width, 3)) + " ± " + str(round(oErr, 3))
        self.widthOutput.setText(widthText)

        offsetText = str(round(offset, 3)) + " ± " + str(round(oErr, 3))
        self.offsetOutput.setText(offsetText)

    # -------------------------------------
    # Update the profile line on the screen
    def createProfileLine(self, event=None, makeFit=False):

        # Do not fit if no profile is selected
        if self.position is None:
            return 0

        # Extract the values
        self.angle = self.angleSlider.value()
        self.length = self.lengthSlider.value()

        # Update the line on the image
        currentTab, _ = self.parent.getCurrentTab()
        p1, p2 = currentTab.image.createProfile( self.position, self.angle, self.length )

        # Compute the profile and display it
        self.distance, self.profile = currentTab.image.extractProfile(p1, p2, self.position)

        # Fit profiles if required
        if makeFit or self.parent.controlPanel.liveFitCheckBox.isChecked():
            brightSpot = self.parent.controlPanel.brightSpotCheckBox.isChecked()
            self.initial_parameters = initializeParameters( self.distance, self.profile, brightSpot=brightSpot )
            self.updateInitialParameters( self.initial_parameters )
            self.fitProfile()

        else:
            self.plotProfile()
            pass

    # -----------------------------------------------------------------------------
    # Plot the intensity profile with the current position, angle and length given
    def plotProfile(self):

        # Do not fit if no profile is selected
        if self.position is None:
            return 0

        # Reset the display
        self.profileAxis.clear()

        # Calculate the fitted range
        xMin = self.distance[0]
        xMax = self.distance[-1]
        xStep = (xMax - xMin) / 1000
        self.distance_fitted = np.arange(xMin, xMax + xStep, xStep)

        # Plot the profile
        self.profileAxis.plot(self.distance, self.profile, "k-", linewidth=3)

        # Plot the pre-fit plot
        if self.prefitDisplayCheckBox.isChecked():
            self.profileAxis.plot(
                self.distance_fitted,
                fittedProfile(
                    self.distance_fitted,
                    self.getInitialParameters(),
                    fitType=self.returnFitType(),
                ),
                "r--",
                linewidth=2,
            )

        # Plot the plot
        self.profile_short = fittedProfile(
            self.distance, self.fit_parameters, fitType=self.returnFitType()
        )
        self.profile_fitted = fittedProfile(
            self.distance_fitted, self.fit_parameters, fitType=self.returnFitType()
        )
        self.profileAxis.plot(
            self.distance_fitted, self.profile_fitted, "b-", linewidth=4
        )

        # Refresh the canvas
        self.profileCanvas.draw()

    ##-\-\-\-\-\-\-\
    ## FIT MANAGEMENT
    ##-/-/-/-/-/-/-/

    # -----------------------------
    # Return the type of fit to use
    def returnFitType(self):

        # Lists
        modes = np.array(["sinc", "gauss"])
        buttonState = np.array(
            [
                self.sincFunctionRadiobutton.isChecked(),
                self.gaussFunctionRadiobutton.isChecked(),
            ]
        )

        # Get the enabled mode
        modeIndex = np.where(buttonState == True)[0]

        return modes[modeIndex[0]]

    # ----------------------------------------------
    # Get the initial parameters currently displayed
    def getInitialParameters(self):

        # Retrieve the values
        amplitude = self.amplitudeEntry.text()
        center = self.centerEntry.text()
        width = self.widthEntry.text()
        offset = self.offsetEntry.text()

        # Check the variable type
        amplitude = string2Float(amplitude)
        if amplitude == False:
            amplitude = self.fit_parameters[0]
            self.amplitudeEntry.setText( str(amplitude) )
        center = string2Float(center)
        if center == False:
            center = self.fit_parameters[1]
            self.amplitudeEntry.setText( str(center) )
        width = string2Float(width)
        if width == False:
            width = self.fit_parameters[2]
            self.amplitudeEntry.setText( str(width) )
        offset = string2Float(offset)
        if offset == False:
            offset = self.fit_parameters[3]
            self.amplitudeEntry.setText( str(offset) )

        return [amplitude, width, center, offset]

    # ---------------
    # Fit the profile
    def fitProfile(self):

        # Do not fit if no profile is selected
        if self.position is None:
            return 0

        # Retrieve the initial parameters to use from the UI
        initialParameters = self.getInitialParameters()

        # Fit the profile using the given fit parameters
        self.fit_type = self.returnFitType()
        self.fit_parameters, self.fit_errors = fitProfile(
            self.distance, self.profile, initialParameters, fitType=self.fit_type
        )

        # Update the display
        self.updateFittedParameters(self.fit_parameters, self.fit_errors)
        self.calculateContrastNoise()
        self.plotProfile()

        # Enable the store profile button
        if not self.storeFitButton.isEnabled():
            self.createProfileLine()
            self.storeFitButton.setEnabled(True)

    # ----------------------------------------------------------------
    # Calculate and display the contrast, noise and SNR of the profile
    def calculateContrastNoise(self):

        # Calculate the values
        signal = self.distance, self.profile
        fittedSignal = (
            self.distance,
            fittedProfile(
                self.distance, self.fit_parameters, fitType=self.returnFitType()
            ),
        )
        imageValues, imageValuesErr = computeSNR(
            signal, fittedSignal, self.fit_parameters, self.fit_errors, brightSpot=self.parent.controlPanel.brightSpotCheckBox.isChecked()
        )
        self.currentContrast, self.currentNoise, self.currentSNR = imageValues
        (
            self.currentContrastErr,
            self.currentNoiseErr,
            self.currentSNRErr,
        ) = imageValuesErr

        # Update the display
        contrastText = (
            str(round(self.currentContrast, 3))
            + " ± "
            + str(round(self.currentContrastErr, 3))
        )
        self.contrastOutput.setText(contrastText)
        noiseText = (
            str(round(self.currentNoise, 3))
            + " ± "
            + str(round(self.currentNoiseErr, 3))
        )
        self.noiseOutput.setText(noiseText)
        snrText = (
            str(round(self.currentSNR, 3)) + " ± " + str(round(self.currentSNRErr, 3))
        )
        self.snrOutput.setText(snrText)

    ##-\-\-\-\-\-\-\-\
    ## TABLE MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # -----------------------
    # Populate the data table
    def populateTable(self):

        # Delete the values
        rowCount = self.resultsTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.resultsTable.removeRow(0)

        # Retrieve the data associated with the current image
        currentTab, _ = self.parent.getCurrentTab()
        currentData = currentTab.image.profile_saved

        # Fill the table
        if len(currentData) > 0:
            for i, savedData in enumerate(currentData):

                # Fill the rows
                self.resultsTable.insertRow(i)
                valueList = savedData.getTableValues()

                # Fill the columns
                for j, data in enumerate(valueList):
                    item = qtw.QTableWidgetItem(str(data))
                    self.resultsTable.setItem(i, j, item)

    # --------------------------------------
    # React if table has been double clicked
    def tableIsDoubleClicked(self, row, column):

        # Display the message box
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Question)
        msg.setText("Delete Profile")
        msg.setInformativeText(
            """Do you want to delete this profile from the current memory?"""
        )
        msg.setWindowTitle("")
        msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        returnValue = msg.exec_()

        # Remove the line from the memory
        if returnValue == qtw.QMessageBox.Ok:

            # Remove from table
            self.resultsTable.removeRow(row)

            # Retrieve the data associated with the current image
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.profile_saved.pop(row)

            currentTab.image.updateArrays()

    # -----------------------------------------------------
    # React if rows are selected or deselected in the table
    def tableSelectionChanged(self):

        # List all the selected elements of the table
        currentSelection = self.resultsTable.selectedItems()

        # Retrieve the data associated with the current image
        currentTab, _ = self.parent.getCurrentTab()

        # Loop over all the items
        rowCount = self.resultsTable.rowCount()
        try:
            for i in range(rowCount):

                # Check if the row is currently selected
                currentItem = self.resultsTable.item(i, 0)

                # Change the colour of the profile based on the selection
                if currentItem in currentSelection:
                    currentTab.image.profile_saved[i].colour = 'blue'
                else:
                    currentTab.image.profile_saved[i].colour = 'black'

            # Refresh the display
            currentTab.image.updateArrays()
        except:
            pass

    # ---------------------------------------
    # Store the current profile in the memory
    def storeProfile(self):

        # Retrieve the current tab and profile
        currentTab, _ = self.parent.getCurrentTab()
        currentWidget = currentTab.image
        currentProfile = currentWidget.profile_active

        # Flag data as saved in the tab
        currentTab.saved_data = True

        # Generate the name of the saved profile
        numberStoredData = len(currentWidget.profile_saved)
        currentProfile.name = currentWidget.name + "_" + str(numberStoredData + 1)

        # Save the profile properties
        currentProfile.position = self.position
        currentProfile.angle = self.angle
        currentProfile.length = self.length

        # Save the image informations
        currentProfile.contrast['value'] = round(self.currentContrast, 3)
        currentProfile.contrast['error'] = round(self.currentContrastErr, 3)
        currentProfile.noise['value'] = round(self.currentNoise, 3)
        currentProfile.noise['error'] = round(self.currentNoiseErr, 3)
        currentProfile.snr['value'] = round(self.currentSNR, 3)
        currentProfile.snr['error'] = round(self.currentSNRErr, 3)

        # Save the fit options and parameters
        currentProfile.fit_type = self.fit_type
        currentProfile.addFitParameters( self.fit_parameters, self.fit_errors )

        # Save the profile and fit
        currentProfile.distance = self.distance
        currentProfile.profile = self.profile
        currentProfile.profile_fit = self.profile_short

        # Update profile display
        currentWidget.profile_saved.append( currentProfile )
        currentWidget.profile_active = None
        currentWidget.updateArrays()

        # Update table display
        self.populateTable()

        # Disable the store profile button
        self.storeFitButton.setEnabled(False)

    # ------------------------------------------
    # Save the content of the table in a file(s)
    def saveTableInFile(self):

        # Retrieve the data associated with the current image
        currentTab, _ = self.parent.getCurrentTab()
        profileNumbers = len( currentTab.image.profile_saved )

        # Display an error message if the table is empty
        if profileNumbers < 1:
            errorMessage("ERROR: Not enough data", "At least one profile is required.")

        # Save the results in a file
        else:
            saveTable( self.parent, currentTab.image.profile_saved )

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## LISTENERS FOR UPDATING THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------
    # Update the profile and fit on image interaction
    def updateOnClick(self, position):

        # Save the position
        self.position = position

        # Update the general informations of the profile
        positionText = "(" + str(position[0]) + ";" + str(position[1]) + ")"
        self.currentPositionDisplay.setText(positionText)

        # Update the caption display
        captionArray = cropImage(position, self.array.display)

        self.captionToDisplay = Image.fromarray(captionArray.astype(np.uint8))
        self.pixmapToDisplay = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt(self.captionToDisplay))
        )
        self.captionCanvas.setPixmap(self.pixmapToDisplay)

        # Update the display
        self.createProfileLine(makeFit=True)
        self.storeFitButton.setEnabled(True)

    # ------------------------------
    # Update when the tab is changed
    def updateOnTabChange(self):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Disable any existing active profile
        currentImage.profile_active = None

        # Deselect all selected profiles
        for profile in currentImage.profile_saved:
            profile.colour="black"

        # Reset the stored properties
        self.array = currentImage.stack.frame

        self.position = None
        self.angle = None
        self.length = None

        self.fit_parameters = None
        self.fit_errors = None
        self.distance = None
        self.profile = None
        self.profile_short = None

        # Reset the canvas
        self.profileAxis.clear()
        self.captionCanvas.clear()

        # Reset the display
        self.currentPositionDisplay.setText("")

        self.amplitudeEntry.setText("")
        self.amplitudeOutput.setText("")
        self.centerEntry.setText("")
        self.centerOutput.setText("")
        self.widthEntry.setText("")
        self.widthOutput.setText("")
        self.offsetEntry.setText("")
        self.offsetOutput.setText("")

        self.contrastOutput.setText("")
        self.noiseOutput.setText("")
        self.snrOutput.setText("")

        # Refresh the canvas
        self.profileCanvas.draw()

        # Update the content of the table
        self.populateTable()

        # Refresh the display
        currentImage.updateArrays()
        self.storeFitButton.setEnabled(False)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import errorMessage
from iscan.operations.general_functions import initializeParameters, fitProfile, fittedProfile, string2Float
from iscan.operations.image_calculation import cropImage
from iscan.operations.intensity_profiling import computeSNR, saveTable
