import numpy as np

from image_processing.modifications import cropImage, getCropSize
from signal_processing.maths import fitGaussian

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------
# Get line limits
def _line_generation(array_shape, center, angle=0):

    # Extract the position
    y, x = center

    # Normalise the angle
    angle = -1 * (((angle + 90) % 180) - 90)

    # Deal with the vertical case
    if abs(angle) == 90:
        p1, p2 = (0, int(center[1])), (int(array_shape[0] - 1), int(center[1]))

    # Deal with the other angles
    else:

        # Get the angle in radian
        angle = angle * np.pi / 180

        # Left point
        xPLeft = 0
        yPLeft = center[0] + np.tan(angle) * center[1]

        # Recalculate if yPLeft is out of boundary
        if yPLeft < 0 or yPLeft > array_shape[0] - 1:
            if yPLeft < 0:
                yPLeft = 0
            else:
                yPLeft = array_shape[0] - 1
            xPLeft = center[1] - (yPLeft - center[0]) / np.tan(angle)

        # Right point
        xPRight = array_shape[1] - 1
        yPRight = center[0] - np.tan(angle) * (xPRight - center[1])

        # Recalculate if yPRight is out of boundary
        if yPRight < 0 or yPRight > array_shape[0] - 1:
            if yPRight < 0:
                yPRight = 0
            else:
                yPRight = array_shape[0] - 1
            xPRight = center[1] - (yPRight - center[0]) / np.tan(angle)

        p1, p2 = (int(yPLeft), int(xPLeft)), (int(yPRight), int(xPRight))

    return p1, p2

# ---------------------------------
# Plot the profile on a single line
def _compute_line_profile(array, angle=0):

    # Get the center
    center = int(array.shape[1]/2), int(array.shape[2]/2)

    # Get the line position
    pLeft, pRight = _line_generation(array.shape[1:], center, angle=angle)

    # Generate the coordinates
    numberPoints = int(np.hypot(pRight[1] - pLeft[1], pRight[0] - pLeft[0]))
    x, y = (
        np.linspace(pLeft[1], pRight[1], numberPoints),
        np.linspace(pLeft[0], pRight[0], numberPoints),
    )

    # Get the profile
    intensity = array[:,y.astype(np.int), x.astype(np.int)]

    # Generate the radius
    distance = np.sqrt((x - center[1]) ** 2 + (y - center[0]) ** 2) * np.sign(
        x - center[1]
    )

    return intensity, distance

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------------------------
# Process all the profiles to get the properties of the signal
def processProfile(frames, x, y):

    # Initialise the lists
    all_frames = []
    all_contrasts = []
    all_noises = []
    all_SNRs = []

    # Process all the frames
    for t in range(y.shape[0]):

        # Get the line
        crt_profile = y[t]

        # Compute the contrast
        try:
            # Fit the profile
            crt_params, crt_err = fitGaussian(crt_profile)

            # Get the contrast
            crt_contrast = crt_params[0] * 100 /crt_params[3]
            all_contrasts.append(crt_contrast)
            all_frames.append(frames[t])
            _proceed = True

        except:
            _proceed = False

        # Compute the noise and SNR
        if _proceed:
            try:

                # Get the other line
                next_profile = y[t+1]

                # Get the profile difference
                diff_profile = crt_profile - next_profile

                # Get the noise
                crt_noise = np.std(diff_profile, ddof=1) * 100 / crt_params[3]

                # Get the SNR
                crt_snr = abs(crt_contrast / crt_noise)

                # Save the values
                all_noises.append(crt_noise)
                all_SNRs.append(crt_snr)

            except:
                all_noises.append(float('NaN'))
                all_SNRs.append(float('NaN'))

    # Convert into arrays
    all_frames = np.array(all_frames)
    all_contrasts = np.array(all_contrasts)
    all_noises = np.array(all_noises)
    all_SNRs = np.array(all_SNRs)

    return all_frames, all_contrasts, all_noises, all_SNRs

# ------------------------------------------------------------
# Extract the intensity profiles of the particle on each track
def getAllProfiles(positions,array, window_size=50, angle=0):

    # Calculate the limiting positions
    crop_size = getCropSize(positions,array, window_size=window_size)

    # Crop all the frames
    cropped_array = []
    for t, y, x in positions:

        # Get the origin
        crt_origin = (int(x - crop_size), int(y - crop_size))

        # Crop the array
        crt_array = cropImage(array, (int(2*crop_size), int(2*crop_size)), origin=crt_origin)
        crt_array = crt_array[ int(t) ]

        cropped_array.append(crt_array)

    # Convert to numpy
    cropped_array = np.array(cropped_array)

    # Get the line
    frames = positions[:,0].astype(int)
    intensity, distance = _compute_line_profile(cropped_array, angle=angle)

    return frames, intensity, distance

# -----------------------------------------------
# Read the signal information from the trajectory
def readSignals(image_array, trajectory):

    # Get the trajectory
    positions = trajectory.positions
    track_list = np.sort( positions["particle"].unique() )
    n_tracks = len(track_list)

    # Process all particles
    track_profiles = {}
    for i, id in enumerate(track_list):
        print(str(i+1)+'/'+str(n_tracks))

        # Get the positions over time of the current track
        crt_trajectory = positions[positions["particle"] == id][ ["frame", "y", "x"] ].to_numpy()

        # Extract the profiles to process
        crt_frames, crt_intensity, crt_distance = getAllProfiles(crt_trajectory, image_array)

        # Compute the properties
        crt_frames, crt_contrast, crt_noise, crt_snr = processProfile(crt_frames, crt_distance, crt_intensity)

        # Save the values
        crt_profile = {
        'frame':crt_frames,
        'distance': crt_distance,
        'intensity': crt_intensity,
        'contrast': crt_contrast,
        'noise': crt_noise,
        'snr': crt_snr,
        }

        # Save the profile
        track_profiles[id] = crt_profile

    return track_profiles
