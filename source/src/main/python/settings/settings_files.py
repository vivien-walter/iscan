from appdirs import AppDirs
import os

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------
# Return the default folder of the system
def _return_default_folder():

    # Search the default directory of the system
    default_directory = AppDirs('iSCAN', 'configs', version="1.0")
    default_directory = default_directory.user_data_dir

    return default_directory

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------
# Return the path to the config file
def getConfigPath(file_name='config.ini'):

    # Get the path to the config file
    default_directory = _return_default_folder()
    file_path = os.path.join(default_directory, file_name)

    return file_path
