import devices
import util
import math

class Arm:
    __slots__ = "_forearm_motor", "_forearm_goal_encoder", "_forearm_start_encoder"
    _forearm_length = util.inches_to_meters(18)
    _upperarm_length = util.inches_to_meters(10.1)
    _upperarm_mount_height = util.inches_to_meters(7)
    _upperarm_angle_range = (0, math.pi / 2) # in radians
    _ticks_per_rotation = 64 * 30.125 / 1.42 
    def __init__(self, debug_logger, robot):
        self._forearm_motor = (devices.Motor(robot, debug_logger, "6_11068811781328764060", "a")
            .set_pid(None, None, None)) # y opens a closes
        self._forearm_motor.reset_encoder()
    def set_goal_height(self, goal_height, velocity):
        if not ((self._upperarm_mount_height + self._upperarm_length - self._forearm_length)
            < goal_height < (self._upperarm_mount_height + self._upperarm_length
            + self._forearm_length)):
            raise ValueError(f"Goal height {goal_height} is out of bounds.")
        theta = math.acos((self._upperarm_length - goal_height + self._upperarm_mount_height)
            / self._forearm_length)
        self._forearm_goal_encoder = theta / (2 * math.pi) * self._ticks_per_rotation
        self._forearm_start_encoder = self._forearm_motor.get_encoder()
    def update(self):
        if self._forearm_start_encoder == None:
            return
        encoder = self._forearm_motor.get_encoder()
        start_encoder_diff = encoder - self._forearm_start_encoder
        encoder_diff = encoder - self._forearm_goal_encoder
        if (encoder < self._upperarm_angle_range[0] / (2 * math.pi) * self._ticks_per_rotation
            or encoder > self._upperarm_angle_range[1] / (2 * math.pi) * self._ticks_per_rotation
            or math.copysign(start_encoder_diff, encoder_diff) != start_encoder_diff):
            forearm_velocity = 0
        else:
            forearm_velocity = math.copysign(1, start_encoder_diff)
        self._forearm_motor.set_velocity(forearm_velocity)
        print(f"forearm velocity: {forearm_velocity}")
        return forearm_velocity != 0
    def update_input(self, input_object):
        self._forearm_motor.set_velocity(input_object.arm_velocity)
class Hand:
    __slots__ = "_debug_logger", "_servo", "_position" 
    _move_increment = 5/90 # servo accepts a number in degrees (hopefully)
    def __init__(self, debug_logger, servo):
        self._servo = servo
        self._debug_logger = debug_logger
        self._position = 0
    def open(self):
        self._servo.set_position(0.5) # also try 30 degrees
    def close(self):
        self._servo.set_position(-0.5)
    def update_input(self, input_object):
        self._debug_logger.print(f"hand status: {input_object.hand_status}")
        self._move_to(self._position + input_object.hand_status * self._move_increment)

    def _move_to(self, pos):
        self._servo.set_position(pos)
        self._position = pos
