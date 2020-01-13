# iSCAN - iSCAT Image Analysis

## Presentation

**Current version**: Beta

**Release date**: 10/02/2020

**iSCAN** is a Python 3-based GUI to analyse the image stacks that have been collected using an iSCAT microscope. Background correction, contrast enhancement and frame averaging tools have been optimised for that type of microscopy.

The software also has the functions to measure the contrast and S:N ratio of typical iSCAT samples and enables quick-and-dirty particle tracking using TrackPy.

The software has been developed by [Vivien WALTER](http://www.vwalter.fr "Vivien Walter's website") in the [Mark I. Wallace group](http://markwallace.org "MIW Group's website") of the King's College London.

## Installation

### Module required

iSCAN requires the following modules to be installed on your computer:
- PyQt5
- NumPy
- SciPy
- Pandas
- Matplotlib
- Seaborn
- PIMS
- Pillow
- Scikit-Images
- TrackPy

### How to install the software

- Download the source files of the repo on your computer

- Unzip the archive file if necessary

## User Manual

### Starting the software

- To start the software from the **Terminal**, open the *iscan/* folder and simply start the *cli.py* script with Python 3
```bash
cd ./path/to/directory/iscan/
python3 cli.py
```
- If you are using **Anaconda**, simply load the *cli.py* script in Spyder and run the execution of the script.

- It is not recommended to start the software using **Jupyter** notebooks.

### Accessing image files and folders

#### - Opening an image stack

To open an image stack, use the **File/Open.../** menu and select wether you want to open an image stack (.tiff ou .gif file) or a folder of individual images; by respectively

Upon starting, you can simply drag & drop the stack or folder on the main window to directly open it.

The function to open image stack has not been implemented yet.

#### - Saving an image stack

To save an image stack or a single frame, use the **File/Save Image** menu.

### Navigating and editing an image stack

#### - Using the Image Control left dock

When an image is opened in the software, the **Image Control** left dock is automatically opened. The dock allows the user to do the following navigation commands:

- **Change the zoom** of the displayed image. The default zoom is automatically set so that the image flls the whole center widget of the software. The value can be changed manually by editing the input field, set to the actual pixel size (100%), or increased/decreased by 5% respectively with the + and - buttons.

- **Navigate through the frames** of the image stack. The frame to be displayed can be changed manually via the input field or the slide bar. It can also be changed using the left and right arrows. The animation can be started using the Play button, and stopped using the Stop button.

The speed of the animation (in FPS) can be changed using the input field. However, the speed is automatically recalculated when the maximum speed that can be achieved by the software is lower than the speed given in the input field. Note also that the speed of the animation is not affecting the time calibration of the stack, used for the diffusitiviy calculations for example.
