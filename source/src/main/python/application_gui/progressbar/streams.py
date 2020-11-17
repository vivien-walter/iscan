import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\
## STREAM FROM TERMINAL
##-/-/-/-/-/-/-/-/-/-/

# ---------------------------
# Class to stream the console
class Stream(qtc.QObject):

    newText = qtc.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
