import config
import devices

class BaseComponent:
    def input_tick(self, input_object):
        raise NotImplementedError()
    def check_input_compatability(self, input_mapping):
        raise NotImplementedError()
    def check_queue_compatability(self, auto_queue):
        raise NotImplementedError()

class BaseDriveComponent(BaseComponent):
    def check_input_compatability(self, input_mapping):
        if (self.check_input_compatability ==
            BaseDriveComponent.check_input_compatability):
            raise NotImplementedError()
        return "drive" in input_mapping.get_component_support()

class AngledOmniDrive(BaseComponent):
    def __init__(self, robot):
        self._fl_motor = config.create_motor("drive.flmotor")
        self._fr_motor = config.create_motor("drive.frmotor")
        self._bl_motor = config.create_motor("drive.blmotor")
        self._br_motor = config.create_motor("drive.brmotor")
    def check_input_compatability(self, input_mapping):
        return super().check_input_compatability(input_mapping) and ("omni" in
            input_mapping.get_component_support()["drive"])
    def check_queue_compatability(self, auto_queue):
        return auto_queue.
    def input_tick(self, input_object):
        ax = input_object.axial
        la = input_object.lateral
        ya = input_object.yaw
        raw_velocities = [
            (ax + la) / 2 + ya, # front left points front right
            (ax - la) / 2 - ya, # front right points front left 
            (ax - la) / 2 + ya, # back left points front left
            (ax + la) / 2 - ya, # back right points front right
        ]
        max_abs_vel = max(abs(x) for x in raw_velocities)
        velocities = [x / max_abs_vel for x in raw_velocities]
        self._fl_motor.set_velocity(velocities[0])
        self._fr_motor.set_velocity(velocities[1])
        self._bl_motor.set_velocity(velocities[2])
        self._br_motor.set_velocity(velocities[3])
