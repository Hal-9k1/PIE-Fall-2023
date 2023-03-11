import math
import devices
import path

class TestChassis:
    """Test chassis for pimulator.pierobotics.org."""
    __slots__ = "__wheels", "__angle", "__queue"
    __motors = {
        left = Motor("koala_bear", "a"),
        right = Motor("koala_bear", "b").invert()
    }
    __wheels = {
        left = Wheel(__motors.left, 0.5, 8),
        right = Wheel(__motors.right, 0.5, 8)
    }
    
    def __init__(self, starting_angle):
        self.__queue = []
        self.__angle = starting_angle
    
    def move(self, path):
        """Autonomous mode only. Moves the chassis along a path."""
        self.__queue.append((self.__update_move, path))
    def orient(self, angle):
        """Autonomous mode only. Rotates the chassis in place to align with the given angle."""
        self.turn(angle - self.__angle)
    def turn(self, angle):
        """Autonomous mode only. Rotates the chassis in place by the given angle."""
        self.__queue.append((self.__update_turn, angle))
    def update(self):
        """Autonomous mode only. Updates state and motor powers."""
        if self.__queue:
            if not self.__queue[0][0](self.__queue[0][1]):
                self.__queue.pop(0)
        _wheels.left.update()
        _wheels.right.update()
    def input(self, strength):
        """Teleop mode only. """
        pass
    
    def __update_move(self, path):
        pass
    def __update_turn(self, angle):
        pass