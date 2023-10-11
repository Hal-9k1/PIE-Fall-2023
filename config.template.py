# config.py: a generated file holding externally set program configuration.
# Configuration is exposed through functions because some may return mocks,
# which will be created on the spot.

import inputmapping
import components
import mockrobot

raise RuntimeError("The template cannot be used as-is.")

def get_input_mapping_class():
    pass
def get_drive_component_class():
    pass
def create_robot():
    pass
def create_input_source():
    pass
def create_autonomous_queue():
    pass

# "name": (id, [motor_slot])
_device_ids = {

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
