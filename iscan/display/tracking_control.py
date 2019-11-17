import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class trackingControlPanel:#(qtw.QDockWidget):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent

        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Warning)

        msg.setText("ERROR: Function(s) unavailable")
        msg.setInformativeText("""The tracking function(s) has not been implemented yet.
Please check if a more recent version of this software has been released.""")
        msg.setWindowTitle("ERROR")
        msg.setStandardButtons(qtw.QMessageBox.Ok)

        retval = msg.exec_()
