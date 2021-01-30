import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui._custom.rangeslider import QRangeSlider

##-\-\-\-\-\-\-\-\-\-\-\
## CALL WINDOW FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/-/

# -------------------------------------
# Check if the window is already opened
def _is_window_open(parent, window_tag):

    # Initialise if it does not exist
    if window_tag not in parent.subWindows.keys():
        parent.subWindows[window_tag] = None

    return parent.subWindows[window_tag] is None

# ---------------
# Open the window
def openWindow(parent, window_class, window_tag, **kwargs):

    # Stop any ongoing animation
    if parent.animation_on:
        parent.toggleAnimation(stop=True)

    # Check if the window is not open yet
    if _is_window_open(parent, window_tag):
        parent.subWindows[window_tag] = window_class(parent, **kwargs)

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## WIDGET & LAYOUT MANAGEMENT
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Remove all the content in a layout
def emptyLayout(layout):

    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)

# -----------------------------------------------------
# Update the value of a widget without releasing signal
def updateValue(widget, new_value):

    # Block the signals
    widget.blockSignals(True)

    # Edit the values
    widget.setValue(new_value)

    # Release the signals
    widget.blockSignals(False)

##-\-\-\-\-\-\-\
## COMMON WIDGETS
##-/-/-/-/-/-/-/

# ---------------------
# Generate label widget
def CLabel(text):

    widgetName = qtw.QLabel(text)
    widgetNameFont = qtg.QFont()
    widgetNameFont.setBold(True)
    widgetName.setFont(widgetNameFont)

    return widgetName

# ----------------------------------------------------
# Generate a QLineEdit widget with a label on the side
def CLabelledLineEdit(label, left_side=True, bold=True):

    # User name entry
    fullWidget = qtw.QWidget()
    fullLayout = qtw.QHBoxLayout( fullWidget )

    # Make the label
    if bold:
        widgetLabel = CLabel(label)
    else:
        widgetLabel = qtw.QLabel(label)

    # Add the label on the left
    if left_side:
        fullLayout.addWidget(widgetLabel)

    # Add the QLineEdit widget
    lineEditWidget = qtw.QLineEdit()
    fullLayout.addWidget(lineEditWidget)

    # Add the label on the right
    if not left_side:
        fullLayout.addWidget(widgetLabel)

    fullWidget.setLayout(fullLayout)
    fullWidget.setContentsMargins(0, 0, 0, 0)
    return fullWidget, lineEditWidget

# -------------------------------------------------------------------------------
# Generate a QLineEdit and a QButton (with a QLabel if requested) to browse files
class CBrowse(qtw.QWidget):
    def __init__(self, label=None, bold=True, read_only=True):
        super(CBrowse, self).__init__()

        # User name entry
        self.layout = qtw.QHBoxLayout( self )

        # Add the label on the left
        if label is not None:
            if bold:
                self.label = CLabel(label)
            else:
                self.label = QLabel(label)
            self.layout.addWidget(self.label)

        # Add the QLineEdit widget
        self.lineEdit = qtw.QLineEdit()
        self.layout.addWidget(self.lineEdit)

        if read_only:
            self.lineEdit.setReadOnly(True)

        # Add the browse button
        self.pushButton = qtw.QPushButton('Browse')
        self.pushButton.setFixedWidth(100)
        self.layout.addWidget(self.pushButton)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## ACCESS THE LINEEDIT WIDGET
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Get the text from the Line Edit widget
    def text(self):
        return self.lineEdit.text()

    # ------------------------------------
    # Edit the text in the LineEdit widget
    def setText(self, new_text):
        self.lineEdit.setText(new_text)

    ##-\-\-\-\
    ## CONNECT
    ##-/-/-/-/

    # --------------------------------
    # Connect the action to the button
    def connectButton(self, connected_function):
        self.pushButton.clicked.connect(connected_function)

    # ---------------------------------------
    # Connect the entry control to a function
    def connectEntry(self, connected_function):
        self.pushButton.editingFinished.connect(connected_function)

    # ------------------------------------------
    # Connect both controls to the same function
    def connect(self, connected_function):
        self.connectButton(connected_function)
        self.connectEntry(connected_function)

# ---------------------------------------------------------
# Generate the several controls making the animation widget
class CAnimationControl(qtw.QWidget):
    def __init__(self, n_frames=""):
        super(CAnimationControl, self).__init__()

        # User name entry
        self.layout = qtw.QHBoxLayout( self )

        # Add the play button
        self.playButton = qtw.QPushButton("Play")
        self.playButton.setFixedWidth(50)
        self.layout.addWidget(self.playButton)

        # Add the QLineEdit widget
        self.lineEdit = qtw.QLineEdit()
        self.lineEdit.setFixedWidth(50)
        self.layout.addWidget(self.lineEdit)

        # Add the number of frames
        self.frameLabel = CLabel("/"+str(n_frames))
        self.layout.addWidget(self.frameLabel)

        # Add the play button
        self.previousButton = qtw.QPushButton("<")
        self.previousButton.setFixedWidth(25)
        self.layout.addWidget(self.previousButton)

        # Add the play button
        self.nextButton = qtw.QPushButton(">")
        self.nextButton.setFixedWidth(25)
        self.layout.addWidget(self.nextButton)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    ##-\-\-\-\
    ## CONNECT
    ##-/-/-/-/

    # -------------------------------------
    # Connect the action to the play button
    def connectPlay(self, connected_function):
        self.playButton.clicked.connect(connected_function)

    # ---------------------------------------------------
    # Connect the action to the previous and next buttons
    def connectChangeFrames(self, connected_function):
        self.previousButton.clicked.connect(lambda : connected_function(False))
        self.nextButton.clicked.connect(lambda : connected_function(True))

    # ------------------------------------
    # Connect the action to the entry line
    def connectEntry(self, connected_function):
        self.lineEdit.editingFinished.connect(lambda : connected_function(self.lineEdit.text()))

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # ------------------------------------------
    # Toggle the status of the animation control
    def setEnabled(self, status):
        self.playButton.setEnabled(status)
        self.lineEdit.setEnabled(status)
        self.frameLabel.setEnabled(status)
        self.previousButton.setEnabled(status)
        self.nextButton.setEnabled(status)

    # --------------------------------
    # Edit the text of the play button
    def togglePlay(self, status=True):
        if status:
            self.playButton.setText('Stop')
        else:
            self.playButton.setText('Play')

    # -------------------------------------
    # Edit the display of the current frame
    def setCurrentFrame(self, frame_id):
        self.lineEdit.setText(str(frame_id + 1))

    # ----------------------------------------
    # Edit the display of the number of frames
    def setNFrames(self, n_frames):
        self.frameLabel.setText("/" + str(n_frames))

# ------------------------------------------------
# Generate the several controls to select the path
class CPathSelection(qtw.QWidget):
    def __init__(self):
        super(CPathSelection, self).__init__()

        # User name entry
        self.layout = qtw.QHBoxLayout( self )
        self.list = None

        # Add the previous button
        self.previousButton = qtw.QPushButton("<")
        self.previousButton.setFixedWidth(25)
        self.previousButton.setEnabled(False)
        self.previousButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.previousButton)

        # Add the QLineEdit widget
        self.comboBox = qtw.QComboBox()
        self.comboBox.setFixedWidth(75)
        self.layout.addWidget(self.comboBox)

        # Add the next button
        self.nextButton = qtw.QPushButton(">")
        self.nextButton.setFixedWidth(25)
        self.nextButton.setEnabled(False)
        self.nextButton.clicked.connect(self._change_index)
        self.layout.addWidget(self.nextButton)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # ---------------------------------------------------
    # Replace the content of the combobox with a new list
    def replaceList(self, new_list):

        # Clear the content of the combobox
        self.comboBox.clear()

        # Fill the combo box with the content of the list
        self.comboBox.addItems(new_list)
        self.list = new_list

        # Update the controls
        _enough_paths = len(new_list) > 1
        self.previousButton.setEnabled(_enough_paths)
        self.nextButton.setEnabled(_enough_paths)

    # -------------------------------------
    # Change the selection on the combo box
    def _change_index(self, go_back=False):

        # Get the current index
        crt_index = self.comboBox.currentIndex()

        # Get the new index
        if go_back:
            new_index = crt_index - 1
        else:
            new_index = crt_index + 1

        # Coerce the value
        if new_index < 0:
            new_index = len(self.list)-1
        if new_index >= len(self.list):
            new_index = 0

        # Set the new index
        self.comboBox.setCurrentIndex(new_index)

    ##-\-\-\-\
    ## CONNECT
    ##-/-/-/-/

    # -------------------------------------
    # Connect the action to the play button
    def connectChange(self, connected_function):
        self.comboBox.currentIndexChanged.connect(connected_function)

# ---------------
# Range selection
class CRangeSelection(QRangeSlider):
    def __init__(self):
        super(CRangeSelection, self).__init__()

# ---------------
# Navigation tool
class CNavigation(qtw.QWidget):
    def __init__(self):
        super(CNavigation, self).__init__()

        # User name entry
        self.layout = qtw.QGridLayout( self )

        # Add the UP button
        self.upButton = qtw.QPushButton("")
        self.upButton.setIcon( self.style().standardIcon(getattr(qtg.QStyle, 'SP_ArrowUp')) )
        self.upButton.setFixedWidth(25)
        self.upButton.setFixedHeight(25)
        #self.upButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.upButton, 0, 1)

        # Add the LEFT button
        self.leftButton = qtw.QPushButton("")
        self.leftButton.setIcon( self.style().standardIcon(getattr(qtg.QStyle, 'SP_ArrowLeft')) )
        self.leftButton.setFixedWidth(25)
        self.leftButton.setFixedHeight(25)
        #self.leftButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.leftButton, 1, 0)

        # Add the OK button
        self.okButton = qtw.QPushButton("")
        self.okButton.setIcon( self.style().standardIcon(getattr(qtg.QStyle, 'SP_DialogYesButton')) )
        self.okButton.setFixedWidth(25)
        self.okButton.setFixedHeight(25)
        #self.okButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.okButton, 1, 1)

        # Add the RIGHT button
        self.rightButton = qtw.QPushButton("")
        self.rightButton.setIcon( self.style().standardIcon(getattr(qtg.QStyle, 'SP_ArrowRight')) )
        self.rightButton.setFixedWidth(25)
        self.rightButton.setFixedHeight(25)
        #self.leftButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.rightButton, 1, 2)

        # Add the DOWN button
        self.downButton = qtw.QPushButton("")
        self.downButton.setIcon( self.style().standardIcon(getattr(qtg.QStyle, 'SP_ArrowDown')) )
        self.downButton.setFixedWidth(25)
        self.downButton.setFixedHeight(25)
        #self.downButton.clicked.connect(lambda: self._change_index(go_back=True))
        self.layout.addWidget(self.downButton, 2, 1)

        self.setLayout(self.layout)
        self.setFixedWidth(90)
        self.setFixedHeight(90)
        self.setContentsMargins(0, 0, 0, 0)

    ##-\-\-\-\-\-\-\-\-\
    ## CONNECT FUNCTIONS
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Connect the action to the direction buttons
    def connectDirections(self, connected_function):
        self.upButton.clicked.connect(lambda : connected_function((-1,0)))
        self.leftButton.clicked.connect(lambda : connected_function((0,-1)))
        self.rightButton.clicked.connect(lambda : connected_function((0,1)))
        self.downButton.clicked.connect(lambda : connected_function((1,0)))

    # ---------------------------------------
    # Connect the action to the center button
    def connectCenter(self, connected_function):
        self.okButton.clicked.connect(connected_function)

# ---------------------------
# Define the separator widget
def CHorizontalSeparator():
    separator = qtw.QFrame()
    separator.setFrameShape(qtw.QFrame.HLine)
    separator.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
    separator.setLineWidth(1)

    return separator

# ---------------------------
# Define the separator widget
def CVerticalSeparator():
    separator = qtw.QFrame()
    separator.setFrameShape(qtw.QFrame.VLine)
    separator.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
    separator.setLineWidth(1)

    return separator
