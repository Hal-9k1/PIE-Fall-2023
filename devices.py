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
    def set_pid(self, p, i, d):
        if not (p or i or d):
            self._set("pid_enabled", False)
            return
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
        return self._get("enc")
    
    def _set(self, key, value):
        print("set:" + self._controller + ";" + key + "_" + self._motor + ";" + str(value) + ";")
        Robot.set_value(self._controller, key + "_" + self._motor, value)
    def _get(self, key):
        print("get:" + self._controller + ";" + key + "_" + self._motor + ";")
        return Robot.get_value(self._controller, key + "_" + self._motor)
    
class Wheel:
    # goal and radius are in meters
    __slots__ = "_motor", "_radius", "_ticks_per_rot", "_goal_pos", "_goal_delta", "_velocity", "_initialized"
    def __init__(self, motor, radius, ticks_per_rotation):
        self._motor = motor
        self._radius = radius
        self._ticks_per_rot = ticks_per_rotation
        self._initialized = False
    
    def set_goal(self, goal, velocity):
        self._initialized = True
        self._goal_delta = math.ceil(goal / (radius * 2 * math.pi) * self._ticks_per_rot)
        self._goal_pos = self._motor.get_encoder() + self._goal_delta 
        self._motor.set_velocity(math.copysign(velocity, _goal_pos))
        self._velocity = velocity
    def get_goal_progress(self):
        return (self._goal_pos - self._motor.get_encoder()) / self._goal_delta
    def stop(self):
        self._goal_pos = self._motor.get_encoder()
        self._motor.set_velocity(0)
    def update(self):
        if not self._initialized:
            return # no commands given yet
        delta = self._goal_pos - self._motor.get_encoder()
        if self.get_goal_progress() >= 1:
            self._motor.set_velocity(0)
