import bottleneck as bn
import numpy as np

##-\-\-\-\-\-\-\-\-\-\
## PROFILE CALCULATIONS
##-/-/-/-/-/-/-/-/-/-/

# --------------------------------------------------
# Compute the contrast, noise and snr of the signal
def computeSNR(signal, fittedSignal, parameters, parameterErrors, widthFactor=3, brightSpot=True):

    # Extract the profiles and values
    distance, profile = signal
    fitDistance, fitProfile = fittedSignal
    A, w, c, y0 = parameters
    aErr, wErr, cErr, yErr = parameterErrors

    # Compute the contrast
    if brightSpot:
        contrast = (np.amax(fitProfile) - y0) * 100 / y0
        contrastErr = (aErr * 100 / y0) + (
            yErr * (np.amax(fitProfile) - y0) * 100 / (y0 ** 2)
        )
    else:
        contrast = (np.amin(fitProfile) - y0) * 100 / y0
        contrastErr = (aErr * 100 / y0) + (
            yErr * (np.amin(fitProfile) - y0) * 100 / (y0 ** 2)
        )

    if c - w * widthFactor > distance[0]:

        # Compute the noise
        baseProfile = profile - fitProfile
        noiseProfile = baseProfile[
            (distance < (c - w * widthFactor)) | (distance > (c + w * widthFactor))
        ]
        noise = bn.nanstd(noiseProfile, ddof=1) * 100 / y0
        noiseErr = yErr * bn.nanstd(noiseProfile, ddof=1) * 100 / (y0 ** 2)

        # Compute the SNR
        if brightSpot:
            snr = (np.amax(fitProfile) - y0) / bn.nanstd(noiseProfile, ddof=1)
        else:
            snr = (np.amin(fitProfile) - y0) / bn.nanstd(noiseProfile, ddof=1)
        snrErr = (contrastErr / noise) + (noiseErr * contrast / (noise ** 2))

    else:
        noise = 0
        noiseErr = 0
        snr = 0
        snrErr = 0

    return [contrast, noise, snr], [contrastErr, noiseErr, snrErr]

##-\-\-\-\-\-\-\-\-\
## PROFILE STATISTICS
##-/-/-/-/-/-/-/-/-/

# -------------------------------------------------------
# Save the stats on the given distribution or correlation
def saveStats(parent, dataArray, parameterNames, numberColumns):

    # Prepare the data to save
    fileText = ""

    if numberColumns == 2:
        dataArray = np.copy(dataArray).T

        # Initialise the header
        valueNames = parameterNames.split(",")
        fileText += (
            "Mean " + valueNames[0] + ":" + str(bn.nanmean(dataArray[:, 0])) + "\n"
        )
        fileText += (
            "StDev " + valueNames[0] + ":" + str(bn.nanstd(dataArray[:, 0], ddof=1)) + "\n"
        )
        fileText += (
            "Mean " + valueNames[1] + ":" + str(bn.nanmean(dataArray[:, 1])) + "\n"
        )
        fileText += (
            "StDev " + valueNames[1] + ":" + str(bn.nanstd(dataArray[:, 1], ddof=1)) + "\n"
        )

        # Get the linear correlation estimator
        fileText += (
            "Spearman's Rho:"
            + str(np.corrcoef(dataArray[:, 0], dataArray[:, 1], ddof=1))
            + "\n"
        )

    # Initialise the header for a single distribution
    else:
        fileText += "Mean:" + str(bn.nanmean(dataArray)) + "\n"
        fileText += "StDev:" + str(bn.nanstd(dataArray, ddof=1)) + "\n"

    # File the rest of the file
    fileText += parameterNames + '\n'
    for row in dataArray:

        # Add the values
        if isinstance(row, list):
            fileText += str(row[0]) + ',' + str(row[1]) + '\n'
        else:
            fileText += str(row) +'\n'

    saveTextFile(parent, fileText)

# -----------------------------------------------
# Save all the possible stats on the given array
def allStats(parent, dataDict):

    # Generate the data array
    parameters = list(dataDict.keys())
    dataArray = []
    for param in parameters:
        currentArray = [
            param,
            str(bn.nanmean(dataDict[param])),
            str(bn.nanstd(dataDict[param], ddof=1)),
        ]
        for param2 in parameters:
            currentArray.append(
                str(np.corrcoef(dataDict[param], dataDict[param2], ddof=1)[0, 1])
            )
        dataArray.append(np.copy(np.array(currentArray)))

    # Create the file
    columnNames = ['Parameter','Mean','StDev']
    for param in parameters:
        columnNames.append( param )

    saveDataFile( parent, np.array(dataArray), name_array= np.array(columnNames) )

##-\-\-\-\-\-\-\
## SAVE PROFILES
##-/-/-/-/-/-/-/

# ------------------------------------
# Save all the profiles in a .csv file
def saveTable( parent, profiles ):

    # Retrieve all the values
    allValues = []
    for profile in profiles:
        allValues.append( profile.getTableValues() )
    allValues = np.array(allValues)

    # Prepare the header
    # NOTE: Take this from profiling_control.py
    columnNames = [
        "Name",
        "Contrast",
        "ContrastErr",
        "Noise",
        "NoiseErr",
        "SNR",
        "SNRErr",
        "Frame",
        "X",
        "Y",
        "Angle",
        "Length",
        "Fit",
        "Amplitude",
        "AErr",
        "Center",
        "CErr",
        "Width",
        "WErr",
        "Offset",
        "OErr",
    ]

    saveDataFile( parent, allValues, name_array= np.array(columnNames) )

# ------------------------------------
# Save the profile plot in a .csv file
def saveProfile(parent, profile, fileName):

    # Generate the value array
    plotValue = np.array([ profile.distance , profile.profile, profile.profile_fit ]).T

    # Prepare the header
    columnNames = ['Distance','Profile','Fit']

    saveDataFile( parent, plotValue, file_name=fileName, name_array= np.array(columnNames), confirm_message=False )

##-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS TO HANDLE PROFILES
##-/-/-/-/-/-/-/-/-/-/-/-/

class profile:
    def __init__ (self, frame, line, circle):

        self.name = "none"

        # Time information
        self.frame = frame

        # Elements of the profile
        self.position = None
        self.angle = None
        self.length = None
        self.line = line
        self.circle = circle
        self.colour = 'black'

        # Initialize the intensity profile
        self.profile = None
        self.distance = None

        # Initialize the fitted profile
        self.profile_fit = None

        # Initialize the fit parameters
        self.fit_type = None
        self.fit_parameters = None
        self.fit_errors = None
        self.amplitude = None
        self.width = None
        self.center = None
        self.offset = None

        # Initialize the image properties
        self.contrast = {}
        self.noise = {}
        self.snr = {}

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## ACCESSING THE VALUES FOR THE FIT
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------
    # Store the fit parameters and errors
    def addFitParameters( self, parameters, errors ):

        # Save the whole parameters and errors
        self.fit_parameters = parameters
        self.fit_errors = errors

        # Save the parameters and errors individually
        self.amplitude = { 'value':parameters[0], 'error':errors[0] }
        self.width = { 'value':parameters[1], 'error':errors[1] }
        self.center = { 'value':parameters[2], 'error':errors[2] }
        self.offset = { 'value':parameters[3], 'error':errors[3] }

    # --------------------------------
    # Extract the values for the table
    def getTableValues(self):

        # Generate the data list
        dataList = [
            self.name,
            self.contrast['value'],
            self.contrast['error'],
            self.noise['value'],
            self.noise['error'],
            self.snr['value'],
            self.snr['error'],
            self.frame,
            self.position[0],
            self.position[1],
            self.angle,
            self.length,
            self.fit_type,
            self.amplitude['value'],
            self.amplitude['error'],
            self.center['value'],
            self.center['error'],
            self.width['value'],
            self.width['error'],
            self.offset['value'],
            self.offset['error'],
        ]

        return dataList

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.input_output.data_files import saveDataFile, saveTextFile
