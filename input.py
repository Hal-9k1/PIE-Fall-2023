import util

class Input:
    __slots__ = "drive", "turn"
    def __init__(self, drive_left, drive_right, turn):
        self.drive = util.LRStruct(left = drive_left, right = drive_right)
        self.turn = turn

class TankInputGenerator:
    """Controls chassis motion with two joysticks.

    The "left" and "right" components of the drive (whose interpretation depends on the chassis)
    are controlled by the left and right joysticks.
    """
    __slots__ = "_gamepad_tolerance"
    def __init__(self, gamepad_tolerance):
        self._gamepad_tolerance = gamepad_tolerance

    def generate_keyboard(self):
        return Input(
            drive_left = ((1 if Keyboard.get_value("w") else 0)
                - (1 if Keyboard.get_value("s") else 0)),
            drive_right = ((1 if Keyboard.get_value("up_arrow") else 0)
                - (1 if Keyboard.get_value("down_arrow") else 0)),
            turn = 0
        )
    def generate_gamepad(self):
        drive_left = Gamepad.get_value("joystick_left_y")
        if drive_left < self._gamepad_tolerance:
            drive_left = 0
        drive_right = Gamepad.get_value("joystick_left_y")
        if drive_right < self._gamepad_tolerance:
            drive_right = 0
        return Input(
            drive_left = drive_left,
            drive_right = drive_right,
            turn = 0
        )

class WeirdInputGenerator:
    """Controls chassis motion with one joystick.

    Driving and turning are both controlled by the left joystick, leaving the other joystick
    free for... something.
    """
    def generate_keyboard(self):
        drive = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        )
    def generate_gamepad(self):
        drive = Gamepad.get_value("joystick_left_y")
        if drive < self._gamepad_tolerance:
            drive = 0
        turn = Gamepad.get_value("joystick_left_x")
        if turn < self._gamepad_tolerance:
            turn = 0
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = turn
        )
