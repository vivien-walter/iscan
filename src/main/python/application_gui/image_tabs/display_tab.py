import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.image_tabs.functions_image import imageDisplayFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## TAB DISPLAY FOR THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageDisplayTab( imageDisplayFunctions ):
    def __init__(self, parent, image_class):

        # Initialise the parameters
        self.parent = parent
        self.image_class = image_class

        # Widget content
        self.tabWidget = qtw.QWidget()
        self.tabLayout = qtw.QVBoxLayout()

        # Add the custom display options
        self.createStackDisplay(self.tabLayout)

        # Load the layout
        self.tabWidget.setLayout(self.tabLayout)

        # Generate the array the first time
        self.displayImage()

        # Install a listener if needed
        if not self.parent.imageTabDisplay.event_filter_on:
            self.parent.imageTabDisplay.tabBar().installEventFilter(self.parent.imageTabDisplay)
            self.parent.imageTabDisplay.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
            self.parent.imageTabDisplay.event_filter_on = True

        # Update the display if first tab open
        if not self.parent.image_on:
            self.parent.updateAnimationAction()
            self.image_on = True

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Create the display for the image stack
    def createStackDisplay(self, parentWidget):

        # Define the scrollable widget
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setMinimumWidth(512)
        self.scrollArea.setMinimumHeight(512)

        # Define the image label
        self.scrollAreaImage = qtw.QLabel(self.scrollArea)
        self.scrollAreaImage.setScaledContents(True)
        self.scrollAreaImage.mousePressEvent = self.actionOnClick
        self.scrollArea.setWidget(self.scrollAreaImage)

        # Display the widget
        parentWidget.addWidget(self.scrollArea)
