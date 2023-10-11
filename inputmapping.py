class OmniDriveInputObject:
    component_support = {
        "drive": ["omni"]
    }
    def __init__(self, axial, lateral, yaw):
        self.axial = axial # move forward
        self.lateral = lateral # move right
        self.yaw = yaw # turn right
class TankDriveInputObject:
    component_support = {
        "drive": ["tank"]
    }
    def __init__(self, left, right):
        self.left = left
        self.right = right

class BaseInputMapping:
    def __init__(self, input_source):
        self._input_source = input_source
    def generate_input(self):
        raise NotImplementedError()
    def get_component_support(self):
        return self._get_input_object_class().component_support

    def _get_input_object_class(self):
        raise NotImplementedError()

class BaseKeyboardInputMapping(BaseInputMapping):
    def _p_bidi_input(negative_key, positive_key, negative_weight=1, positive_weight=1):
        value = positive_weight if self._input_source.get_value(positive_key) else 0
        value -= negative_weight if self._input_source.get_value(negative_key) else 0
        return value

class KeyboardOmniDrive(BaseKeyboardInputMapping):
    input_object_class = OmniDriveInputObject
    def generate_input(self):
        axial = self._p_bidi_input("s", "w")
        lateral = self._p_bidi_input("a", "d")
        yaw = self._p_bidi_input("h", "l")
        return self._get_input_object_class(axial, lateral, yaw)
    def _get_input_object_class(self):
        return OmniDriveInputObject
