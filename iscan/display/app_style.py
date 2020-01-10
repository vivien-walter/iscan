import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

# --------------------------
# Apply the style to the GUI
def applyStyle( app ):

    # Select the style to use
    app.setStyle("Fusion")

    # Generate the colour palette
    palette = qtg.QPalette() # Get a copy of the standard palette.

    # Define colours
    background = qtg.QColor(40, 50, 60)
    button = qtg.QColor(55, 80, 95)
    light_background = qtg.QColor(30, 35, 45)
    links = qtg.QColor(42, 130, 218)
    highlight = qtg.QColor(60, 123, 150)

    palette.setColor(qtg.QPalette.Window, background)
    palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Base, light_background)
    palette.setColor(qtg.QPalette.AlternateBase, background)
    palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.white)
    palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Text, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Button, button)
    palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
    palette.setColor(qtg.QPalette.Link, links)
    palette.setColor(qtg.QPalette.Highlight, highlight)
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)

    # Set the palette
    app.setPalette(palette)

    # Additional CSS styling for tooltip elements.
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
