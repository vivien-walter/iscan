import numpy as np
from scipy.optimize import curve_fit
import threading

##-\-\-\-\-\-\-\-\-\
## VARIABLE CHECKING
##-/-/-/-/-/-/-/-/-/

# -----------------------------
# Check if the string is an int
def isStringInt(text):

    try:
        value = int(text)
        return True
    except:
        return False

# ------------------------------
# Check if the string is a float
def isStringFloat(text):

    try:
        value = float(text)
        return True
    except:
        return False

##-\-\-\-\-\-\-\-\-\-\
## VARIABLE CONVERTION
##-/-/-/-/-/-/-/-/-/-/

# ------------------------------
# Convert a string to an integer
def string2Int(text, convert=True):

    # Check if the value is an int
    if isStringInt(text):
        return int(text)

    # Check if convertion is true and return if it's a float
    elif convert and isStringFloat(text):
        return round( float(text) )

    # Return false if the convertion failed
    else:
        return False

# ------------------------------
# Convert a string to an integer
def string2Float(text):

    # Check if the value is a float
    if isStringFloat(text):
        return float(text)

    # Return false if the convertion failed
    else:
        return False

##-\-\-\-\-\-\-\-\-\
## VARIABLE COERCING
##-/-/-/-/-/-/-/-/-/

# ----------------
# Coerce the value
def coerceValue(value, max, min=0, max2Zero=False):

    # Coerce if index lower than the minimum value
    if value < min:
        value = min

    # Coerce if index greater than the maximum value
    elif value > max:
        if max2Zero:
            value = min
        else:
            value = max

    return value

# -----------------------
# Calculate the new index
def calculateIndex(index, max, min=0, increment=1, frame=None, max2Zero=False):

    # Calculate the new index
    if frame is None:
        frame = index + increment

    # Coerce the value of the index
    newIndex = coerceValue(frame, max, min=min, max2Zero=max2Zero)

    return newIndex

# -----------------------------------
# Calculate the new value (non index)
def calculateValue(value, max, min=0, factor=1.005, newValue=None, multiplication=True, max2Zero=False):

    # Calculate the new value
    if newValue is None:
        if multiplication:
            newValue = value * factor
        else:
            newValue = value + factor

    # Coerce the value of the index
    newValue = coerceValue(newValue, max, min=min, max2Zero=max2Zero)

    return newValue

# -----------------------------------------------------
# Check that the limit of the area are within the image
def limitCalculation(position, radius, positionMax, positionMin=0):

    # Compute the inferior limit
    limInf = position - radius
    if limInf < positionMin:
        limInf = 0

    # Compute the superior limit
    limSup = position + radius
    if limSup > positionMax:
        limSup = positionMax

    return limInf, limSup

##-\-\-\-\
## GEOMETRY
##-/-/-/-/

# ----------------------------------------------------------------------
# Calculate the position of the circle and adjust the radius if required
def _circleCalculation(position, radius, positionMax, positionMin=(0, 0)):

    # Extract the position
    row, column = position

    # Get the limits (1)
    a, b = limitCalculation(row, radius, positionMax[0], positionMin=positionMin[0])
    c, d = limitCalculation(column, radius, positionMax[1], positionMin=positionMin[1])

    # Get the radii
    ra = row - a
    rb = b - row
    rc = column - c
    rd = d - column
    trueRadius = np.amin([ra, rb, rc, rd])

    # Get the limits (2)
    a, b = limitCalculation(row, trueRadius, positionMax[0], positionMin=positionMin[0])
    c, d = limitCalculation(
        column, trueRadius, positionMax[1], positionMin=positionMin[1]
    )

    return a, c, 2 * trueRadius, 2 * trueRadius


# ----------------------------------------------------------------------
# Calculate the position of the circle and adjust the length if required
def _lineCalculation(position, length, angle, positionMax, positionMin=(0, 0)):

    # Extract the position
    row, column = position

    # Calculate the coordinates of the first point
    a = row - np.sin(angle * np.pi / 180) * length
    b = column - np.cos(angle * np.pi / 180) * length

    # Calculate the coordinates of the second point
    c = row + np.sin(angle * np.pi / 180) * length
    d = column + np.cos(angle * np.pi / 180) * length

    return a, b, c, d


# ---------------------------
# Adjust the limits of a line
def _lineAdjustment(p1, p2, positionMax, positionMin=(0, 0)):

    # Get the parameters of the line
    if p2[0] - p1[0] != 0:
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - p1[0] * a

        # Adjust the position of the 1st point
        if p1[0] < positionMin[0]:
            p1 = (0, b)
        if p1[1] < positionMin[1]:
            p1 = (-b / a, 0)
        if p1[0] > positionMax[0]:
            p1 = (positionMax[0], a * positionMax[0] + b)
        if p1[1] > positionMax[1]:
            p1 = ((positionMax[1] - b) / a, positionMax[1])

        # Adjust the position of the 2nd point
        if p2[0] < positionMin[0]:
            p2 = (0, b)
        if p2[1] < positionMin[1]:
            p2 = (-b / a, 0)
        if p2[0] > positionMax[0]:
            p2 = (positionMax[0], a * positionMax[0] + b)
        if p2[1] > positionMax[1]:
            p2 = ((positionMax[1] - b) / a, positionMax[1])

    # Exception: case of a vertical line
    else:
        # Adjust the position of the 1st point
        if p1[1] < positionMin[1]:
            p1 = (p1[0], 0)
        if p1[1] > positionMax[1]:
            p1 = (p1[0], positionMax[1])

        # Adjust the position of the 2nd point
        if p2[1] < positionMin[1]:
            p2 = (p2[0], 0)
        if p2[1] > positionMax[1]:
            p2 = (p2[0], positionMax[1])

    return p1, p2

# ---------------------------------------------------------
# Calculate the position of the line and adjust if required
def circleAndLineComputation(
    position, length, angle, positionMax, positionMin=(0, 0), radius=30
):

    # Get the position
    x, y = position

    # Get the limit of the circle
    circleLimits = _circleCalculation(position, radius, positionMax)

    # Get the position of the line
    aL, bL, cL, dL = _lineCalculation(position, length / 2, angle, positionMax)
    p1, p2 = _lineAdjustment((aL, bL), (cL, dL), positionMax)
    aL, bL = p1
    cL, dL = p2
    lineLimits = (aL, bL, cL, dL)

    return circleLimits, lineLimits, p1, p2

##-\-\-\-\-\-\-\
## FIT FUNCTIONS
##-/-/-/-/-/-/-/

# --------------------------
# Sinc function for a 1D fit
def sinc(x, A, w, c, y0):

    # Correct the width of the sinc
    w *= 2 / np.pi

    return A * np.sinc((x - c) / w) + y0


# ---------------------------
# Gauss function for a 1D fit
def gauss(x, A, w, c, y0):

    # Correct the width of the gaussian
    w *= np.sqrt(2 * np.log10(2)) / 2

    return A * np.exp(-((x - c) ** 2) / (2 * w ** 2)) + y0

# ---------
# Power law
def powerlaw(x, A, n):

    return A * (x**n)

##-\-\-\-\-\-\-\
## FIT MANAGEMENT
##-/-/-/-/-/-/-/

# ------------------------------------------------
# Initialise the parameters for the different fits
def initializeParameters(x, y, brightSpot=True):

    # Offset calculation
    scanLim = int(y.shape[0] / 8)
    offset = np.mean(np.array([y[0:scanLim], y[-scanLim::]]))

    # Calculation for bright spot
    if brightSpot:

        # Amplitude calculation
        amplitude = np.amax(y[3 * scanLim : 5 * scanLim]) - offset

        # Center calculation
        center = x[3 * scanLim : 5 * scanLim][np.argmax(y[3 * scanLim : 5 * scanLim])]

    else:

        # Amplitude calculation
        amplitude = np.amin(y[3 * scanLim : 5 * scanLim]) - offset

        # Center calculation
        center = x[3 * scanLim : 5 * scanLim][np.argmin(y[3 * scanLim : 5 * scanLim])]

    # Width calculation
    halfMax = (amplitude / 2) + offset
    halfedArray = abs(y[4 * scanLim : :] - halfMax)
    width = x[4 * scanLim : :][np.argmin(halfedArray)] - center

    return [amplitude, width, center, offset]

# -------------------------------------------------
# Return the fitted profile based on the parameters
def fitProfile(x, y, parameters, fitType="sinc"):

    # List of the functions
    fitFunctions = {
        "sinc": sinc,
        "gauss": gauss,
    }

    # Fit the data
    popt, pcov = curve_fit(fitFunctions[fitType], x, y, p0=parameters)

    return popt, np.sqrt(np.diag(pcov))

# -------------------------------------------------
# Return the fitted profile based on the parameters
def fittedProfile(x, parameters, fitType="sinc"):

    # List of the functions
    fitFunctions = {
        "sinc": sinc,
        "gauss": gauss,
    }

    return fitFunctions[fitType](x, *parameters)

# ---------------------------------------------------
# Return the fit parameters of a power law on the MSD
def fitMSD(x, y, yerr=None):

    # Estimate the initial parameters
    A = y[-1] / x[-1]
    n = 1.
    parameters = [A, n]

    # Fit the data
    popt, pcov = curve_fit(powerlaw, x, y, sigma=yerr, p0=parameters)

    return popt, np.sqrt(np.diag(pcov))

##-\-\-\-\-\-\-\-\
## MULTI-THREADING
##-/-/-/-/-/-/-/-/

# ----------------------------------
# Class to create a stoppable thread
class subThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(subThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
