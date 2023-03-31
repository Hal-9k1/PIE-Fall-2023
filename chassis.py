import math
import devices
import path
import util

class TestChassis:
    """Test chassis for pimulator.pierobotics.org."""
    __slots__ = "__motors", "__wheels", "__position", "__angle", "__queue", "__init_encs"
    __wheelspan = 1 # meters
    
    def __init__(self, starting_position, starting_angle):
        self.__queue = []
        self.__position = starting_position
        self.__angle = starting_angle
        self.__motors = util.LRStruct(
            left = devices.Motor("koala_bear", "a"),
            right = devices.Motor("koala_bear", "b").invert()
        )
        self.__wheels = util.LRStruct(
            left = devices.Wheel(__motors.left, 0.5 / math.pi, 8),
            right = devices.Wheel(__motors.right, 0.5 / math.pi, 8)
        )
        self.__init_encs = util.LRStruct(left = 0, right = 0)
    
    def move(self, end_pos, angle):
        """Autonomous mode only. Moves the chassis along a path."""
        self.__queue.append((self.__update_move, path.Path(__position, end_pos, angle)))
        self.__position = end_pos
    def orient(self, angle):
        """Autonomous mode only. Rotates the chassis in place to align with the given angle in radians."""
        self.turn(angle - self.__angle)
        self.__angle = angle
    def turn(self, angle):
        """Autonomous mode only. Rotates the chassis in place by the given angle in radians."""
        self.__queue.append((self.__update_turn, angle))
        self.__angle += angle
    def update(self):
        """Autonomous mode only. Updates state and motor powers."""
        if self.__queue:
            if not self.__queue[0][0](self.__queue[0][1]):
                self.__queue.pop(0)
                self.__init_encs = util.LRStruct(
                    left = self.__motors.left.get_encoder(),
                    right = self.__motors.right.get_encoder()
                )
        __wheels.left.update()
        __wheels.right.update()
    def update_input(self, input):
        """Teleop mode only. Takes common inputs and updates the motors' strengths."""
        __motors.left.set_velocity(input.drive.left + input.turn)
        __motors.right.set_velocity(input.drive.right - input.turn)
    
    def __update_move(self, path):
        
        return True
    def __update_turn(self, angle):
        wheel_dist = angle / self.__wheelspan
        
        return

class QuadChassis:
    """The rectangular two-wheel drive chassis in use since 3/13/2023."""
    __slots__ = "__motors", "__wheels"
    def __init__(self, starting_position, starting_angle):
        self.__motors = util.LRStruct(
            left = devices.Motor("koala_bear", "a"),
            right = devices.Motor("koala_bear", "b").invert()
        )
        self.__wheels = util.LRStruct(
            left = devices.Wheel(__motors.left, 0.5, 8),
            right = devices.Wheel(__motors.right, 0.5, 8)
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
        __motors.left.set_velocity(input.drive.left + input.turn)
        __motors.right.set_velocity(input.drive.right - input.turn)
