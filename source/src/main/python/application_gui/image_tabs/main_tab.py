import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.image_tabs.functions_tab import mainTabFunctions
from application_gui.image_tabs.display_tab import imageDisplayTab

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## TAB DISPLAY FOR THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class mainTabWidget(qtw.QTabWidget, mainTabFunctions):
    def __init__(self, parent):
        super(mainTabWidget, self).__init__()

        # Initialise the parameters
        self.parent = parent
        self.event_filter_on = False

        # Initialise the tab display
        self.displayedTabs = []

        # Link to the event
        self.currentChanged.connect(self.tabChanged)

    # ------------------------
    # Add a tab to the display
    def newTab(self, image_class):

        # Append the tab to the list
        self.displayedTabs.append( imageDisplayTab(self.parent, image_class) )

        # Append the tab to the widget
        self.addTab( self.displayedTabs[-1].tabWidget, image_class.name )
        self.setCurrentIndex( self.count() - 1 )

    # ------------------------------------------
    # Replace the image array on the current tab
    def replaceTab(self, tab_id, image_class):

        # Get the image class to delete later
        _class_to_delete = self.displayedTabs[tab_id].image_class

        # Upload the new class
        self.displayedTabs[tab_id].image_class = image_class

        # Delete the old class
        del _class_to_delete

        # Refresh the display
        self.displayedTabs[tab_id].displayImage()
