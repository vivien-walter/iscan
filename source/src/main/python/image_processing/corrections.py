import bottleneck as bn
import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -------------------------------------------------------
# Rescale the image intensity to apply the given contrast
def _rescale_contrast(image_array, minPV, maxPV, displayedMaxPV):

    # Turn to float
    image_array = image_array.astype(float)

    # Crop the values
    image_array[image_array < minPV] = minPV
    image_array[image_array > maxPV] = maxPV

    # Shift to 0
    image_array = image_array - minPV

    # Rescale the maximal value
    maxPV -= minPV
    image_array = image_array * displayedMaxPV / maxPV

    return image_array

# ------------------------------------------
# Generate the static background of an image
def _generate_background(image_array, median=True):

    # Compute the median image
    if median:
        reference_array = bn.nanmedian(image_array, axis=0)

    # Compute the mean image
    else:
        reference_array = bn.nanmean(image_array, axis=0)

    return reference_array

# ---------------------------------
# Compute the background correction
def _do_correction(image_array, reference_array, divide=True):

    # Compute the division
    if divide:
        corrected_array = image_array / reference_array

    # Compute the subtraction
    else:
        corrected_array = image_array - reference_array

    return corrected_array

# -----------------------------------
# Retrieve the intensity fluctuations
def _get_fluctuations(image_array, correction='median'):

    # Calculate the mean PV for each image
    if correction == 'mean':
        mean_values = bn.nanmean( bn.nanmean(image_array, axis=1), axis=1)
    elif correction == 'median':
        mean_values = bn.nanmedian( bn.nanmedian(image_array, axis=1), axis=1)

    return mean_values

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------------
# Apply a background correction on the given stack
def backgroundCorrection(image_array, median=True, divide=True):

    # Create the background
    background_array = _generate_background(image_array, median=median)

    # Do the correction
    corrected_array = _do_correction(image_array, background_array, divide=divide)

    return corrected_array

# ----------------------------------
# Rescale the intensity of the image
def contrastCorrection(image_array, max_value, limits=None):

    # Retrieve the values
    if limits is None:
        minPV, maxPV = np.amin(image_array), np.amax(image_array)
    else:
        minPV, maxPV = limits

    # Rescale the contrast of the image
    contrast_array = _rescale_contrast(image_array, minPV, maxPV, 256)

    # Adjust the intensity for display
    contrast_array = contrast_array * max_value

    return contrast_array

# -------------------------------
# Correct signed bits-based image
def correctSignedBits(image_array):

    # Get the bitness
    if np.amax(image_array) > 256:
        _bitvalue = 65536
    else:
        _bitvalue = 256

    # Correct the signed bits
    _bit_zero = _bitvalue / 2
    image_array = image_array - _bit_zero

    return image_array

# --------------------------------------------
# Correct the intensity fluctuations over time
def intensityCorrection(image_array, correction='median'):

    # Calculate the mean PV for each image
    mean_values = _get_fluctuations(image_array, correction=correction)

    # Correct the pixel values
    image_array = image_array / mean_values[:, np.newaxis, np.newaxis]

    return image_array

# ------------------------------------
# Calculate the mean PV for each image
def getFluctuations(image_array):
    return _get_fluctuations(image_array)

# --------------------------------------------------------------------------------------
# Subtract background and compute the absolute value to convert dark particles to bright
def convertDark2Bright(image_array, median=True):

    # Get the background
    corrected_array = backgroundCorrection(image_array, median=median, divide=False)

    # Compute the absolute value
    corrected_array = abs(corrected_array)

    return corrected_array
