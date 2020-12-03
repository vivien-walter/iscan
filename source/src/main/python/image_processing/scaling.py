##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------------------------
# Convert the space scale (px/unit) in micron per pixel
def getSpaceScale(space_scale, space_unit):

    # Remove eventual plural
    if space_unit[-1] == 's':
        space_unit = space_unit[:-1]

    # Check the input
    if space_unit.lower() in ['micron', 'µm', 'micrometer', 'micrometre']:
        space_unit = 'micrometer'

    if space_unit.lower() in ['nm', 'nanometer', 'nanometre']:
        space_unit = 'nanometer'

    if space_unit.lower() in ['mm', 'millimeter', 'millimetre']:
        space_unit = 'millimeter'

    if space_unit.lower() in ['cm', 'centimeter', 'centimetre']:
        space_unit = 'centimeter'

    # Get the scake dictionary
    unit_conversion = {
    'micrometer':1,
    'nanometer':0.001,
    'millimeter':1000,
    'centimeter':10000
    }
    factor = unit_conversion[ space_unit.lower() ]

    # Convert the value
    micron_per_pixel = 1 / (space_scale * factor)

    return micron_per_pixel
