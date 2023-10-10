# config.py: a generated file holding externally set program configuration.
# Configuration is exposed through functions because some may return mocks,
# which will be created on the spot.

import inputmapping
import components
import mockrobot

def get_input_mapping_class():
    return inputmapping.KeyboardOmniDrive
def get_drive_component_class():
    return components.AngledOmniDrive
def create_robot():
    return Robot
def create_input_source():
    return Keyboard
def create_autonomous_queue():
    return []
