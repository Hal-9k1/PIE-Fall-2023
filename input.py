import util

class Input:
    __slots__ = "drive", "turn", "elbow_velocity", "forearm_goal", "forearm_velocity", "hand_status"
    def __init__(self, drive_left, drive_right, turn, elbow_velocity, forearm_goal, forearm_velocity, hand_status):
        self.drive = util.LRStruct(left = drive_left, right = drive_right)
        self.turn = turn
        self.elbow_velocity = elbow_velocity
        self.forearm_goal = forearm_goal
        self.forearm_velocity = forearm_velocity
        self.hand_status = hand_status
    def __str__(self):
        return (f"Input: drive = {{{self.drive.left}, {self.drive.right}}} turn = {self.turn}"
            f" elbow_velocity = {self.elbow_velocity} hand_status = {self.hand_status}")


class BaseInputGenerator:
    __slots__ = "_buttons_pressed", "_debug_logger", "_gamepad_tolerance", "_hand_opened"
    def __init__(self, debug_logger, gamepad_tolerance):
        self._buttons_pressed = set()
        self._debug_logger = debug_logger
        self._gamepad_tolerance = gamepad_tolerance
        self._hand_opened = False
    def generate_keyboard(self):
        raise NotImplementedError()
    def generate_gamepad(self):
        raise NotImplementedError()

    def _calc_gamepad_elbow_velocity(self):
        arm_bias = 0.1
        arm_strength = 0.4
        return ((arm_strength - arm_bias if Gamepad.get_value("r_bumper") else 0)
            - (arm_strength if Gamepad.get_value("r_trigger") else 0)) + arm_bias
    def _test_button_pressed(self, button, use_keyboard):
        if use_keyboard:
            button_down = Keyboard.get_value(button)
        else:
            button_down = Gamepad.get_value(button)
        was_pressed = button_down and not (button in self._buttons_pressed)
        if button_down:
            self._buttons_pressed.add(button)
        elif button in self._buttons_pressed:
            self._buttons_pressed.remove(button)
        return was_pressed
    def _bidirectional_input(self, up_input, down_input, up_input_weight=1, down_input_weight=1):
        return (up_input_weight if up_input else 0) - (down_input_weight if down_input else 0)


class TankInputGenerator(BaseInputGenerator):
    """Controls chassis motion with two joysticks.

    The "left" and "right" components of the drive (whose interpretation depends on the chassis)
    are controlled by the left and right joysticks.
    """
    def __init__(self, debug_logger, gamepad_tolerance):
        super().__init__(debug_logger, gamepad_tolerance)

    def generate_keyboard(self):
        return Input(
            drive_left = self._bidirectional_input(Keyboard.get_value("w"), Keyboard.get_value("s")),
            drive_right = self._bidirectional_input(Keyboard.get_value("up_arrow"),
                Keyboard.get_value("down_arrow")),
            turn = 0,
            # who knows if these keybinds make sense, the peripherals are really meant to be
            # controlled by gamepad...
            elbow_velocity = self._bidirectional_input(Keyboard.get_value("q"), Keyboard.get_value("a")),
            forearm_goal = (0.75 if Keyboard.get_value("p") else
                (0 if Keyboard.get_value("u") else None)),
            forearm_velocity = self._bidirectional_input(Keyboard.get_value("o"), Keyboard.get_value("i")),
            hand_status = self._bidirectional_input(self._test_button_pressed("e", True),
                self._test_button_pressed("d", True))
        )
    def generate_gamepad(self):
        drive_left = Gamepad.get_value("joystick_left_y")
        if abs(drive_left) < self._gamepad_tolerance:
            drive_left = 0
        drive_right = Gamepad.get_value("joystick_right_y")
        if abs(drive_right) < self._gamepad_tolerance:
            drive_right = 0
        if self._test_button_pressed("l_bumper", False):
            self._hand_opened = not self._hand_opened
            hand_status = 1 if self._hand_opened else -1
        else:
            hand_status = 0
        #hand_status = ((1 if self._test_button_pressed("l_bumper", False) else 0)
        #    - (1 if self._test_button_pressed("l_trigger", False) else 0))
        return Input(
            drive_left = drive_left,
            drive_right = drive_right,
            turn = 0,
            elbow_velocity = self._calc_gamepad_elbow_velocity(),
            forearm_goal = None, # TODO: decide on keybinds
            forearm_velocity = self._bidirectional_input(Gamepad.get_value("button_y"),
                 Gamepad.get_value("button_a")),
            hand_status = hand_status
        )

class WeirdInputGenerator(BaseInputGenerator):
    """Controls chassis motion with one joystick.

    Driving and turning are both controlled by the left joystick, leaving the other joystick
    free for... something.
    """
    __slots__ = "_gamepad_tolerance"
    def __init__(self, debug_logger, gamepad_tolerance):
        super().__init__(debug_logger, gamepad_tolerance)

    def generate_keyboard(self):
        drive = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0),
            elbow_velocity = ((1 if Keyboard.get_value("r") else 0)
                - (1 if Keyboard.get_value("f") else 0)),
            forearm_goal = (0.75 if Keyboard.get_value("p") else
                (0 if Keyboard.get_value("u") else None)),
            forearm_velocity = ((1 if Keyboard.get_value("o") else 0)
                - (1 if Keyboard.get_value("i") else 0)),
            hand_status = ((1 if self._test_button_pressed("t", True) else 0)
                - (1 if self._test_button_pressed("g", True) else 0))
        )
    def generate_gamepad(self):
        drive = Gamepad.get_value("joystick_left_y")
        if abs(drive) < self._gamepad_tolerance:
            drive = 0
        turn = Gamepad.get_value("joystick_left_x")
        if abs(turn) < self._gamepad_tolerance:
            turn = 0
        if self._test_button_pressed("l_bumper", False):
            self._hand_opened = not self._hand_opened
            hand_status = 1 if self._hand_opened else -1
        else:
            hand_status = 0
        #hand_status = ((1 if self._test_button_pressed("l_bumper", False) else 0)
        #    - (1 if self._test_button_pressed("l_trigger", False) else 0))
        return Input(
            drive_left = drive,
            drive_right = drive,
            turn = turn,
            elbow_velocity = self._calc_gamepad_elbow_velocity(),
            forearm_goal = None, # TODO: decide on keybinds
            forearm_velocity = self._bidirectional_input(Gamepad.get_value("button_y"),
                 Gamepad.get_value("button_a")),
            hand_status = hand_status
        )
