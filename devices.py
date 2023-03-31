class Motor:
    """Wraps a KoalaBear-controlled motor."""
    __slots__ = "_controller", "_motor"
    def __init__(self, controller_id, motor):
        self._controller = controller_id
        self._motor = motor
    
    def invert(self):
        self._set("invert", True)
        return self
    def set_deadband(self, deadband):
        self._set("deadband", deadband)
        return self
    def set_pid(self, pid_tuple):
        if pid[0]:
            self._set("pid_kp", pid[0])
        if pid[1]:
            self._set("pid_ki", pid[1])
        if pid[2]:
            self._set("pid_kd", pid[2])
        return self
    def set_velocity(self, velocity):
        self._set("velocity", velocity)
        return self
    def get_velocity(self):
        return self._get("velocity")
    def get_encoder(self):
        return self._get("enc")
    
    def _set(self, key, value):
        Robot.set_value(self._controller, key + "_" + self._motor, value)
    def _get(self, key):
        return Robot.get_value(self._controller, key + "_" + self._motor)
    
class Wheel:
    # goal and radius are in meters
    __slots__ = "__motor", "__radius", "__ticks_per_rot", "__goal_pos", "__goal_delta"
    def __init__(self, motor, radius, ticks_per_rotation):
        self.__motor = motor
        self.__radius = radius
        self.__ticks_per_rot = ticks_per_rotation
    
    def set_goal(self, goal, velocity):
        self.__goal_delta = math.ceil(goal / (radius * 2 * math.pi) * self.__ticks_per_rot)
        self.__goal_pos = self.__motor.get_encoder() + self.__goal_delta 
        self.__motor.set_velocity(math.copysign(velocity, __goal_pos))
    def get_goal_progress(self):
        return (self.__goal_pos - self.__motor.get_encoder()) / self.__goal_delta
    def stop(self):
        self.__goal_pos = self.__motor.get_encoder()
        self.__motor.set_velocity(0)
    def update(self):
        delta = self.__goal_pos - self.__motor.get_encoder()
        if self.get_goal_progress() >= 1:
            self.__motor.set_velocity(0)
