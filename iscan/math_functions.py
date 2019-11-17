import numpy as np
from scipy.optimize import curve_fit

##-\-\-\-\-\-\-\
## FIT FUNCTIONS
##-/-/-/-/-/-/-/

#---------------------------
# Sinc function for a 1D fit
def sinc(x, A, w, c, y0):

    # Correct the width of the sinc
    w *= 2 / np.pi

    return A * np.sinc((x-c)/w) + y0

#----------------------------
# Gauss function for a 1D fit
def gauss(x, A, w, c, y0):

    # Correct the width of the gaussian
    w *= np.sqrt(2*np.log10(2)) / 2

    return A * np.exp(-(x-c)**2/(2*w**2)) + y0

#----------------------------
# Gauss function for a 2D fit
def gauss2D(xy, amplitude, xc, yc, sigma_x, sigma_y, theta, offset):

    x, y = xy

    xo = float(xc)
    yo = float(yc)

    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)

    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))

    return g.ravel()

#----------------
# 2D Gaussian fit
def gaussian2DFit(imageArray):

    # Create x and y indices
    x = np.arange(0, imageArray.shape[0])
    y = np.arange(0, imageArray.shape[1])
    x, y = np.meshgrid(x, y)

    # Iniitalise the parameters
    a = np.amax(imageArray)
    xc = imageArray.shape[0]/2
    yc = imageArray.shape[1]/2
    sx = 5
    sy = 5
    theta = 1
    y0 = 1

    # Fit the data
    popt, pcov = curve_fit(gauss2D, (x, y), imageArray.ravel(), p0=[a, xc, yc, sx, sy, theta, y0])

    return popt, np.sqrt(np.diag(pcov))

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMAGE GENERATION-RELATED CALCULATIONS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

#-----------------------------------------------------------------------
# Calculate the position of the circle and adjust the radius if required
def _circleCalculation(position, radius, positionMax, positionMin=(0,0)):

    # Extract the position
    row, column = position

    # Get the limits (1)
    a,b = limitCalculation(row, radius, positionMax[0], positionMin=positionMin[0])
    c,d = limitCalculation(column, radius, positionMax[1], positionMin=positionMin[1])

    # Get the radii
    ra = row - a
    rb = b - row
    rc = column - c
    rd = d - column
    trueRadius = np.amin([ra,rb,rc,rd])

    # Get the limits (2)
    a,b = limitCalculation(row, trueRadius, positionMax[0], positionMin=positionMin[0])
    c,d = limitCalculation(column, trueRadius, positionMax[1], positionMin=positionMin[1])

    return a,c, 2*trueRadius, 2*trueRadius

#-----------------------------------------------------------------------
# Calculate the position of the circle and adjust the length if required
def _lineCalculation(position, length, angle, positionMax, positionMin=(0,0)):

    # Extract the position
    row, column = position

    # Calculate the coordinates of the first point
    a = row - np.sin(angle*np.pi/180)*length
    b = column - np.cos(angle*np.pi/180)*length

    # Calculate the coordinates of the second point
    c = row + np.sin(angle*np.pi/180)*length
    d = column + np.cos(angle*np.pi/180)*length

    return a,b,c,d

#----------------------------
# Adjust the limits of a line
def _lineAdjustment(p1, p2, positionMax, positionMin=(0,0)):

    # Get the parameters of the line
    if p2[0] - p1[0] != 0:
        a = (p2[1] - p1[1])/(p2[0] - p1[0])
        b = p1[1] - p1[0]*a

        # Adjust the position of the 1st point
        if p1[0] < positionMin[0]:
            p1 = ( 0 , b )
        if p1[1] < positionMin[1]:
            p1 = ( -b/a , 0 )
        if p1[0] > positionMax[0]:
            p1 = ( positionMax[0], a*positionMax[0]+b )
        if p1[1] > positionMax[1]:
            p1 = ( (positionMax[1]-b)/a , positionMax[1] )

        # Adjust the position of the 2nd point
        if p2[0] < positionMin[0]:
            p2 = ( 0 , b )
        if p2[1] < positionMin[1]:
            p2 = ( -b/a , 0 )
        if p2[0] > positionMax[0]:
            p2 = ( positionMax[0], a*positionMax[0]+b )
        if p2[1] > positionMax[1]:
            p2 = ( (positionMax[1]-b)/a , positionMax[1] )

    # Exception: case of a vertical line
    else:
        # Adjust the position of the 1st point
        if p1[1] < positionMin[1]:
            p1 = ( p1[0] , 0 )
        if p1[1] > positionMax[1]:
            p1 = ( p1[0] , positionMax[1] )

        # Adjust the position of the 2nd point
        if p2[1] < positionMin[1]:
            p2 = ( p2[0] , 0 )
        if p2[1] > positionMax[1]:
            p2 = ( p2[0] , positionMax[1] )

    return p1, p2

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

#------------------------------------------------------
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

#----------------------------------------------------------
# Calculate the position of the line and adjust if required
def circleAndLineComputation(position, length, angle, positionMax, positionMin=(0,0), radius=30):

    # Get the position
    x,y = position

    # Get the limit of the circle
    circleLimits = _circleCalculation(position, radius, positionMax)

    # Get the position of the line
    aL,bL,cL,dL = _lineCalculation(position, length/2, angle, positionMax)
    p1, p2 = _lineAdjustment((aL, bL), (cL, dL), positionMax)
    aL, bL = p1
    cL, dL = p2
    lineLimits = (aL, bL, cL, dL)

    return circleLimits, lineLimits, p1, p2

#-------------------------------------------------
# Initialise the parameters for the different fits
def initialiseParameters(x, y):

    # Offset calculation
    scanLim = int(y.shape[0] / 8)
    offset = np.mean(np.array([y[0:scanLim],y[-scanLim::]]))

    # Amplitude calculation
    amplitude = np.amax(y[3*scanLim:5*scanLim]) - offset

    # Center calculation
    center = x[3*scanLim:5*scanLim][np.argmax(y[3*scanLim:5*scanLim])]

    # Width calculation
    halfMax = (amplitude / 2) + offset
    halfedArray = y[4*scanLim::] - halfMax
    width = x[4*scanLim::][np.argmin(halfedArray)] - center

    return [amplitude, width, center, offset]

#--------------------------------------------------
# Return the fitted profile based on the parameters
def fitProfile(x, y, parameters, fitType='sinc'):

    # List of the functions
    fitFunctions = {
    'sinc': sinc,
    'gauss': gauss,
    }

    # Fit the data
    popt, pcov = curve_fit(fitFunctions[fitType], x, y, p0=parameters)

    return popt, np.sqrt(np.diag(pcov))

#--------------------------------------------------
# Return the fitted profile based on the parameters
def fittedProfile(x, parameters, fitType='sinc'):

    # List of the functions
    fitFunctions = {
    'sinc': sinc,
    'gauss': gauss,
    }

    return fitFunctions[fitType](x, *parameters)

#--------------------------------------------------
# Compute the contrast, noise and snr of the signal
def computeSNR(signal, fittedSignal, parameters, parameterErrors, widthFactor=3):

    # Extract the profiles and values
    distance, profile = signal
    fitDistance, fitProfile = fittedSignal
    A, w, c, y0 = parameters
    aErr, wErr, cErr, yErr = parameterErrors

    # Compute the contrast
    contrast = (np.amax(fitProfile) - y0) * 100 / y0
    contrastErr = (aErr * 100 / y0) + (yErr * (np.amax(fitProfile) - y0) * 100/ (y0**2))

    if c-w*widthFactor > distance[0]:

        # Compute the noise
        baseProfile = profile - fitProfile
        noiseProfile = baseProfile[(distance < (c-w*widthFactor))|(distance > (c+w*widthFactor))]
        noise = np.std(noiseProfile, ddof=1) * 100 / y0
        noiseErr = (yErr * np.std(noiseProfile, ddof=1) * 100/ (y0**2))

        # Compute the SNR
        snr = (np.amax(fitProfile) - y0) / np.std(noiseProfile, ddof=1)
        snrErr = (contrastErr / noise) + (noiseErr * contrast / (noise**2))

    else:
        noise = 0
        noiseErr = 0
        snr = 0
        snrErr = 0

    return [contrast, noise, snr], [contrastErr, noiseErr, snrErr]
