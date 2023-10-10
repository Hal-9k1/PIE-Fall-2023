_HELPER_module_export_dict = {}
_HELPER_entry_point_line_nums = [18, 25, 30, 38, 44, 52, 60, 70, 74, 81]
class _HELPER_Module:
    def __init__(self, module_name):
        self.__dict__ = _HELPER_module_export_dict[module_name]
    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
def _HELPER_entry_point(func):
    import functools
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('Source traceback (most recent call last):')
            frame_lines = []
            tb = e.__traceback__
            while tb:
                translation_result = _HELPER_translate_line_no(tb.tb_lineno)
                if not translation_result:
                    tb = tb.tb_next
                    continue
                module_name, line_no = translation_result
                frame_lines.append(f'  File "{module_name + ".py"}", line {line_no}, in {tb.tb_frame.f_code.co_name}')
                tb = tb.tb_next
            print('\n'.join(frame_lines))
            print(type(e).__name__ + (': ' if str(e) else '') + str(e))
            exit()
    return wrapped
def _HELPER_translate_line_no(line_no):
    if line_no >= 978:
        skipped_lines = 0
        for entry_point_line_num in _HELPER_entry_point_line_nums:
            if entry_point_line_num + 978 <= line_no:
                skipped_lines += 1
            else:
                break
        return 'main', line_no - 978 - skipped_lines
    elif line_no >= 890:
        return 'path', line_no - 895
    elif line_no >= 849:
        return 'util', line_no - 854
    elif line_no >= 724:
        return 'devices', line_no - 729
    elif line_no >= 417:
        return 'chassis', line_no - 422
    elif line_no >= 259:
        return 'input', line_no - 264
    elif line_no >= 151:
        return 'peripherals', line_no - 156
    elif line_no >= 54:
        return 'mock_robot', line_no - 59
def _HELPER_import_mock_robot():
    if 'mock_robot' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    import time
    
    class MockRobot:
        __slots__ = "_debug_logger", "_devices", "_max_devices", "_device_types", "_device_counts"
        _default_device_properties = {
            "koalabear": {
                "velocity_a": 0.0,
                "deadband_a": 0.05,
                "invert_a": False,
                "pid_enabled_a": True,
                "pid_kp_a": 0.05,
                "pid_ki_a": 0.035,
                "pid_kd_a": 0.0,
                "enc_a": 0,
                "velocity_b": 0.0,
                "deadband_b": 0.05,
                "invert_b": False,
                "pid_enabled_b": True,
                "pid_kp_b": 0.05,
                "pid_ki_b": 0.035,
                "pid_kd_b": 0.0,
                "enc_b": 0
            },
            "servocontroller": {
                "servo0": 0.0,
                "servo1": 0.0
            }
        }
        _motor_ticks_per_sec = 2000
        def __init__(self, debug_logger, max_devices):
            print("NOTICE: MockRobot instance constructed.")
            self._devices = {}
            self._device_types = {}
            self._max_devices = max_devices
            self._device_counts = {}
            self._debug_logger = debug_logger
            for device_type in self._default_device_properties:
                self._device_counts[device_type] = 0
        def get_value(self, device_id, value_name):
            self._check_property(device_id, value_name)
            if self._device_types[device_id] == "koalabear":
                self._update_koalabear(device_id)
            #print(f"get:{device_id},{value_name}={self._devices[device_id][value_name]}")
            return self._devices[device_id][value_name]
        def set_value(self, device_id, value_name, value):
            self._check_property(device_id, value_name)
            self._debug_logger.print(f"set:{device_id},{value_name}={str(value)}")
            if self._device_types[device_id] == "koalabear":
                self._update_koalabear(device_id)
            expected_type = type(self._devices[device_id][value_name])
            if expected_type == float and type(value) == int:
                value = float(value)
            if expected_type != type(value):
                raise TypeError(f"Expected value of type {expected_type.__name__} for property"
                    f" {value_name}, got {type(value).__name__}.")
            self._devices[device_id][value_name] = value
    
        def _check_property(self, device_id, value_name):
            if not device_id in self._devices:
                for device_type, default_props in self._default_device_properties.items():
                    if value_name in default_props:
                        found_device_type = True
                        break
                if not found_device_type:
                    raise ValueError(f"Unrecognized device property {value_name}.")
                if not device_type in self._max_devices or (self._device_counts[device_type] >= self._max_devices[device_type]):
                    raise ValueError(f"Cannot initialize more devices of type {device_type}. Check the id for typos.")
                self._device_counts[device_type] += 1
                device = {}
                device.update(self._default_device_properties[device_type])
                if device_type == "koalabear":
                    device["_LAST_UPDATED"] = time.time()
                self._devices[device_id] = device
                self._device_types[device_id] = device_type
            if not value_name in self._devices[device_id]:
                raise ValueError(f"Property {value_name} not found on device of type {self._device_types[device_id]}.")
        def _update_koalabear(self, device_id):
            device = self._devices[device_id]
            timestamp = time.time()
            dt = timestamp - device["_LAST_UPDATED"]
            device["_LAST_UPDATED"] = timestamp
            if abs(device["velocity_a"]) > 1:
                raise ValueError("Koalabear velocity a is out of bounds.")
            if abs(device["velocity_b"]) > 1:
                raise ValueError("Koalabear velocity b is out of bounds.")
            device["enc_a"] += device["velocity_a"] * dt * self._motor_ticks_per_sec * (-1 if device["invert_a"] else 1)
            device["enc_b"] += device["velocity_b"] * dt * self._motor_ticks_per_sec * (-1 if device["invert_b"] else 1)

    # End imported file.
    _HELPER_module_export_dict['mock_robot'] = locals()


def _HELPER_import_peripherals():
    if 'peripherals' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    _HELPER_import_devices(); devices = _HELPER_Module('devices') # import devices
    _HELPER_import_util(); util = _HELPER_Module('util') # import util
    import math
    
    class Arm:
        __slots__ = ("_elbow_motor", "_elbow_goal_encoder", "_elbow_start_encoder", "_debug_logger",
            "_forearm_motor", "_forearm_wheel", "_is_forearm_goal_set")
        _elbow_motor_controller = "6_12234750113563914332"
        _forearm_motor_controller = "6_8989232379725682226"
        _forearm_length = util.inches_to_meters(7.5)
        _midarm_length = util.inches_to_meters(18)
        _upperarm_length = util.inches_to_meters(10.1)
        _upperarm_mount_height = util.inches_to_meters(7)
        _upperarm_angle_range = (0, math.pi) # in radians
        _ticks_per_rotation = 475 #64 * 30.125 / 1.42 
        def __init__(self, debug_logger, robot):
            self._elbow_motor = (devices.MotorPair(robot, debug_logger, self._elbow_motor_controller,
                "a", self._elbow_motor_controller, "b").set_pid(None, None, None))
            self._elbow_motor.reset_encoder()
            self._forearm_motor = devices.Motor(robot, debug_logger, self._forearm_motor_controller,
                "a").set_pid(None, None, None).set_invert(True)
            self._forearm_motor.reset_encoder()
            self._forearm_wheel = devices.Wheel(debug_logger, self._forearm_motor,
                util.inches_to_meters(1.5), self._ticks_per_rotation)
            self._debug_logger = debug_logger
            self._is_forearm_goal_set = False
        def set_goal_height(self, goal_height, velocity):
            if not ((self._upperarm_mount_height + self._upperarm_length - self._midarm_length)
                < goal_height < (self._upperarm_mount_height + self._upperarm_length
                + self._midarm_length)):
                raise ValueError(f"Goal height {goal_height} is out of bounds.")
            theta = math.acos((self._upperarm_length - goal_height + self._upperarm_mount_height)
                / self._midarm_length)
            self._elbow_goal_encoder = theta / (2 * math.pi) * self._ticks_per_rotation
            self._elbow_start_encoder = self._elbow_motor.get_encoder()
        def set_goal_extension(self, goal_extension, velocity):
            if not 0 <= goal_extension <= 1:
                raise ValueError(f"Goal extension {goal_extension} is out of bounds.")
            self._forearm_wheel.set_goal(goal_extension * self._forearm_length, velocity)
        def update(self):
            if self._elbow_start_encoder == None:
                return
            encoder = self._elbow_motor.get_encoder()
            start_encoder_diff = self._elbow_start_encoder - self._elbow_goal_encoder
            encoder_diff = encoder - self._elbow_goal_encoder
            if (not self._is_elbow_in_range()
                or math.copysign(start_encoder_diff, encoder_diff) != start_encoder_diff):
                elbow_velocity = 0
                self._debug_logger.print_once("Arm.update: motion completed", "Arm motion completed."
                    f" encoder: {encoder} encoder lower bound: {self._upperarm_angle_range[0] / (2 * math.pi) * self._ticks_per_rotation}"
                    f" encoder upper bound: {self._upperarm_angle_range[1] / (2 * math.pi) * self._ticks_per_rotation}"
                    f" was in range: {self._is_elbow_in_range()}")
            else:
                elbow_velocity = math.copysign(1, encoder_diff)
            self._elbow_motor.set_velocity(forearm_velocity)
            self._forearm_wheel.update()
            return elbow_velocity != 0
        def update_input(self, input_object):
            self._elbow_motor.set_velocity(input_object.elbow_velocity if self._is_elbow_in_range()
                else 0)
            #if input_object.forearm_velocity:
            #    goal = (0.75 * self._forearm_length) if input_object.forearm_velocity > 0 else 0
            #    self._debug_logger.print(f"forearm goal: {goal}")
            #    self._forearm_wheel.set_goal(goal, input_object.forearm_velocity)
            #elif input_object.forearm_goal:
            #    self._is_forearm_goal_set = True
            #    self._forearm_wheel.set_goal(input_object.forearm_goal, 1)
            #elif not self._is_forearm_goal_set:
            #    self._forearm_wheel.stop()
            #self._forearm_wheel.update()
            #if self._forearm_wheel.get_goal_progress() >= 1:
            #    self._is_forearm_goal_set = False
            self._forearm_motor.set_velocity(input_object.forearm_velocity)
    
        def _is_elbow_in_range(self):
            return True # TODO: kludge
            encoder = self._elbow_motor.get_encoder()
            return (encoder > (self._upperarm_angle_range[0] / (2 * math.pi) * self._ticks_per_rotation)
                and encoder < (self._upperarm_angle_range[1] / (2 * math.pi) * self._ticks_per_rotation)) 
    
    class Hand:
        __slots__ = "_debug_logger", "_servo", "_position" 
        _move_increment = 5/90 # servo accepts a number in degrees (hopefully)
        def __init__(self, debug_logger, servo):
            self._servo = servo
            self._debug_logger = debug_logger
            self._position = 0
            self.close()
        def open(self):
            self._servo.set_position(1) # also try 30 degrees
        def close(self):
            self._servo.set_position(-1)
        def update_input(self, input_object):
            #self._debug_logger.print(f"hand status: {input_object.hand_status}")
            #self._move_to(self._position + input_object.hand_status * self._move_increment)
            if input_object.hand_status == 1:
                self.open()
            elif input_object.hand_status == -1:
                self.close()
    
        def _move_to(self, pos):
            self._servo.set_position(pos)
            self._position = pos

    # End imported file.
    _HELPER_module_export_dict['peripherals'] = locals()


def _HELPER_import_input():
    if 'input' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    _HELPER_import_util(); util = _HELPER_Module('util') # import util
    
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
            self._debug_logger.print("forearm power: " + self._bidirectional_input(Gamepad.get_value("button_a"),
                 Gamepad.get_value("button_y")))
            return Input(
                drive_left = drive_left,
                drive_right = drive_right,
                turn = 0,
                elbow_velocity = self._calc_gamepad_elbow_velocity(),
                forearm_goal = None, # TODO: decide on keybinds
                forearm_velocity = self._bidirectional_input(Gamepad.get_value("button_y"),
                     Gamepad.get_value("button_a")) * 0.5,
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
            turn = -Gamepad.get_value("joystick_left_x")
            if abs(turn) < self._gamepad_tolerance:
                turn = 0
            if self._test_button_pressed("l_bumper", False):
                self._hand_opened = not self._hand_opened
                hand_status = 1 if self._hand_opened else -1
            else:
                hand_status = 0
            #hand_status = ((1 if self._test_button_pressed("l_bumper", False) else 0)
            #    - (1 if self._test_button_pressed("l_trigger", False) else 0))
            self._debug_logger.print("forearm power: " + str(self._bidirectional_input(Gamepad.get_value("button_a"),
                Gamepad.get_value("button_y"))))
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

    # End imported file.
    _HELPER_module_export_dict['input'] = locals()


def _HELPER_import_chassis():
    if 'chassis' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    import math
    _HELPER_import_devices(); devices = _HELPER_Module('devices') # import devices
    _HELPER_import_path(); path = _HELPER_Module('path') # import path
    _HELPER_import_util(); util = _HELPER_Module('util') # import util
    import time
    
    class QueuedMotion:
        __slots__ = "_update_func", "_data", "_setup_func"
        def __init__(self, update_func, data, setup_func=None):
            self._update_func = update_func
            self._data = data
            self._setup_func = setup_func
        def setup(self):
            if self._setup_func:
                self._setup_func()
        def update(self):
            return self._update_func(self._data)
        def match_update_func(self, update_func):
            return self._update_func == update_func
        def get_data(self):
            return self._data
    
    class BaseQueuedChassis:
        __slots__ = "_queue", "_position", "_angle", "_debug_logger", "_is_idle"
        def __init__(self, debug_logger, starting_position, starting_angle):
            self._queue = []
            self._debug_logger = debug_logger
            self._position = starting_position
            self._angle = starting_angle
            self._is_idle = True
        def move(self, end_pos, UNUSED_angle):
            """Autonomous mode only. Moves the chassis along a path."""
            angle = 2 * (self._angle - math.atan2(end_pos[1] - self._position[1], end_pos[0] - self._position[0]))
            self._queue.append(QueuedMotion(self._update_move,
                path.Path(self._position, end_pos, angle)))
            self._position = end_pos
        def orient(self, angle):
            """Autonomous mode only. Rotates the chassis in place to align with the given angle in radians."""
            self.turn(angle - self._angle)
            self._angle = angle
        def turn(self, angle):
            """Autonomous mode only. Rotates the chassis in place by the given angle in radians."""
            self._queue.append(QueuedMotion(self._update_turn, angle))
            self._angle += angle
        def peripheral_action(self, peripheral, action):
            self._queue.append(QueuedMotion(self._update_peripheral, peripheral, setup_func=action))
        def update(self):
            """Autonomous mode only. Updates state and motor powers."""
            if self._queue and self._is_idle:
                self._on_start_new_motion(self._queue[0])
                self._is_idle = False
            if self._queue and not self._queue[0].update():
                print("Chassis: next queue item")
                self._queue.pop(0)
                if self._queue:
                    self._on_start_new_motion(self._queue[0])
                    self._queue[0].setup()
            elif not self._queue and not self._is_idle:
                self._on_queue_finish()
                self._is_idle = True
            self._on_post_update()
        def update_input(self, input):
            raise NotImplementedError()
    
        def _on_start_new_motion(self, motion):
            pass
        def _on_queue_finish(self):
            pass
        def _on_post_update(self):
            pass
        def _update_move(self, data):
            raise NotImplementedError()
        def _update_turn(self, data):
            raise NotImplementedError()
        def _update_peripheral(self, data):
            raise NotImplementedError()
    
    class TestChassis(BaseQueuedChassis):
        """Test chassis for pimulator.pierobotics.org."""
        # width = 26.7;               // width of robot, inches
        # height = 20;                // height or robot, inches
        # wheelWidth = 20;            // wheelbase width, inches
        # wRadius = 2;                // radius of a wheel, inches
        # MaxX = 192;                 // maximum X value, inches, field is 12'x12'
        # MaxY = 144;                 // maximum Y value, inches, field is 12'x12'
        # robotTypeNum: 0 = light, 1 = medium (default), 2 = heavy
        # this.accel = (8 - robotTypeNum) / 5 * 0.05413; // Larger robots accelerate more slowly
        # this.maxVel = robotTypeNum / 5 * 1.236;        // Larger robots have a higher top speed
    
        # note: pimulator assumes a 12'x12' field, while the Spring 2023 competition is played on a
        # 12'x16'. this shouldn't matter for the purposes of testing since we don't intend to leave
        # our half of the field.
        __slots__ = ("_motors", "_prev_motor_velocity", "_motion_start_timestamp", "_max_acceleration",
            "_max_velocity", "_wheelspan")
        _robot_types = ("light", "medium", "heavy")
        _robot_type_wheelspans = (9.06, 12.39, 8.98)
        _tick_rate_ms = 50
    
        def __init__(self, robot, debug_logger, starting_position, starting_angle, robot_type):
            super().__init__(debug_logger, starting_position, starting_angle)
            self._motors = util.LRStruct(
                left = devices.Motor(robot, debug_logger, "koala_bear", "a").set_invert(False),
                right = devices.Motor(robot, debug_logger, "koala_bear", "b").set_invert(True)
            )
            if not robot_type in self._robot_types:
                raise ValueError("Invalid robot type.")
            robot_type_num = self._robot_types.index(robot_type) + 3
            self._max_acceleration = util.inches_to_meters((8 - robot_type_num) / 5 * 0.05413) * (1000 / self._tick_rate_ms) # knowing PIE this is probably in inches/sec^2
            self._max_velocity = util.inches_to_meters(robot_type_num / 5 * 1.236) * (1000 / self._tick_rate_ms) # same above
            print(f"max accel: {self._max_acceleration} max vel: {self._max_velocity}")
            self._wheelspan = util.inches_to_meters(
                self._robot_type_wheelspans[self._robot_types.index(robot_type)])
            self._prev_motor_velocity = util.LRStruct(0, 0)
        def update_input(self, input):
            self._motors.left.set_velocity(input.drive.left + input.turn)
            self._motors.right.set_velocity(input.drive.right - input.turn)
    
        def _on_start_new_motion(self, motion):
            self._motion_start_timestamp = time.time()
        def _on_queue_finish(self):
            # might be redundant
            self._motors.left.set_velocity(0)
            self._motors.right.set_velocity(0)
        def _on_post_update(self):
            pass
        def _calculate_move(self, path):
            left_dist = path.get_offset_length(self._wheelspan / 2)
            right_dist = path.get_offset_length(-self._wheelspan / 2)
            return (left_dist, right_dist)
        def _calculate_turn(self, angle):
            goal_dist = angle / self._wheelspan / 2
            left_dist = math.copysign(goal_dist, angle)
            right_dist = -math.copysign(goal_dist, angle)
            return (left_dist, right_dist)
        def _sum_wheel_dists(self, motion_list):
            left_dist = 0
            right_dist = 0
            for motion in motion_list:
                if motion.match_update_func(self._update_move):
                    calc_func = self._calculate_move
                elif motion.match_update_func(self._update_turn):
                    calc_func = self._calculate_turn
                elif motion.match_update_func(self._update_peripheral):
                    calc_func = lambda: (0, 0)
                wheel_dists = calc_func(motion.get_data())
                left_dist += wheel_dists[0]
                right_dist += wheel_dists[1]
            return (left_dist, right_dist)
        def _get_actual_motor_velocity(self, motor_idx):
            if motor_idx == 0:
                motor = self._motors.left
                prev_velocity = self._prev_motor_velocity.left
            elif motor_idx == 1:
                motor = self._motors.right
                prev_velocity = self._prev_motor_velocity.right
            else:
                raise ValueError(f"Invalid motor index {motor_idx}.")
            target_velocity = motor.get_velocity() * self._max_velocity
            elapsed = self._motion_start_timestamp - time.time()
            delta = target_velocity - prev_velocity
            if delta == 0:
                return 0
            progress = min(1, elapsed * self._max_acceleration / delta)
            return prev_velocity + progress * delta
        def _update_move(self, path):
            return self._update_motors(*self._calculate_move(path))
        def _update_turn(self, angle):
            return self._update_motors(*self._calculate_turn(angle))
        def _update_peripheral(self, peripheral):
            return peripheral.update()
        def _update_motors(self, left_dist, right_dist):
            #if len(self._queue) == 1:
            #    should_deaccelerate = True
            #else:
            #    future_motor_dists = self._sum_wheel_dists(self._queue[1:])
            #    min_dist_idx = 0 if future_motor_dists[0] < future_motor_dists[1] else 1
            #    should_deaccelerate = not self._can_deaccelerate_before_dist(
            #        self._get_actual_motor_velocity(min_dist_idx), future_motor_dists[min_dist_idx])
            should_deaccelerate = False # TODO: why
            (left_deacc_time, left_finish_time) = self._estimate_travel_time(
                self._get_actual_motor_velocity(0), left_dist, should_deaccelerate)
            (right_deacc_time, right_finish_time) = self._estimate_travel_time(
                self._get_actual_motor_velocity(1), right_dist, should_deaccelerate)
            elapsed = time.time() - self._motion_start_timestamp
            self._debug_logger.print(f"left actual velocity = {self._get_actual_motor_velocity(0)} right actual velocity"
                f" = {self._get_actual_motor_velocity(1)} left_deacc_time = {left_deacc_time} left_finish_time = {left_finish_time}"
                f"\nright_deacc_time = {right_deacc_time} right_finish_time = {right_finish_time} elapsed = {elapsed}"
                f"\nleft_dist = {left_dist} right_dist = {right_dist}")
            if elapsed > min(left_deacc_time, right_deacc_time):
                self._motors.left.set_velocity(0)
                self._motors.right.set_velocity(0)
            else:
                max_abs_dist = max(abs(left_dist), abs(right_dist))
                self._motors.left.set_velocity(left_dist / max_abs_dist)
                self._motors.right.set_velocity(right_dist / max_abs_dist)
            return elapsed <= min(left_finish_time, right_finish_time)
        def _estimate_travel_time(self, current_velocity, dist, should_deaccelerate):
            d_f = abs(dist)
            v_max = self._max_velocity
            v_i = abs(current_velocity)
            a = self._max_acceleration
            if should_deaccelerate:
                if self._will_hit_max_velocity(current_velocity, dist):
                    # Case 2: v_c > v_max
                    t_f = (d_f / v_max) + (v_i ** 2 / (2 * a * v_max)) + ((2 * v_max - v_i) / a)
                    t_c = t_f - (v_max / a)
                else:
                    # Case 1: v_c <= v_max
                    # might be -2 * v_i - 1 - math.sqrt...
                    t_f = (-2 * v_i - 1 + math.sqrt((-4 * v_i ** 2) + (4 * v_i) + (64 * a * d_f) + 1)) / (4 * a)
                    t_c = (t_f / 2) - (v_i / (2 * a))
            else:
                # might be v_i - math.sqrt...
                # also we might have to divide by a inside min
                t_f = min(-v_i + math.sqrt(v_i ** 2 + (2 * a * d_f)), v_max) / a
                self._debug_logger.print(f"v_max / a = {v_max / a} t_f = {t_f}")
                t_c = t_f # no deacceleration before the end
    
            return (t_c, t_f)
        def _will_hit_max_velocity(self, current_velocity, dist):
            return (self._max_velocity ** 2) > (current_velocity ** 2 + 2 * self._max_acceleration * abs(dist))
        def _can_deaccelerate_before_dist(self, current_velocity, dist):
            v_i = abs(current_velocity)
            a = self._max_acceleration
            return abs(dist) <= v_i ** 2 * a + 0.5 * a ** 3 + v_i ** 4
    
    class QuadChassis(BaseQueuedChassis):
        """The rectangular two-motor drive chassis in use since 3/13/2023."""
        __slots__ = "_motors", "_wheels"
        _wheelspan = util.inches_to_meters(14.5)
        _drive_controller_id = "6_10833107448071795766"
        _ticks_per_rotation = 475 #64 * 30.125 / 1.42 # 30.125 probably a gear ratio, 1.42 magic number
        def __init__(self, robot, debug_logger, starting_position, starting_angle):
            super().__init__(debug_logger, starting_position, starting_angle)
            self._motors = util.LRStruct(
                left = (devices.Motor(robot, debug_logger, self._drive_controller_id, "b")
                    .set_pid(None, None, None).set_invert(False)),
                right = (devices.Motor(robot, debug_logger, self._drive_controller_id, "a")
                    .set_pid(None, None, None).set_invert(True))
            )
            self._wheels = util.LRStruct(
                left = devices.Wheel(debug_logger, self._motors.left, util.inches_to_meters(2),
                    self._ticks_per_rotation),
                right = devices.Wheel(debug_logger, self._motors.right, util.inches_to_meters(2),
                    self._ticks_per_rotation)
            )
        
        def update_input(self, input):
            """Teleop mode only. Takes common inputs and updates the motors' strengths."""
            self._motors.left.set_velocity(input.drive.left + input.turn)
            self._motors.right.set_velocity(input.drive.right - input.turn)
        
        def _on_start_new_motion(self, motion):
            self._motors.left.reset_encoder()
            self._motors.right.reset_encoder()
            if motion.match_update_func(self._update_move):
                calc_func = self._calculate_move
            elif motion.match_update_func(self._update_turn):
                calc_func = self._calculate_turn
            elif motion.match_update_func(self._update_peripheral):
                calc_func = lambda: (0, 0)
            left_dist, right_dist = calc_func(motion.get_data())
            max_abs_dist = max(abs(left_dist), abs(right_dist)) or 1 # don't divide by 0
            self._wheels.left.set_goal(left_dist, left_dist / max_abs_dist)
            self._wheels.right.set_goal(right_dist, right_dist / max_abs_dist)
        def _on_queue_finish(self):
            self._wheels.left.stop()
            self._wheels.right.stop()
        def _on_post_update(self):
            self._wheels.left.update()
            self._wheels.right.update()
        def _calculate_move(self, path):
            left_dist = path.get_offset_length(self._wheelspan / 2)
            right_dist = path.get_offset_length(-self._wheelspan / 2)
            return left_dist, right_dist
        def _update_move(self, path):
            return self._update_motors(*self._calculate_move(path))
        def _calculate_turn(self, angle):
            goal_dist = angle / self._wheelspan / 2
            left_dist = math.copysign(goal_dist, angle)
            right_dist = -math.copysign(goal_dist, angle)
            return left_dist, right_dist
        def _update_turn(self, angle):
            return self._update_motors(*self._calculate_turn(angle))
        def _update_motors(self, left_dist, right_dist):
            max_abs_dist = max(abs(left_dist), abs(right_dist))
            left_progress = self._wheels.left.get_goal_progress()
            right_progress = self._wheels.right.get_goal_progress()
            # TODO: balance velocities using progress
            self._wheels.left.set_velocity(left_dist / max_abs_dist)
            self._wheels.right.set_velocity(right_dist / max_abs_dist)
            self._debug_logger.print(f"left_dist: {left_dist} right_dist: {right_dist} left_progress: "
                f"{left_progress} right_progress: {right_progress}")
            return min(left_progress, right_progress) < 1
        def _update_peripheral(self, peripheral):
            return peripheral.update()
    

    # End imported file.
    _HELPER_module_export_dict['chassis'] = locals()


def _HELPER_import_devices():
    if 'devices' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    import math
    
    class Motor:
        """Wraps a KoalaBear-controlled motor."""
        __slots__ = "_controller", "_motor", "_robot", "_debug_logger", "_is_inverted"
        def __init__(self, robot, debug_logger, controller_id, motor):
            self._controller = controller_id
            self._motor = motor
            self._robot = robot
            self._debug_logger = debug_logger
            self._is_inverted = False
        
        def set_invert(self, invert):
            self._set("invert", invert)
            self._is_inverted = invert
            return self
        def set_deadband(self, deadband):
            self._set("deadband", deadband)
            return self
        def set_pid(self, p, i, d):
            if not (p or i or d):
                self._set("pid_enabled", False)
                return self
            self._set("pid_enabled", True)
            if p:
                self._set("pid_kp", p)
            if i:
                self._set("pid_ki", i)
            if d:
                self._set("pid_kd", d)
            return self
        def set_velocity(self, velocity):
            self._set("velocity", velocity)
            return self
        def get_velocity(self):
            return self._get("velocity")
        def get_encoder(self):
            return self._get("enc") * (-1 if self._is_inverted else 1)
        def reset_encoder(self):
            self._set("enc", 0)
        
        def _set(self, key, value):
            self._robot.set_value(self._controller, key + "_" + self._motor, value)
        def _get(self, key):
            return self._robot.get_value(self._controller, key + "_" + self._motor)
        
    class MotorPair(Motor):
        __slots__ = "_paired_motor"
        def __init__(self, robot, debug_logger, controller_id, motor_suffix,
            paired_controller_id, paired_motor_suffix):
            super().__init__(robot, debug_logger, controller_id, motor_suffix)
            self._paired_motor = Motor(robot, debug_logger, paired_controller_id,
                paired_motor_suffix) #.set_invert(True)
        def set_invert(self, invert):
            super().set_invert(invert)
            #self._paired_motor.set_invert(not invert)
            self._paired_motor.set_invert(invert)
            return self
        def set_deadband(deadband):
            super().set_deadband(self, deadband)
            self._paired_motor.set_deadband(deadband)
            return self
        def set_pid(self, p, i, d):
            super().set_pid(p, i, d)
            self._paired_motor.set_pid(p, i, d)
            return self
        def set_velocity(self, velocity):
            #self._debug_logger.print(f"MotorPair velocity: {velocity}")
            super().set_velocity(velocity)
            self._paired_motor.set_velocity(velocity)
            return self
    
    class Wheel:
        """Represents a wheel that may be ran to a goal position."""
        # goal and radius are in meters
        __slots__ = ("_motor", "_radius", "_ticks_per_rot", "_goal_pos", "_velocity", "_debug_logger",
            "_start_pos")
        def __init__(self, debug_logger, motor, radius, ticks_per_rotation):
            self._motor = motor
            self._radius = radius
            self._ticks_per_rot = ticks_per_rotation
            self._debug_logger = debug_logger
            self._start_pos = None
        
        def set_goal(self, goal, velocity):
            self._start_pos = self._motor.get_encoder()
            self._goal_pos = math.ceil(goal / (self._radius * 2 * math.pi) * self._ticks_per_rot) 
            self._motor.set_velocity(math.copysign(velocity, self._goal_pos))
            self._velocity = velocity
        def set_velocity(self, velocity):
            if self.get_goal_progress() < 1:
                self._motor.set_velocity(math.copysign(velocity, self._goal_pos))
        def get_goal_progress(self):
            if self._start_pos == None:
                return 0
            #self._debug_logger.print(f"{self._motor._motor} goal pos: {self._goal_pos} encoder: {self._motor.get_encoder()} start pos: {self._start_pos}")
            if self._goal_pos == self._start_pos:
                #print("goal progress is 0 for some reason")
                return 1
            return (self._motor.get_encoder() - self._start_pos) / (self._goal_pos - self._start_pos)
        def stop(self):
            self._goal_pos = self._motor.get_encoder()
            self._motor.set_velocity(0)
        def update(self):
            if self.get_goal_progress() >= 1:
                self._motor.set_velocity(0)
    
    class Servo:
        __slots__ = "_controller", "_servo", "_robot"
        def __init__(self, robot, controller, servo):
            self._controller = controller
            self._servo = servo
            self._robot = robot
        def set_position(self, position):
            self._robot.set_value(self._controller, "servo" + self._servo, position)

    # End imported file.
    _HELPER_module_export_dict['devices'] = locals()


def _HELPER_import_util():
    if 'util' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    class LRStruct:
        __slots__ = "left", "right"
        def __init__(self, left, right):
            self.left = left
            self.right = right
    class DebugLogger:
        __slots__ = "_default_interval", "_tick", "_printed_tags"
        def __init__(self, default_interval):
            self._default_interval = default_interval
            self._tick = 0
            self._printed_tags = {}
        def tick(self):
            self._tick += 1
        def lazy_print(self, func, interval=None):
            if interval == None:
                interval = self._default_interval
            if (self._tick % interval) == 0:
                print(func())
        def print(self, msg, interval=None):
            self.lazy_print(lambda: msg, interval)
        def lazy_print_once(self, tag, func):
            if not (tag in self._printed_tags):
                self._printed_tags[tag] = True
                print(func())
        def print_once(self, tag, msg):
            self.lazy_print_once(tag, lambda: msg)
        def reset_print_tag(self, tag):
            if tag in self._printed_tags:
                del self._printed_tags[tag]
    def inches_to_meters(inches):
        return inches / 39.3700787

    # End imported file.
    _HELPER_module_export_dict['util'] = locals()


def _HELPER_import_path():
    if 'path' in _HELPER_module_export_dict:
        return

    # Begin imported file.
    import math
    
    class Path:
        __slots__ = "_angle", "_start_pos", "_end_pos", "_pivot", "_radius", "_start_theta"
        def __init__(self, start_pos, end_pos, angle):
            # Angle is in radians. negative is counterclockwise.
            self._angle = angle
            self._start_pos = start_pos
            self._end_pos = end_pos
            if angle != 0:
                # If angle is 0 the path is a line
                self._calculate_arc_details()
        
        def dist_to_point(self, dist):
            """Gets the point on the path that is the given distance from the start."""
            if self._angle == 0:
                (a_x, a_y) = self._start_pos
                (b_x, b_y) = self._end_pos
                c_x = a_x + dist * (b_x - a_x)
                c_y = a_y + dist * (b_y - a_y)
                return (c_x, c_y)
            else:
                (p_x, p_y) = self._pivot
                # theta = arc_length * 2 * pi / circumference = arc_length / radius
                theta = dist / self._radius
                return (p_x + math.cos(theta), p_y + math.sin(theta))
        def point_to_dist(self, point):
            """Gets how far the point is along the direction of the path."""
            (a_x, a_y) = self._start_pos
            (b_x, b_y) = self._end_pos
            (c_x, c_y) = point
            if self._angle == 0:
                if a_y == b_y:
                    return (c_x, a_y)
                elif a_x == b_x:
                    return (a_x, c_y)
                else:
                    x = (((a_x - b_x) / (b_y - a_y) * c_x - c_y + (a_y - b_y) / (b_x - a_x) * a_x + a_y)
                        / ((a_x - b_x) / (b_y - a_y) + (a_y - b_y) / (b_x - a_x)))
                    y = (b_y - a_y) / (b_x - a_x) * x + (a_y - b_y) / (b_x - b_y) * a_x + a_y
                    return (x, y)
            else:
                return ((math.atan2(c_y - self._pivot[1], a_x - self._pivot[0]) - self._start_theta)
                    * self._radius)
        def get_offset_length(self, offset):
            if self._angle == 0:
                (a_x, a_y) = self._end_pos
                (b_x, b_y) = self._start_pos
                return math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
            return self._angle / (self._radius + offset)
        
        def _calculate_arc_details(self):
            """Calculates the center and radius of the arc segment that is the path."""
            (a_x, a_y) = self._end_pos
            (b_x, b_y) = self._start_pos
            # let d be the distance between a and b
            d = math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
            # let l be the distance between c and p
            l = d / (2 * math.tan(self._angle / 2))
            # let c be the midpoint of segment ab
            c_x = (a_x + b_x) / 2
            c_y = (a_y + b_y) / 2
            # Selector determines which pivot (there are two possible) to pick
            selector = 1 if self._angle > 0 else -1
            if b_y == a_y:
                # Special case, calculating m_cp would divide by zero
                p_x = c_x
                p_y = c_y + selector * l
            else:
                # let m_cp be the slope of segment cp
                m_cp = (a_x - b_x) / (b_y - a_y)
                # let p be the pivot
                p_x = c_x + selector * math.sqrt(l ** 2 / (1 + m_cp ** 2))
                p_y = m_cp * (p_x - c_x) + c_y
            
            self._pivot = (p_x, p_y)
            self._radius = d / (2 * math.sin(self._angle / 2))
            self._start_theta = math.atan2(a_y - p_y, a_x - p_x)

    # End imported file.
    _HELPER_module_export_dict['path'] = locals()


# End imports.
import math
_HELPER_import_chassis(); chassis = _HELPER_Module('chassis') # import chassis
_HELPER_import_path(); path = _HELPER_Module('path') # import path
_HELPER_import_input(); input = _HELPER_Module('input') # import input
_HELPER_import_util(); util = _HELPER_Module('util') # import util
_HELPER_import_peripherals(); peripherals = _HELPER_Module('peripherals') # import peripherals
_HELPER_import_devices(); devices = _HELPER_Module('devices') # import devices
_HELPER_import_mock_robot(); mock_robot = _HELPER_Module('mock_robot') # import mock_robot
#from challenges import * # apparently we don't need to have challenges on the robot

chassis_object = None
robot_object = None
input_generator = None
debug_logger = None
hand = None
arm = None

@_HELPER_entry_point
def create_robot():
    create_debug_logger()
    global robot_object
    if not robot_object:
        #robot_object = mock_robot.MockRobot(debug_logger, {"koalabear": 2, "servocontroller": 1})
        robot_object = Robot
@_HELPER_entry_point
def create_debug_logger():
    global debug_logger
    if not debug_logger:
        debug_logger = util.DebugLogger(10000)
@_HELPER_entry_point
def create_chassis():
    create_robot()
    create_debug_logger()
    global chassis_object
    if not chassis_object:
        chassis_object = chassis.QuadChassis(robot_object, debug_logger, (0, 0), 0)
        #chassis_object = chassis.TestChassis(robot_object, debug_logger, (0, 0), 0, "medium")
@_HELPER_entry_point
def create_input_generator():
    create_debug_logger()
    global input_generator
    if not input_generator:
        input_generator = input.WeirdInputGenerator(debug_logger, gamepad_tolerance=0.06)
@_HELPER_entry_point
def create_hand():
    create_robot()
    create_debug_logger()
    global hand
    if not hand:
        hand = peripherals.Hand(debug_logger, devices.Servo(robot_object, "4_779575167933185031",
            "0"))
@_HELPER_entry_point
def create_arm():
    create_robot()
    create_debug_logger()
    global arm
    if not arm:
        arm = peripherals.Arm(debug_logger, robot_object) 

@_HELPER_entry_point
def autonomous_setup():
    create_debug_logger()
    create_chassis()
    create_arm()
    create_hand()
    chassis_object.turn(math.radians(90))
    #chassis_object.move((4, 3), 5)
    chassis_object.move((1, 0), 0)
    #chassis_object.peripheral_action(arm, lambda x: x.set_goal_height(0.5, 0.5))
@_HELPER_entry_point
def autonomous_main():
    chassis_object.update()
    debug_logger.tick()
@_HELPER_entry_point
def teleop_setup():
    create_debug_logger()
    create_chassis()
    create_arm()
    create_hand()
    create_input_generator()
@_HELPER_entry_point
def teleop_main():
    input_object = input_generator.generate_gamepad()
    #debug_logger.print(str(input_object))
    chassis_object.update_input(input_object)
    arm.update_input(input_object)
    hand.update_input(input_object)
    debug_logger.tick()

