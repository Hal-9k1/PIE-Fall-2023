import util

class Input:
    __slots__ = "drive", "turn"
    def __init__(self, drive_left, drive_right, turn):
        self.drive = util.LRStruct(left = drive_left, right = drive_right)
        self.turn = turn

class TankInputGenerator:
    def generate_keyboard(self):
        return Input(
            drive_left = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0),
            drive_right = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0),
            turn = 0
        )
    def generate_gamepad(self):
        raise NotImplementedError
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        )
class WeirdInputGenerator:
    def generate_keyboard(self):
        drive = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        )
    def generate_gamepad(self):
        drive = Gamepad.get_value("joystick_left_y")
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = Gamepad.get_value("joystick_left_x")
        )