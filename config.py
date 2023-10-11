# config.py: a generated file holding externally set program configuration.
# Configuration is exposed through functions because some may return mocks,
# which will be created on the spot.

import inputmapping
import components
import mockrobot
import devices

def get_input_mapping_class():
    return inputmapping.KeyboardOmniDrive
def get_drive_component_class():
    return components.AngledOmniDrive
def create_robot():
    return Robot
def create_input_source():
    return Keyboard
def create_autonomous_queue():
    return []

# "name": (id, [motor_slot])
_device_ids = {
    "drive.flmotor": ("6_WHATEVER","a"),
    "drive.frmotor": ("6_WHATEVER","b"),
    "drive.blmotor": ("6_WHATEVER","a"),
    "drive.brmotor": ("6_WHATEVER","b"),
}
# "name": (radius, ticks_per_rotation)
_wheel_configs = {

}
def get_device_id(device_name):
    return _device_ids[device_name][0]
def get_motor_config(motor_name):
    if len(_device_ids[motor_name]) == 0:
        raise ValueError(motor_name + " is not the name of a motor.")
    return _device_ids[device_name]
def get_wheel_config(wheel_name):
    return _wheel_configs[wheel_name]
def create_motor(motor_name, robot, debug_logger):
    motor_config = get_motor_config(motor_name)
    return devices.Motor(robot, debug_logger, motor_config[0], motor_config[1])
def create_wheel(wheel_name, motor, debug_logger):
    wheel_config = get_wheel_config(wheel_name)
    return devices.Wheel(debug_logger, motor, wheel_config[0], wheel_config[1])
