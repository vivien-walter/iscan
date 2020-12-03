import os

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------
# Create the selected folder
def createFolder(file_path):

    # Create all the directories if needed
    try:
        os.makedirs(os.path.dirname(file_path))

    # Guard against race condition
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
