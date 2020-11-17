import json
import os

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# --------------------------------------
# Check that the extension is authorized
def _check_extensions(file, extensions=[".json"]):

    file_name, file_extension = os.path.splitext(file)

    # Save in the new list on if the extension is authorized
    if file_extension in extensions:
        return file

    # Raise an error if not valid
    else:
        raise Exception("The extension is not valid.")

# ------------------------------------------
# Return the list of attributes of the class
def _get_attribute_list():
    return [
        "diameter",
        "minmass",
        "maxsize",
        "separation",
        "noise_size",
        "smoothing_size",
        "threshold",
        "invert",
        "percentile",
        "topn",
        "preprocess",
        "max_iterations",
        "characterize",
        "engine",
        "search_range",
        "memory",
        "adaptive_stop",
        "adaptive_step",
        "neighbor_strategy",
        "link_strategy",
        "filter_stubs",
    ]

# -------------------------------------------------
# Convert settings in class instance to a dictonary
def _settings2dict(setting_object):

    # Retrieve the list of settings to save
    setting_list = _get_attribute_list()

    # Save all the settings in a dictionnary
    setting_dict = {}
    for setting in setting_list:
        setting_dict[setting] = getattr(setting_object, setting)

    return setting_dict

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------
# Save the settings in a JSON file
def saveSettings(settings, name):

    # Retrieve the informations from the dictionnary
    setting_dict = _settings2dict(settings)

    # Set the file name
    name = _check_extensions(name)

    # Save the dictionnary in a file
    with open(name, "w") as fp:
        json.dump(setting_dict, fp)

# ----------------------------------
# Load the settings from a JSON file
def loadSettings(name):

    # Check the file
    name = _check_extensions(name)

    # Retrieve the dictonary
    with open(name, "r") as fp:
        data = json.load(fp)

    return data
