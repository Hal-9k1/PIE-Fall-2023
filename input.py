import util

class Input:
    __slots__ = "drive", "turn", "arm_velocity", "hand_status"
    def __init__(self, drive_left, drive_right, turn, arm_velocity, hand_status):
        self.drive = util.LRStruct(left = drive_left, right = drive_right)
        self.turn = turn
        self.arm_velocity = arm_velocity
        self.hand_status = hand_status

class TankInputGenerator:
    """Controls chassis motion with two joysticks.

    The "left" and "right" components of the drive (whose interpretation depends on the chassis)
    are controlled by the left and right joysticks.
    """
    __slots__ = "_gamepad_tolerance", "_hand_open_pressed", "_hand_close_pressed"
    def __init__(self, gamepad_tolerance):
        self._gamepad_tolerance = gamepad_tolerance
        self._hand_open_pressed = False
        self._hand_close_pressed = False

    def generate_keyboard(self):
        return Input( # TODO: add arm velocity and hand status
            drive_left = ((1 if Keyboard.get_value("w") else 0)
                - (1 if Keyboard.get_value("s") else 0)),
            drive_right = ((1 if Keyboard.get_value("up_arrow") else 0)
                - (1 if Keyboard.get_value("down_arrow") else 0)),
            turn = 0
        )
    def generate_gamepad(self):
        drive_left = Gamepad.get_value("joystick_left_y")
        if abs(drive_left) < self._gamepad_tolerance:
            drive_left = 0
        drive_right = Gamepad.get_value("joystick_right_y")
        if abs(drive_right) < self._gamepad_tolerance:
            drive_right = 0
        arm_bias = 0.1
        arm_strength = 0.4
        arm_velocity = ((arm_strength - arm_bias if Gamepad.get_value("r_bumper") else 0)
            - (arm_strength if Gamepad.get_value("r_trigger") else 0)) + arm_bias
        hand_status = ((1 if (Gamepad.get_value("l_bumper") and not self._hand_open_pressed) else 0)
            - (1 if (Gamepad.get_value("l_trigger") and not self._hand_close_pressed) else 0))
        self._hand_open_pressed = Gamepad.get_value("l_bumper")
        self._hand_closed_pressed = Gamepad.get_value("l_trigger")

        return Input(
            drive_left = drive_left,
            drive_right = drive_right,
            turn = 0,
            arm_velocity = arm_velocity,
            hand_status = hand_status
        )

class WeirdInputGenerator:
    """Controls chassis motion with one joystick.

    Driving and turning are both controlled by the left joystick, leaving the other joystick
    free for... something.
    """
    __slots__ = "_gamepad_tolerance"
    def __init__(self, gamepad_tolerance):
        self._gamepad_tolerance = gamepad_tolerance

    def generate_keyboard(self):
        drive = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
        return Input( # TODO: add arm velocity and hand status
            drive_left = drive,
            drive_right = drive,
            turn = (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        )
    def generate_gamepad(self):
        drive = Gamepad.get_value("joystick_left_y")
        if abs(drive) < self._gamepad_tolerance:
            drive = 0
        turn = Gamepad.get_value("joystick_left_x")
        if abs(turn) < self._gamepad_tolerance:
            turn = 0
        return Input( # TODO: add arm velocity and hand status
            drive_left = drive,
            drive_right = drive,
            turn = turn
        )
