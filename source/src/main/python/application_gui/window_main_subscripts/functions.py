from copy import deepcopy

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CAnimationControl
from application_gui.window_main_subscripts.animation import mainGUIAnimation

class mainGUIFunctions:

    ##-\-\-\-\-\-\-\-\
    ## IMAGE ANIMATION
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # Update the main display to add the animation actions
    def updateAnimationAction(self, n_frames=None):

        # Empty the widget
        for i in reversed(range(self.controlLayout.count())):
            self.controlLayout.itemAt(i).widget().setParent(None)

        # Add the slider for animation control
        self.animationSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.animationSlider.setMinimum(0)
        self.animationSlider.sliderReleased.connect(lambda: self.setFrame(self.animationSlider.value(), frame_format=True))
        self.controlLayout.addWidget(self.animationSlider)

        # Generate the button sub-widget
        self.buttonsWidget = qtw.QWidget()
        self.buttonsLayout = qtw.QHBoxLayout(self.buttonsWidget)

        # Insert empty widget to center animation controls
        self.buttonsLayout.addWidget(qtw.QWidget(), alignment=qtc.Qt.AlignLeft)

        # Add the animation control
        self.animationControl = CAnimationControl(n_frames=n_frames)
        self.buttonsLayout.addWidget(self.animationControl, alignment=qtc.Qt.AlignCenter)
        self.animationControl.connectPlay(self.toggleAnimation)
        self.animationControl.connectChangeFrames(self.nextFrame)
        self.animationControl.connectEntry(self.setFrame)

        # Reload the exit button
        self.exitButton = qtw.QPushButton("Exit")
        self.exitButton.setFixedWidth(125)
        self.exitButton.clicked.connect(self.close)
        self.buttonsLayout.addWidget(self.exitButton, alignment=qtc.Qt.AlignRight)

        # Display the sub-widget
        self.buttonsWidget.setLayout(self.buttonsLayout)
        self.controlLayout.addWidget(self.buttonsWidget)

    # --------------------------------------------------
    # Reset the display to remove the animation controls
    def resetActions(self):

        # Empty the widget
        for i in reversed(range(self.controlLayout.count())):
            self.controlLayout.itemAt(i).widget().setParent(None)

        # Generate the button sub-widget
        self.buttonsWidget = qtw.QWidget()
        self.buttonsLayout = qtw.QHBoxLayout(self.buttonsWidget)

        # Reload the exit button
        self.exitButton = qtw.QPushButton("Exit")
        self.exitButton.setFixedWidth(125)
        self.exitButton.clicked.connect(self.close)
        self.buttonsLayout.addWidget(self.exitButton, alignment=qtc.Qt.AlignRight)

        # Display the sub-widget
        self.buttonsWidget.setLayout(self.buttonsLayout)
        self.controlLayout.addWidget(self.buttonsWidget)

    # --------------------------
    # Toggle the stack animation
    def toggleAnimation(self, stop=False):

        # Stop the animation
        if self.animation_on or stop:
            self.animation_thread.stop()

        # Start the animation
        else:
            self.animation_thread = mainGUIAnimation(self)
            self.animation_thread.next_frame.connect(self.nextFrame)

        # Update the GUI
        self.animation_on = not self.animation_on
        self.animationControl.togglePlay(self.animation_on)

    # -------------------------------------------
    # Change the displayed frame by one iteration
    def nextFrame(self, go_forward=True):
        self.imageTabDisplay.changeFrame( go_back=not go_forward )

    # ---------------------------------------------
    # Change the displayed frame to the given value
    def setFrame(self, value, frame_format=False):

        # Correct for the line entry selection
        if not frame_format:
            value = int(value)-1

        # Set the new value
        self.imageTabDisplay.changeFrame( new_frame=value )
