import numpy as np
from image_processing.modifications import getCropSize, cropImage

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------------------------
# Crop and center the image on the selected particle
def centerCrop(array, trajectory, path_id=0):

    # Retrieve the path
    crt_positions = trajectory.positions
    crt_positions = crt_positions[crt_positions['particle'] == path_id][ ["frame", "y", "x"] ].to_numpy()

    # Get the crop size
    crop_size = getCropSize(crt_positions, array, window_size=9999)

    # Crop all the frames
    cropped_array = []
    for t, y, x in crt_positions:

        # Get the origin
        crt_origin = (int(x - crop_size), int(y - crop_size))

        # Crop the array
        crt_array = cropImage(array, (int(2*crop_size), int(2*crop_size)), origin=crt_origin)
        crt_array = crt_array[ int(t) ]

        cropped_array.append(crt_array)

    # Convert to numpy
    cropped_array = np.array(cropped_array)

    return cropped_array
