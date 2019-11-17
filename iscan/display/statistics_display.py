import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.})

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from iscan.input_output import saveAllStats, saveStats

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class profilesAnalysisPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(profilesAnalysisPanel, self).__init__(parent)

        self.parent = parent

        # Check how many data are stored in the memory
        tabIndex = parent.centralWidget.currentIndex()
        profileNumbers = len(parent.imageTabsImage[tabIndex].savedData)

        # Display the window if statistics are in the table
        if profileNumbers >= 2:

            # Get the data
            self.extractData( parent.imageTabsImage[tabIndex].savedData )

            # Generate the window
            self.createWindowDisplay(parent)
            self.plotAnalysis()

        else:
            # Display the message box
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Warning)
            msg.setText("ERROR: Not enough data")
            msg.setInformativeText("""At least two profiles need to be saved in the memory to perform statistics.""")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            returnValue = msg.exec_()

            # Reinitialise the display
            parent.statisticWindow = None

    #---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event):
        event.accept()
        self.parent.statisticWindow = None

    #----------------------------------
    # Generation of the analysis window
    def createWindowDisplay(self, parent):

        # Initialise the subwindow
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle('Profile Statistics')

        # Populate the panel
        self.createStatsDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createSelectionDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createActionButtons(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)

        self.show()

    #---------------------------------------------
    # Generate the statistics histogram and values
    def createStatsDisplay(self, parentWidget):

        # Generate the widget
        self.statsDisplayWidget = qtw.QWidget()
        self.statsDisplayLayout = qtw.QGridLayout(self.statsDisplayWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Statistics")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.statsDisplayLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Histogram in a matplotlib figure
        currentRow += 1
        self.statsFigure = plt.Figure(figsize=(3,2), dpi=50)
        self.statsCanvas = FigureCanvas(self.statsFigure)
        self.statsCanvas.setStatusTip(
            "Distribution of the given parameter."
        )

        # Initialise the graph
        self.statsAxis = self.statsFigure.add_subplot(111)
        self.statsAxis.clear()
        self.statsFigure.subplots_adjust(0,0,1,1)
        self.statsAxis.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
        self.statsAxis.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)

        self.statsDisplayLayout.addWidget(self.statsCanvas, currentRow, 0, 1, -1)

        # Statistics - Mean value
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("Mean"), currentRow, 0)
        self.meanOutput = qtw.QLineEdit()
        self.meanOutput.setEnabled(False)
        self.meanOutput.setStatusTip(
            "Mean value of the selected parameter."
        )
        self.statsDisplayLayout.addWidget(self.meanOutput, currentRow, 1)

        # Statistics - St. Dev.
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("St. Dev."), currentRow, 0)
        self.stdOutput = qtw.QLineEdit()
        self.stdOutput.setEnabled(False)
        self.stdOutput.setStatusTip(
            "Standard deviation of the selected parameter."
        )
        self.statsDisplayLayout.addWidget(self.stdOutput, currentRow, 1)

        # Statistics - Spearman's Rho
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("Spearman's rho"), currentRow, 0)
        self.spearmanROutput = qtw.QLineEdit()
        self.spearmanROutput.setEnabled(False)
        self.spearmanROutput.setStatusTip(
            "Linear correlation estimator."
        )
        self.statsDisplayLayout.addWidget(self.spearmanROutput, currentRow, 1)

        # Display the widget
        self.statsDisplayWidget.setLayout(self.statsDisplayLayout)
        parentWidget.addWidget(self.statsDisplayWidget)

    #------------------------------------------------
    # Generate selection of the parameters to analyse
    def createSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.parameterSelectionWidget = qtw.QWidget()
        self.parameterSelectionLayout = qtw.QGridLayout(self.parameterSelectionWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Parameter(s) Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.parameterSelectionLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Parameter selection
        currentRow += 1
        self.contrastSelection = qtw.QCheckBox("Contrast")
        self.contrastSelection.setChecked(True)
        self.contrastSelection.toggled.connect(lambda: self.updateCheckBoxes(self.contrastSelection))
        self.contrastSelection.setStatusTip(
            "Analyse the contrasts."
        )
        self.amplitudeSelection = qtw.QCheckBox("Amplitude")
        self.amplitudeSelection.toggled.connect(lambda: self.updateCheckBoxes(self.amplitudeSelection))
        self.amplitudeSelection.setStatusTip(
            "Analyse the fit amplitudes."
        )
        self.parameterSelectionLayout.addWidget(self.contrastSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.amplitudeSelection, currentRow, 1)

        currentRow += 1
        self.noiseSelection = qtw.QCheckBox("Noise")
        self.noiseSelection.toggled.connect(lambda: self.updateCheckBoxes(self.noiseSelection))
        self.noiseSelection.setStatusTip(
            "Analyse the noises."
        )
        self.centerSelection = qtw.QCheckBox("Center")
        self.centerSelection.toggled.connect(lambda: self.updateCheckBoxes(self.centerSelection))
        self.centerSelection.setStatusTip(
            "Analyse the centers."
        )
        self.parameterSelectionLayout.addWidget(self.noiseSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.centerSelection, currentRow, 1)

        currentRow += 1
        self.snrSelection = qtw.QCheckBox("SNR")
        self.snrSelection.toggled.connect(lambda: self.updateCheckBoxes(self.snrSelection))
        self.snrSelection.setStatusTip(
            "Analyse the signal-to-noise ratios."
        )
        self.widthSelection = qtw.QCheckBox("Width")
        self.widthSelection.toggled.connect(lambda: self.updateCheckBoxes(self.widthSelection))
        self.widthSelection.setStatusTip(
            "Analyse the widths."
        )
        self.parameterSelectionLayout.addWidget(self.snrSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.widthSelection, currentRow, 1)

        currentRow += 1
        self.frameSelection = qtw.QCheckBox("Frame")
        self.frameSelection.toggled.connect(lambda: self.updateCheckBoxes(self.frameSelection))
        self.frameSelection.setStatusTip(
            "Analyse the frame numbers."
        )
        self.offsetSelection = qtw.QCheckBox("Offset")
        self.offsetSelection.toggled.connect(lambda: self.updateCheckBoxes(self.offsetSelection))
        self.offsetSelection.setStatusTip(
            "Analyse the offsets."
        )
        self.parameterSelectionLayout.addWidget(self.frameSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.offsetSelection, currentRow, 1)

        currentRow += 1
        self.positionSelection = qtw.QCheckBox("Distance from a reference point (X,Y)")
        self.positionSelection.toggled.connect(lambda: self.updateCheckBoxes(self.positionSelection))
        self.positionSelection.setStatusTip(
            "Analyse the distance to a reference point."
        )
        self.parameterSelectionLayout.addWidget(self.positionSelection, currentRow, 0, 1, -1)

        # Center input
        currentRow += 1
        tabIndex = self.parent.centralWidget.currentIndex()
        self.xCenterInput = qtw.QLineEdit()
        self.xCenterInput.setText( str(self.parent.imageTabsImage[tabIndex].currentArray.shape[0]/2) )
        self.xCenterInput.setStatusTip(
            "X coordinates of the reference point."
        )
        self.yCenterInput = qtw.QLineEdit()
        self.yCenterInput.setText( str(self.parent.imageTabsImage[tabIndex].currentArray.shape[1]/2) )
        self.yCenterInput.setStatusTip(
            "Y coordinates of the reference point."
        )
        self.parameterSelectionLayout.addWidget(self.xCenterInput, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.yCenterInput, currentRow, 1)

        currentRow += 1
        self.errorSelection = qtw.QCheckBox("Compare the errors on the parameters")
        self.errorSelection.toggled.connect(self.plotAnalysis)
        self.errorSelection.setStatusTip(
            "Use the errors instead of the values when available."
        )
        self.parameterSelectionLayout.addWidget(self.errorSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.parameterSelectionWidget.setLayout(self.parameterSelectionLayout)
        parentWidget.addWidget(self.parameterSelectionWidget)

    #------------------------------------------------
    # Generate selection of the parameters to analyse
    def createActionButtons(self, parentWidget):

        # Generate the widget
        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QGridLayout(self.buttonWidget)

        # Buttons
        currentRow = 0
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.setStatusTip(
            "Save the result(s) of the analysis."
        )
        self.buttonLayout.addWidget(self.saveButton, currentRow, 0)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip(
            "Close the window."
        )
        self.buttonLayout.addWidget(self.closeButton, currentRow, 1)

        # Save all options
        currentRow += 1
        self.saveAllSelection = qtw.QCheckBox("Save all statistics")
        self.saveAllSelection.setStatusTip(
            "Save all possible statistics."
        )
        self.buttonLayout.addWidget(self.saveAllSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)

    ##-\-\-\-\-\-\-\
    ## DATA HANDLING
    ##-/-/-/-/-/-/-/

    #----------------------------------------------------
    # Extract the data and convert them into a dictionary
    def extractData(self, allData):

        # Store the data
        self.dataObject = allData
        self.dataArray = np.array( [data.getData() for data in allData] )
        self.keys = ['contrast','noise','snr','amplitude','center','width','offset','frame','distance']

        # Extract the data from each profiles
        self.dataDict = {
        'frame': np.array( [data.frame for data in allData] ).astype(float),
        'contrast': np.copy( self.dataArray[:,1] ).astype(float),
        'contrastErr': np.copy( self.dataArray[:,2] ).astype(float),
        'noise': np.copy( self.dataArray[:,3] ).astype(float),
        'noiseErr': np.copy( self.dataArray[:,4] ).astype(float),
        'snr': np.copy( self.dataArray[:,5] ).astype(float),
        'snrErr': np.copy( self.dataArray[:,6] ).astype(float),
        'x': np.copy( self.dataArray[:,7] ).astype(float),
        'y': np.copy( self.dataArray[:,8] ).astype(float),
        'amplitude': np.copy( self.dataArray[:,12] ).astype(float),
        'amplitudeErr': np.copy( self.dataArray[:,13] ).astype(float),
        'center': np.copy( self.dataArray[:,14] ).astype(float),
        'centerErr': np.copy( self.dataArray[:,15] ).astype(float),
        'width': np.copy( self.dataArray[:,16] ).astype(float),
        'widthErr': np.copy( self.dataArray[:,17] ).astype(float),
        'offset': np.copy( self.dataArray[:,18] ).astype(float),
        'offsetErr': np.copy( self.dataArray[:,19] ).astype(float)
        }

    ##-\-\-\-\-\-\-\-\
    ## PLOT THE RESULTS
    ##-/-/-/-/-/-/-/-/

    #--------------------------------
    # Plot the analysis on the window
    def plotDistribution(self, valueName):

        # Get the data
        if valueName != 'distance':
            currentValue = self.dataDict[valueName]
        else:
            currentValue = self.getDistance()

        # Update the graph
        self.statsAxis.clear()
        sns.distplot(currentValue, ax=self.statsAxis)
        self.statsCanvas.draw()

        # Edit the entries
        self.meanOutput.setText( str(round(np.mean(currentValue),3)) )
        self.stdOutput.setText( str(round(np.std(currentValue, ddof=1),3)) )
        self.spearmanROutput.setText('---')

    def plotCorrelation(self, valueNames):

        # Get the data
        if valueNames[0] != 'distance':
            currentY = self.dataDict[valueNames[0]]
        else:
            currentY = self.getDistance()

        if valueNames[1] != 'distance':
            currentX = self.dataDict[valueNames[1]]
        else:
            currentX = self.getDistance()

        # Update the graph
        self.statsAxis.clear()
        sns.regplot(x=currentX, y=currentY, ax=self.statsAxis)
        self.statsCanvas.draw()

        # Edit the entries
        self.meanOutput.setText('---')
        self.stdOutput.setText('---')
        self.spearmanROutput.setText( str(round(np.corrcoef(currentX, currentY, ddof=1)[0,1],3)) )

    def plotAnalysis(self):

        # Check the selected checkbox
        rawSelection = self.getBoxChecked()

        # Check if errors exist for the given values
        currentSelection = []
        if self.errorSelection.isChecked():
            for element in rawSelection:
                if element + 'Err' in list(self.dataDict.keys()):
                    currentSelection.append( element + 'Err' )
                else:
                    currentSelection.append( element )
        else:
            currentSelection = rawSelection

        # Update the displayed informations
        if len(currentSelection) == 1:
            self.plotDistribution(currentSelection[0])
        else:
            self.plotCorrelation(currentSelection)

    #----------------------
    # Manage the checkboxes
    def updateCheckBoxes(self, checkbox):

        # Check the number of box currently checked
        numberSelection = len(self.getBoxChecked())
        if numberSelection > 2:
            checkbox.setChecked(False)
        elif  numberSelection < 1:
            checkbox.setChecked(True)
        else:
            self.plotAnalysis()

    def getBoxChecked(self):

        nameList = np.array(self.keys)
        checkBoxState = np.array([
        self.contrastSelection.isChecked(),
        self.noiseSelection.isChecked(),
        self.snrSelection.isChecked(),
        self.amplitudeSelection.isChecked(),
        self.centerSelection.isChecked(),
        self.widthSelection.isChecked(),
        self.offsetSelection.isChecked(),
        self.frameSelection.isChecked(),
        self.positionSelection.isChecked()
        ])
        currentSelection = nameList[checkBoxState == True]

        return currentSelection

    #---------------------
    # Compute the distance
    def getDistance(self):

        # Extract the position of the reference point
        xRef = float(self.xCenterInput.text())
        yRef = float(self.yCenterInput.text())

        # Calculate the distance
        xValues = self.dataDict['x']
        yValues = self.dataDict['y']
        distances = np.sqrt((xValues - xRef)**2 + (yValues - yRef)**2)

        return distances

    ##-\-\-\-\-\-\-\-\
    ## SAVE THE RESULTS
    ##-/-/-/-/-/-/-/-/

    #----------------------------------------
    # Save the current distribution in a file
    def saveCurrentDistribution(self, valueName):

        # Get the data
        if valueName != 'distance':
            currentValue = self.dataDict[valueName]
        else:
            currentValue = self.getDistance()

        saveStats(self.parent, currentValue, valueName, 1)

    #----------------------------------------------
    # Save the current linear correlation in a file
    def saveCurrentCorrelation(self, valueNames):

        # Get the data
        if valueNames[0] != 'distance':
            currentY = self.dataDict[valueNames[0]]
        else:
            currentY = self.getDistance()

        if valueNames[1] != 'distance':
            currentX = self.dataDict[valueNames[1]]
        else:
            currentX = self.getDistance()
        parameterNames = valueNames[1]+','+valueNames[0]
        currentValue = np.array([currentX, currentY])

        saveStats(self.parent, currentValue, parameterNames, 2)

    #--------------------------------------------
    # Save all the possible stats on the profiles
    def saveAllStats(self):

        # Prepare the distance
        dictToSave = self.dataDict
        dictToSave['distance'] = self.getDistance()

        # Remove the unwanted parameters
        del dictToSave['x']
        del dictToSave['y']

        # Save the file
        saveAllStats(self.parent, dictToSave)

    #------------------------
    # Select the type of save
    def saveData(self):

        # Save all the data possible
        if self.saveAllSelection.isChecked():
            self.saveAllStats()

        # Save the displayed distribution or linear correlation
        else:

            # Check the selected checkbox
            rawSelection = self.getBoxChecked()

            # Check if errors exist for the given values
            currentSelection = []
            if self.errorSelection.isChecked():
                for element in rawSelection:
                    if element + 'Err' in list(self.dataDict.keys()):
                        currentSelection.append( element + 'Err' )
                    else:
                        currentSelection.append( element )
            else:
                currentSelection = rawSelection

            # Update the displayed informations
            if len(currentSelection) == 1:
                self.saveCurrentDistribution(currentSelection[0])
            else:
                self.saveCurrentCorrelation(currentSelection)
