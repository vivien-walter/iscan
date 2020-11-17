import numpy as np
from scipy.optimize import curve_fit

##-\-\-\-\-\-\-\-\
## MATHS FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------
# Gaussian function
def gauss(x, A, x0, w, y0):
    return A * np.exp(-((x - x0) ** 2) / w ** 2) + y0

##-\-\-\-\-\-\-\-\
## PRIVATE FUNCTION
##-/-/-/-/-/-/-/-/

# ------------------------------------------------
# Initialise the fit parameters for a Gaussian fit
def _init_gaussian_fit(y):

    # Get the backgroud level
    y0Init = np.mean(y[0:int(y.shape[0]/5)])

    # Get the type of signal
    x0Init = y.shape[0]/2
    aInit = y[int(x0Init)]

    # Get the width
    wInit = 20 # /!\ Arbitrary value

    return aInit, x0Init, wInit, y0Init

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Fit the data with a gaussian function
def fitGaussian(y):

    # Initialise the parameters
    init_parameters = _init_gaussian_fit(y)

    # Make the range
    x_fit = np.arange(0, y.shape[0], 1)

    # Fit the profile
    params, pcov = curve_fit(gauss, x_fit, y, p0=init_parameters)

    # Calculate the errors
    perr = np.sqrt(np.diag(pcov))

    return params, perr
