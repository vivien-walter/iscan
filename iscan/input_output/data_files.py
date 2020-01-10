import numpy as np
import xml.etree.ElementTree as ET

import PyQt5.QtWidgets as qtw

##-\-\-\-\-\
## SAVE FILE
##-/-/-/-/-/

# -----------------------------------
# Save the given text in a plain file
def saveTextFile(parent, text, file_name=None, confirm_message=True, extension='.csv'):

    # Get the file name
    proceed, file_name = getFileToCreate(parent, file_name=file_name, extension=extension)
    if not proceed:
        return 0

    try:
        # Save the file
        fileToSave = open(file_name, 'w')
        fileToSave.write(text)
        fileToSave.close()

        # Notify the user
        if confirm_message:
            messageFileSaved()

    # Notify the user if an error occured
    except:
        errorFileSaved()

# ------------------------------
# Save the values in a .csv file
def saveDataFile(parent, value_array, file_name=None, name_array=None, confirm_message=True):

    # Get the file name
    proceed, file_name = getFileToCreate(parent, file_name=file_name, extension='.csv')
    if not proceed:
        return 0

    # Generate the header
    if name_array is None:
        headerText = None
    else:
        headerText = name_array[0]
        for name in name_array[1:]:
            headerText += ',' + name

    try:
        # Save the file
        np.savetxt(file_name, value_array.astype(str), fmt="%s", delimiter=",", header=headerText)

        # Notify the user
        if confirm_message:
            messageFileSaved()

    # Notify the user if an error occured
    except:
        errorFileSaved()

##-\-\-\-\-\-\-\
## XML FORMATTING
##-/-/-/-/-/-/-/

# -----------------------------------
# Convert the array into a XML object
def array2XML(array, element_names, column_names, data_attributes={}, item_attributes={}, z_column=True):

    # Prepare the data and its attributes
    data = ET.Element(element_names[0])
    for attribute in data_attributes.keys():
        data.set(attribute, data_attributes[attribute])

    # Prepare the item and its attributes
    item = ET.SubElement(data, element_names[1])
    for attribute in item_attributes.keys():
        item.set(attribute, item_attributes[attribute])

    # Fill the tree with all the items
    for i in range(array.shape[0]):

        # Generate a temp subitem for the array
        tmp_subitem = ET.SubElement(item, element_names[2])

        # Fill the subitem with the columns in the array
        for j in range(array.shape[1]):
            tmp_subitem.set(column_names[j], str(array[i,j]))

        # Add the z column if missing
        if array.shape[1] == 3 and z_column:
            tmp_subitem.set(column_names[3], "0.0")

    return data, ET.tostring(data)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import messageFileSaved, errorFileSaved
from iscan.input_output.check_files import getFileToCreate
