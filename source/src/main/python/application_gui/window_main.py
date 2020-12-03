import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.app_styles import applyStyle
from application_gui.common_gui_functions import CHorizontalSeparator
from application_gui.menubar.display import menuBar
from application_gui.image_tabs.main_tab import mainTabWidget
from application_gui.window_main_subscripts.functions import mainGUIFunctions

from settings.user_settings import loadUserConfig
from settings.tracker_settings import initTrackerConfig
from settings.display_track_settings import loadDisplayTrackConfig

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUI(qtw.QMainWindow, mainGUIFunctions):
    def __init__(self, application, application_context=None, compiler='fbs'):
        super(mainGUI, self).__init__()

        # Initialize the properties of the software Main GUI
        self.appctxt = application_context
        self.application = application
        self.compiler = compiler

        self.title = "iSCAN"
        self.version = "v1.1"

        self.subWindows = {}
        self.docks = {
        "tracking":None
        }
        self.image_on = False
        self.show_trajectory = True

        self.animation_on = False
        self.animation_thread = None

        # Load the config
        self.config = loadUserConfig()
        initTrackerConfig()
        self.disptrack_conf = loadDisplayTrackConfig()

        # Set the global scale
        self.space_scale = self.config.space_scale
        self.space_unit = self.config.space_unit
        self.frame_rate = self.config.frame_rate

        # Generate the display
        self.setWindowTitle(self.title + " (" + self.version + ")")
        self.menuBar = menuBar(self)

        # Populate the window
        self.generateCentralWidget()

        # Apply the style
        if self.config.dark_theme:
            applyStyle( self.application )

        # Display the window
        self.statusBar()
        self.show()
        self.setMinimumSize(575,725)

    # --------------------------
    # Initialise the main widget
    def generateCentralWidget(self):

        # Define the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Display the widget
        self.imageTabDisplay = mainTabWidget(self)
        self.mainLayout.addWidget( self.imageTabDisplay )

        self.mainLayout.addWidget( CHorizontalSeparator() )

        # Add action widget at the bottom
        self.generateButtonWidget(self.mainLayout)

        # Display the widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    # -------------------------------------------------------
    # Close all background threads when the application close
    def closeEvent(self, event=None):

        # Cancel the periodic check thread
        if self.animation_on:
            self.animation_thread.stop()

        # Terminate
        event.accept()
        qtw.qApp.quit()

    ##-\-\-\-\-\-\-\-\
    ## GENERATE DISPLAY
    ##-/-/-/-/-/-/-/-/

    # ----------------------------
    # Initialise the button widget
    def generateButtonWidget(self, parentWidget):

        # Generate the widget
        self.controlWidget = qtw.QWidget()
        self.controlLayout = qtw.QVBoxLayout(self.controlWidget)

        # Generate the button sub-widget
        self.buttonsWidget = qtw.QWidget()
        self.buttonsLayout = qtw.QHBoxLayout(self.buttonsWidget)

        # Exit button
        self.exitButton = qtw.QPushButton("Exit")
        self.exitButton.setFixedWidth(125)
        self.exitButton.clicked.connect(self.close)
        self.buttonsLayout.addWidget(self.exitButton, alignment=qtc.Qt.AlignRight)

        # Display the sub-widget
        self.buttonsWidget.setLayout(self.buttonsLayout)
        self.controlLayout.addWidget(self.buttonsWidget)

        # Display the widget
        self.controlWidget.setLayout(self.controlLayout)
        self.controlWidget.setContentsMargins(0, 0, 0, 0)
        parentWidget.addWidget(self.controlWidget)
