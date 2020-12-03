import bottleneck as bn
import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# --------------------
# Do a block averaging
def _block_average(image_array, window, include_partial=False, quiet=False):

    # Get the number of frames
    n_frames = image_array.shape[0]
    n_blocks = n_frames // window
    n_blocks_txt = n_blocks

    # Prepare partials
    if include_partial and n_frames % n_blocks != 0:
        n_blocks_txt += 1

    # Process all blocks
    new_array = []
    for i in range(n_blocks):
        if not quiet:
            print(str(i+1)+'/'+str(n_blocks_txt))

        # Get the limits
        frame0 = i * window
        frame1 = (i+1) * window

        # Make the selection
        crt_avg = image_array[frame0:frame1]

        # Do the average
        crt_avg = bn.nanmean(crt_avg, axis=0)

        new_array.append(crt_avg)

    # Append partials
    if include_partial and n_frames % n_blocks != 0:
        if not quiet:
            print(str(i+2)+'/'+str(n_blocks_txt))
        crt_avg = image_array[frame1:]
        new_array.append(crt_avg)

    # Make the array
    new_array = np.array(new_array)

    return new_array

# --------------------
# Do a running average
def _running_average(image_array, window, include_partial=False, quiet=False):

    # Get the number of frames
    n_frames = image_array.shape[0]
    n_blocks = n_frames - (window-1)
    n_blocks_txt = n_blocks

    # Check for partial data
    if include_partial:
        n_blocks_txt = n_frames

    # Process all blocks
    new_array = []
    for i in range(n_blocks):
        if not quiet:
            print(str(i+1)+'/'+str(n_blocks_txt))

        # Make the selection
        crt_avg = image_array[i:i+window]

        # Do the average
        crt_avg = bn.nanmean(crt_avg, axis=0)

        new_array.append(crt_avg)

    # Append partials
    if include_partial:
        for j in range(n_blocks_txt-n_blocks):
            if not quiet:
                print(str(i+j+2)+'/'+str(n_blocks_txt))

            # Make the selection
            crt_avg = image_array[j+i+1:]

            # Do the average
            crt_avg = bn.nanmean(crt_avg, axis=0)

            new_array.append(crt_avg)

    # Make the array
    new_array = np.array(new_array)

    return new_array

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------
# Average the image stack
def averageStack(image_array, window, average_type='block', include_partial=False, quiet=False):

    # Do the block averaging
    if average_type == 'block':
        new_array = _block_average(image_array, window, include_partial=include_partial, quiet=quiet)

    # Do the running average
    elif average_type == 'running':
        new_array = _running_average(image_array, window, include_partial=include_partial, quiet=quiet)

    return new_array
