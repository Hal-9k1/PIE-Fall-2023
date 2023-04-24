import math
import devices
import path
import util

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

class BaseQueuedChassis:
    __slots__ = "_queue", "_position", "_angle", "_debug_logger"
    def __init__(self, debug_logger, starting_position, starting_angle):
        self._queue = []
        self._debug_logger = debug_logger
        self._position = starting_position
        self._angle = starting_angle
    def move(self, end_pos, angle):
        """Autonomous mode only. Moves the chassis along a path."""
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
        if self._queue and not self._queue[0].update():
            print("next queue item")
            self._queue.pop(0)
            if self._queue:
                self._on_start_new_motion(self._queue[0])
                self._queue[0].setup()
        elif not self._queue:
            self._on_queue_finish()
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
    # 12'x16'.
    __slots__ = "_motors", "_actual_motor_velocity", "_motion_start_timestamp"
    _robot_types = ("light", "medium", "heavy")
    _wheelspan = util.inches_to_meters(20)

    def __init__(self, robot, debug_logger, starting_position, starting_angle, robot_type):
        super().__init__(debug_logger, starting_position, starting_angle)
        self._motors = util.LRStruct(
            left = devices.Motor(robot, "koala_bear", "a").set_invert(False),
            right = devices.Motor(robot, "koala_bear", "b").set_invert(True)
        )
        if not robot_type in self._robot_types:
            raise ValueError("Invalid robot type.")
    def update_input(self, input):
        self._motors.left.set_velocity(input.drive_left + input.turn)
        self._motors.right.set_velocity(input.drive_right - input.turn)

    def _on_start_new_motion(self, motion):
        self._motion_start_timestamp = 0
    def _on_queue_finish(self):
        self._motors.left.stop()
        self._motors.right.stop()
    def _on_post_update(self):
        self._motors.left.update()
        self._motors.right.update()
    def _update_move(self, path):
        left_dist = path.get_offset_length(self._wheelspan / 2)
        right_dist = path.get_offset_length(-self._wheelspan / 2)
        return self._update_motors(left_dist, right_dist)
    def _update_turn(self, angle):
        goal_dist = angle / self._wheelspan / 2
        left_dist = math.copysign(goal_dist, angle)
        right_dist = -math.copysign(goal_dist, angle)
        return self._update_motors(left_dist, right_dist)
    def _update_peripheral(self, peripheral):
        return peripheral.update()
    def _update_motors(self, left_dist, right_dist):
        max_abs_dist = max(abs(left_dist), abs(right_dist))
        self._wheels.left.set_goal(left_dist, left_dist / max_abs_dist)
        self._wheels.right.set_goal(right_dist, right_dist / max_abs_dist)
        raise NotImplementedError()
        # estimate time until deacceleration, then somehow handle deacceleration that before going
        # to the next motion
    def _estimate_travel_time(self, current_velocity, dist, should_deaccelerate):
        # TODO: just finding the travel time is inadequate. we also need to know when to start
        # deaccelerating, if needed
        d_f = dist
        v_max = 
        if self._will_hit_max_velocity():

        return (t_c, t_f)

class QuadChassis(BaseQueuedChassis):
    """The rectangular two-motor drive chassis in use since 3/13/2023."""
    __slots__ = "_motors", "_wheels"
    _wheelspan = util.inches_to_meters(14.5)
    _drive_controller_id = "6_10833107448071795766"
    _ticks_per_rotation = 64 * 30.125 / 1.42 # 30.125 probably a gear ratio, 1.42 magic number
    def __init__(self, robot, debug_logger, starting_position, starting_angle):
        super().__init__(debug_logger, starting_position, starting_angle)
        self._motors = util.LRStruct(
            left = (devices.Motor(robot, debug_logger, self._drive_controller_id, "b")
                .set_pid(None, None, None).set_invert(False)), # TODO: should maybe be False
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
    def _on_queue_finish(self):
        self._wheels.left.stop()
        self._wheels.right.stop()
    def _on_post_update(self):
        self._wheels.left.update()
        self._wheels.right.update()
    def _update_move(self, path):
        left_dist = path.get_offset_length(self._wheelspan / 2)
        right_dist = path.get_offset_length(-self._wheelspan / 2)
        return self._update_motors(left_dist, right_dist)
    def _update_turn(self, angle):
        goal_dist = angle / self._wheelspan / 2
        left_dist = math.copysign(goal_dist, angle)
        right_dist = -math.copysign(goal_dist, angle)
        return self._update_motors(left_dist, right_dist)
    def _update_motors(self, left_dist, right_dist):
        max_abs_dist = max(abs(left_dist), abs(right_dist))
        self._wheels.left.set_goal(left_dist, left_dist / max_abs_dist)
        self._wheels.right.set_goal(right_dist, right_dist / max_abs_dist)
        left_progress = self._wheels.left.get_goal_progress()
        right_progress = self._wheels.right.get_goal_progress()
        self._debug_logger.print(f"left_dist: {left_dist} right_dist: {right_dist} left_progress: {left_progress} right_progress: {right_progress}")
        return min(left_progress, right_progress) < 1
    def _update_peripheral(self, peripheral):
        return peripheral.update()

