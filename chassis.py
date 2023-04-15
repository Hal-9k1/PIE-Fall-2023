import math
import devices
import path
import util

class TestChassis:
    """Test chassis for pimulator.pierobotics.org."""
    # width = 26.7;               // width of robot, inches
    # height = 20;                // height or robot, inches
    # wheelWidth = 20;            // wheelbase width, inches
    # wRadius = 2;                // radius of a wheel, inches
    # MaxX = 192;                 // maximum X value, inches, field is 12'x12'
    # MaxY = 144;                 // maximum Y value, inches, field is 12'x12'
    __slots__ = "_queue", "_position", "_angle", "_motors", "_debug_printer"
    def __init__(self, robot, debug_printer, starting_position, starting_angle):
        self._queue = []
        self._debug_printer = debug_printer
        self._position = starting_position
        self._angle = starting_angle
        self._motors = util.LRStruct(
            left = devices.Motor(robot, "koala_bear", "a").set_invert(False),
            right = devices.Motor(robot, "koala_bear", "b").set_invert(True)
        )
    
    def move(self, end_pos, angle):
        pass
    def orient(self, angle):
        pass
    def turn(self, angle):
        pass
    def update(self):
        pass
    def update_input(self, input):
        pass

class QuadChassis:
    """The rectangular two-motor drive chassis in use since 3/13/2023."""
    __slots__ = "_motors", "_wheels", "_position", "_angle", "_queue", "_debug_printer"
    _wheelspan = 0.3683
    def __init__(self, robot, debug_printer, starting_position, starting_angle):
        self._queue = []
        self._debug_printer = debug_printer
        self._position = starting_position
        self._angle = starting_angle
        self._motors = util.LRStruct(
            left = devices.Motor(robot, debug_printer, "6_15372564724073988682", "b").set_invert(False),
            right = devices.Motor(robot, debug_printer, "6_15372564724073988682", "a").set_invert(True)
        )
        ticks_per_rotation = 64 * 30.125 / 1.42 # 30.125 probably a gear ratio, 1.42 magic number
        self._wheels = util.LRStruct(
            left = devices.Wheel(self._motors.left, 0.0508, ticks_per_rotation),
            right = devices.Wheel(self._motors.right, 0.0508, ticks_per_rotation)
        )
    
    def move(self, end_pos, angle):
        """Autonomous mode only. Moves the chassis along a path."""
        self._queue.append((self._update_move, path.Path(self._position, end_pos, angle)))
        self._position = end_pos
    def orient(self, angle):
        """Autonomous mode only. Rotates the chassis in place to align with the given angle in radians."""
        self.turn(angle - self._angle)
        self._angle = angle
    def turn(self, angle):
        """Autonomous mode only. Rotates the chassis in place by the given angle in radians."""
        self._queue.append((self._update_turn, angle))
        self._angle += angle
    def update(self):
        """Autonomous mode only. Updates state and motor powers."""
        if self._queue and not self._queue[0][0](self._queue[0][1]):
            print("next queue item")
            self._queue.pop(0)
            self._motors.left.reset_encoder()
            self._motors.right.reset_encoder()
        self._wheels.left.update()
        self._wheels.right.update()
    def update_input(self, input):
        """Teleop mode only. Takes common inputs and updates the motors' strengths."""
        self._motors.left.set_velocity(input.drive.left + input.turn)
        self._motors.right.set_velocity(input.drive.right - input.turn)
    
    def _update_move(self, path):
        left_dist = (path.get_offset_length(self._wheelspan / 2)
            * (1 - self._wheels.left.get_goal_progress()))
        right_dist = (path.get_offset_length(-self._wheelspan / 2)
            * (1 - self._wheels.right.get_goal_progress()))
        return self._update_motors(left_dist, right_dist)
    def _update_turn(self, angle):
        goal_dist = angle / self._wheelspan / 2
        left_dist = math.copysign(goal_dist, angle) * (1 - self._wheels.left.get_goal_progress())
        right_dist = -math.copysign(goal_dist, angle) * (1 - self._wheels.right.get_goal_progress())
        return self._update_motors(left_dist, right_dist)
    def _update_motors(self, left_dist, right_dist):
        max_abs_dist = max(abs(left_dist), abs(right_dist))
        self._wheels.left.set_goal(left_dist, left_dist / max_abs_dist)
        self._wheels.right.set_goal(right_dist, right_dist / max_abs_dist)
        left_progress = self._wheels.left.get_goal_progress()
        right_progress = self._wheels.right.get_goal_progress()
        return min(left_progress, right_progress) < 1

