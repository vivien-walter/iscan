from glob import glob
import numpy as np
import os
from PIL import Image, ImageSequence
import re
from skimage import io

from image_processing.image_class import ImageCollection

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------------
# Make recommendations on how to process the image
def _make_recommendations(image_infos):

    # Should the image been cropped?
    crop = image_infos['size'][0] > 1000 # 1000 is an arbitrary value

    # Set the bitness
    if image_infos['max_pv'] > 256:
        _bitvalue = 65536
    else:
        _bitvalue = 256

    # Is the image signed?
    correct_sign = image_infos['min_pv'] > _bitvalue/2

    return crop, correct_sign

# ----------------------------------------------------
# Check that the extensions in the list are authorized
def _check_img_extensions(list, extensions=['.tif','.png','.bmp','.gif','.jpg']):

    new_list = []

    # Process all the items of the list
    for file in list:
        file_name, file_extension = os.path.splitext(file)

        # Save in the new list on if the extension is authorized
        if file_extension in extensions:
            new_list.append(file)

    # Check that the new list is not empty
    return new_list

# ------------------------------
# Open all the files in a folder
def _open_folder(path, open_range=None):

    # Grab all the files in the folder
    file_in_folder = glob( os.path.join(path, '*.*') )

    # Check that the files in the folder can be opened
    file_in_folder = _check_img_extensions(file_in_folder)

    # Sort the files by number in names
    file_in_folder.sort(key=lambda f: int(re.sub('\D', '', f)))
    n_images = len(file_in_folder)

    # Get the range for opening images
    if open_range is None:
        begin, end = 0, n_images
    else:
        begin, end = open_range
        n_images = end - begin

    # Open all the images
    imageArray = []
    for i, frame_id in enumerate(range(begin, end)):
        print( str(i)+'/'+str(n_images) )

        # Get the file
        f = file_in_folder[frame_id]
        imageArray.append(np.asarray( Image.open(f) ))

    return np.array(imageArray)

# ----------------------
# Open the selected file
def _open_file(path):

    # Load the image(s)
    sequence = Image.open(path)

    # Deal with stacks (.tif) and animations (.gif)
    if 'n_frames' in dir(sequence):

        # Extract all frames
        stack = []
        for i, frame in enumerate( ImageSequence.Iterator(sequence) ):
            print( str(i)+'/'+str(sequence.n_frames) )
            stack.append( np.copy(np.array(frame)) )

        imageArray = np.array(stack)

    # Convert simple image type
    else:
        imageArray = np.array(sequence)

        # Format the shape of all image arrays
        imageArray = np.reshape( imageArray, (1, *imageArray.shape) )

    return imageArray

# -------------------------------------------
# Load an image stack from a file or a folder
def _open_image(path, open_range=None):

    # Check if it is a folder
    if os.path.isdir(path):
        imageArray = _open_folder(path, open_range=open_range)

    # Check if it is a file
    elif os.path.isfile(path):
        imageArray = _open_file(path)

    return imageArray

# ------------------------------
# Rescale the value in the array
def _rescale_array(array, old_limits, new_limits):

    # Save the data type
    data_type = array.dtype
    array = array.astype(np.float64)

    # Get the limits
    old_min, old_max = old_limits
    new_min, new_max = new_limits

    # Rescale to 0 - 1
    unit_array = (array - old_min) / (old_max - old_min)
    unit_array[unit_array < 0] == 0
    unit_array[unit_array > 1] == 1

    # Rescale to the new limits
    new_array = unit_array * (new_max - new_min) + new_min

    return new_array.astype(data_type)

# ------------------------------------
# Convert the image type and bit depth
def _convert_bit_depth(array, bit_depth=8, rescale=True):

    # Convert the array type
    array = array.astype(np.uint16)

    # Get the parameters for the conversion
    data_types = {8:np.uint8, 16:np.uint16}
    data_type = data_types[bit_depth]

    new_limits = (0, 2**bit_depth - 1)

    # Check for rescale of old min value
    if rescale:
        old_min = np.amin(array)
    else:
        old_min = 0

    # Check for rescale of old max value
    if array.dtype in [data_types[d] for d in list(data_types.keys())] and not rescale:
        old_max = np.iinfo(array.dtype).max

    else:
        old_max = np.amax(array)

    old_limits = (old_min, old_max)
    new_array = _rescale_array(array, old_limits, new_limits)

    return new_array.astype(data_type)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------------
# Get the image information from the array
def getArrayInfos(image_array):

    # Build the information dictionary
    image_infos = {
    'number': image_array.shape[0],
    'size': image_array.shape[1:],
    'min_pv': np.amin(image_array),
    'max_pv': np.amax(image_array)
    }

    # Make recommandations
    _crop, _correct_sign = _make_recommendations(image_infos)

    # Append the information
    image_infos['do_crop'] = _crop
    image_infos['do_sign_correction'] = _correct_sign

    return image_infos

# -------------------------
# Get the image information
def getImagesInfos(file_path):

    # Process a folder
    if not os.path.isfile(file_path):

        # Get the first file of the folder
        for image_ext in ['.tif','.tiff','.png','.bmp','.gif']:
            test_image = glob( os.path.join(file_path,'*'+image_ext) )
            if len(test_image) != 0:
                file_path = test_image[0]
                n_images = len(test_image)
                break

    # Process a single image
    else:
        n_images = 1

    # Open the test image
    test_array = _open_image(file_path)

    # Build the information dictionary
    image_infos = {
    'number': n_images,
    'size': test_array.shape[1:],
    'min_pv': np.amin(test_array),
    'max_pv': np.amax(test_array)
    }

    # Make recommandations
    _crop, _correct_sign = _make_recommendations(image_infos)

    # Append the information
    image_infos['do_crop'] = _crop
    image_infos['do_sign_correction'] = _correct_sign

    return image_infos

# ---------------
# Load the images
def loadImages(file_path, name='Untitled', open_range=None, crop=False, crop_size=152, correct_sign=False, space_scale=44.9, space_unit="micron", frame_rate=150):

    # Open the image array
    image_array = _open_image(file_path, open_range=open_range)

    # Load the array in the class
    image_instance = ImageCollection(image_array, name=name, crop=crop, crop_size=crop_size, correct_sign=correct_sign, space_scale=space_scale, space_unit=space_unit, frame_rate=frame_rate)
    return image_instance

# ----------------------
# Save an image or stack
def saveImage(array, path, bit_depth=8, rescale=True):

    # Convert the type
    array = _convert_bit_depth(array, bit_depth=bit_depth, rescale=rescale)

    # Save all frames
    if array.shape[0] > 0:

        # Get the base name and extension
        basename, extension = os.path.splitext(path)

        for i in range(array.shape[0]):

            # Get the name
            name = basename + '_' + str(i) + extension

            # Save the file
            io.imsave(name, array[i])

    # Save a single frame
    else:
        io.imsave(path, array)
