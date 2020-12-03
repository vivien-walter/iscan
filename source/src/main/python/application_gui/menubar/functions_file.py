from functools import partial
import os
from pathlib import Path

import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

from application_gui.image_open.display import openImageWindow
from application_gui.messageboxes.display import errorMessageNoImage, errorMessage, errorMessageNoStack
from application_gui.messageboxes.rangeselection import rangeSelectionWindow
from application_gui.progressbar.image_open import OpenImageProgressBarWindow
from application_gui.progressbar.correction_background import ImageCorrectionProgressBarWindow
from application_gui.image_save_single.display import saveSingleImageWindow
from application_gui.image_save_stack.display import saveImageStackWindow
#from application_gui.image_save_video.display import saveVideoWindow

from image_processing.corrections import backgroundCorrection, intensityCorrection
from image_processing.image_class import ImageCollection
from input_output.image_management import getImagesInfos, loadImages
from settings.recent_files_settings import listRecentFiles, appendRecentFiles, deleteRecentFiles

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarFileFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## GENERATE DISPLAY
    ##-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Generate the list of recent files
    def generateOpenRecentList(self):

        # Clear the menu
        self.fileMenu.openRecentSubMenu.clear()

        # Get the list of files recently opened
        list_files = listRecentFiles()

        # Populate the table
        for item in list_files:

            recentFileAction = qtw.QAction(str(item), self.parent)
            recentFileAction.triggered.connect( partial(self.callOpenRecentFile, path=item) )
            self.fileMenu.openRecentSubMenu.addAction(recentFileAction)

    ##-\-\-\-\-\
    ## FILE MENU
    ##-/-/-/-/-/

    # -----------------------------
    # Display the open image window
    def callOpenImageWindow(self):

        # Autoload the image with recommendations
        if self.parent.config.autoload_images:

            # Load a single image
            if self.parent.config.single_images:
                imageFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Open Image(s)...", "","Image Files (*.tif;*.tiff;*.png;*.bmp;*.gif);;All Files (*)")
            else:
                imageFile = qtw.QFileDialog.getExistingDirectory(self.parent, "Open Image(s)...")

            if imageFile:

                # Get the name of the file
                _, _image_name = os.path.split(imageFile)

                # Get the recommandations
                image_recommendations = getImagesInfos(imageFile)
                _do_crop = image_recommendations['do_crop'] and self.parent.config.crop_image
                _crop_size = self.parent.config.crop_size
                _do_sign_correction = image_recommendations['do_sign_correction'] and self.parent.config.correct_signed
                _open_range = None
                _wait_range = False

                # Open the progress bar window
                openWindow(self.parent, OpenImageProgressBarWindow, 'progress_bar', image_path=imageFile, name=_image_name, crop=_do_crop, crop_size=_crop_size, correct_sign=_do_sign_correction, scheduler=self)

                # Add the path to the recent file list
                appendRecentFiles(imageFile)

        # Load the advanced config window
        else:
            openWindow(self.parent, openImageWindow, 'open_image')

    # -----------------------------
    # Proceed with the opened image
    def imageStackOpened(self):

        # Open the new tab
        self.parent.imageTabDisplay.newTab(self.image_class)

        # Process the background correction if needed
        if self.parent.config.auto_background and self.image_class.n_frames > 1:

            # Open the progress window
            openWindow(self.parent, ImageCorrectionProgressBarWindow, 'progress_bar')

            # Get the settings in memory
            do_median = self.parent.config.background_type == 'Median'
            do_division = self.parent.config.correction_type == 'Division'
            do_intensity_correction = self.parent.config.correct_intensity
            replace_tab = not self.parent.config.correct_newtab

            # Apply the background correction
            corrected_array = backgroundCorrection(self.image_class.image.source, median=do_median, divide=do_division)

            # Apply the intensity fluctuation correction - if required
            if do_intensity_correction:
                _intensity_correction_type = self.parent.config.intensity_correction_type.lower()
                corrected_array = intensityCorrection(corrected_array, correction=_intensity_correction_type)

            # Load the array in a file
            new_class = ImageCollection(corrected_array, name=self.image_class.name.strip()+' (Corrected)', space_scale=self.parent.space_scale, space_unit=self.parent.space_unit, frame_rate=self.parent.frame_rate)

            # Update the current tab
            if replace_tab:
                # Get the current tab
                tab_id = self.parent.imageTabDisplay.currentIndex()

                # Update the tab
                new_class.name = self.image_class.name
                self.parent.imageTabDisplay.replaceTab(tab_id, new_class)

            # Create a new tab
            else:
                self.parent.imageTabDisplay.newTab(new_class)

            # Close the progress window
            self.parent.subWindows['progress_bar'].close()
            self.parent.application.processEvents()

    # ------------------------------
    # Open the selected recent files
    def callOpenRecentFile(self, path=None):

        # Check if the file/dir exist
        if os.path.isdir(path) or os.path.isfile(path):

            # Get the name of the file
            _, _image_name = os.path.split(path)

            # Get the recommandations
            image_recommendations = getImagesInfos(path)
            _do_crop = image_recommendations['do_crop'] and self.parent.config.crop_image
            _crop_size = self.parent.config.crop_size
            _do_sign_correction = image_recommendations['do_sign_correction'] and self.parent.config.correct_signed
            _open_range = None
            _wait_range = False

            # Open the progress bar window
            openWindow(self.parent, OpenImageProgressBarWindow, 'progress_bar', image_path=path, name=_image_name, crop=_do_crop, crop_size=_crop_size, correct_sign=_do_sign_correction, scheduler=self)

            # Add the path to the recent file list
            appendRecentFiles(path)

        # Raise an error if the file doesn't exist anymore
        else:
            errorMessage("No Selection","The selected file or folder doesn't exist.")

            # Remove the file from the list
            deleteRecentFiles(path)

    # ---------------------
    # Close the current tab
    def callCloseCurrentTab(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Close the current tab
            self.parent.imageTabDisplay.closeTab(tab_id)

        else:
            errorMessageNoImage()

    # -----------------------
    # Close all the open tabs
    def callCloseAllTabs(self):

        # Get the number of tabs opened
        n_tabs = len( self.parent.imageTabDisplay.displayedTabs )

        # Check if a tab is open
        if n_tabs > 0:

            # Close all the tabs
            for tab_id in range(n_tabs-1, -1, -1):
                self.parent.imageTabDisplay.closeTab(tab_id)

        else:
            errorMessageNoImage()

    # ------------------------------------
    # Save the frame(s) of the current tab
    def callSaveSingleFrame(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Open the save window
            openWindow(self.parent, saveSingleImageWindow, 'save_frame', image_class=crt_class)

        else:
            errorMessageNoImage()

    # ---------------------------------------------
    # Save the frames of the current tab as a stack
    def callSaveStack(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                openWindow(self.parent, saveImageStackWindow, 'save_frame', image_class=crt_class)

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()

    # ---------------------------------------------
    # Save the frames of the current tab as a video
    def callSaveVideo(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                #openWindow(self.parent, saveVideoWindow, 'save_frame', image_class=crt_class)
                pass

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()
