class Motor:
    __slots__ = "_controller", "_motor"
    def __init__(self, controller_id, motor):
        self._controller = controller
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
    def set_encoder(self, enc_value):
        self._set("enc", enc_value)
        return self
    def get_encoder(self, enc_value):
        return self._get("enc")
    
    def _set(self, key, value):
        Robot.set_value(self._controller, key + "_" + self._motor, value)
    def _get(self, key):
        return Robot.get_value(self._controller, key + "_" + self._motor)

class TestChassis(Chassis):
    """Test chassis for piemultator.pierobotics.org."""
    _motors = {
        left = Motor("koala_bear", "a"),
        right = Motor("koala_bear", "b").invert()
    }
    
    def __init__(self, navigator):
        self._navigator = navigator
        self._queue = []
    def move(self, path):
        """Moves the chassis along an arc."""
        pass
    def orient(self, angle):
        """Rotates the chassis in place."""
        pass
    def update(self):
        """Updates state and motor powers."""
        # Calculate current position from encoders and send to navigator.
        pass