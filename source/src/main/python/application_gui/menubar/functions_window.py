import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

from application_gui.messageboxes.display import errorMessageNoImage
from application_gui.sidebar_trajectory.display import TrajectoryControlsPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarWindowFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # --------------------------------
    # Open the trajectory manager dock
    def callTrajectoryManagerDock(self):

        # Open the dock
        _open_dock = True
        if "tracking" in self.parent.docks.keys():
            if self.parent.docks["tracking"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["tracking"] = TrajectoryControlsPanel("Trajectory Controller", self.parent)
            self.parent.addDockWidget(qtc.Qt.RightDockWidgetArea, self.parent.docks["tracking"])

            # Set the size and attach the dock
            self.parent.docks["tracking"].setFloating(True)
            self.parent.docks["tracking"].detectLocationChange()
            self.parent.docks["tracking"].setFloating(False)
