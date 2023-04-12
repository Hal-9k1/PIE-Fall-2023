import math
import devices
import path
import util

class TestChassis:
    """Test chassis for pimulator.pierobotics.org."""
    def __init__(self, robot, starting_position, starting_angle):
        self._queue = []
        self._position = starting_position
        self._angle = starting_angle
        self._motors = util.LRStruct(
            left = devices.Motor(robot, "koala_bear", "a"),
            right = devices.Motor(robot, "koala_bear", "b").invert()
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
    __slots__ = "_motors", "_wheels", "_position", "_angle", "_queue", "_init_encs"
    _wheelspan = 0.3683
    def __init__(self, robot, starting_position, starting_angle):
        self._queue = []
        self._position = starting_position
        self._angle = starting_angle
        self._motors = util.LRStruct(
            left = devices.Motor(robot, "koala_bear", "a"),
            right = devices.Motor(robot, "koala_bear", "b").invert()
        )
        ticks_per_rotation = 64 * 30.125 / 1.42 # 30.125 probably a gear ratio, 1.42 magic number
        self._wheels = util.LRStruct(
            left = devices.Wheel(self._motors.left, 0.0508, ticks_per_rotation),
            right = devices.Wheel(self._motors.right, 0.0508, ticks_per_rotation)
        )
        self._init_encs = util.LRStruct(left = 0, right = 0)
    
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
            self._init_encs = util.LRStruct(
                left = self._motors.left.get_encoder(),
                right = self._motors.right.get_encoder()
            )
        self._wheels.left.update()
        self._wheels.right.update()
    def update_input(self, input):
        """Teleop mode only. Takes common inputs and updates the motors' strengths."""
        self._motors.left.set_velocity(input.drive.left + input.turn)
        self._motors.right.set_velocity(input.drive.right - input.turn)
    
    def _update_move(self, path):
        left_dist = (path.get_offset_length(self._wheelspan / 2) - self._motors.left.get_encoder()
            + self._init_encs.left)
        right_dist = (path.get_offset_length(-self._wheelspan / 2)
            - self._motors.right.get_encoder() + self._init_encs.left)
        return self._update_motors(left_dist, right_dist)
    def _update_turn(self, angle):
        goal_dist = angle / self._wheelspan / 2
        left_dist = math.copysign(goal_dist, angle) - self._motors.left.get_encoder() + self._init_encs.left
        right_dist = -math.copysign(goal_dist, angle) - self._motors.right.get_encoder() + self._init_encs.right
        return self._update_motors(left_dist, right_dist)
    def _update_motors(self, left_dist, right_dist):
        max_abs_dist = max(abs(left_dist), abs(right_dist))
        self._wheels.left.set_goal(left_dist, left_dist / max_abs_dist)
        self._wheels.right.set_goal(right_dist, right_dist / max_abs_dist)
        left_progress = self._wheels.left.get_goal_progress()
        right_progress = self._wheels.right.get_goal_progress()
        return min(left_progress, right_progress) < 1

