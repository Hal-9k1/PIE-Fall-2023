import config

class RobotController:
    def __init__(self):
        self._input_mapping = config.get_input_mapping_class()(config.create_input_source())
        self._robot = config.create_robot()
        self._drive_component = config.get_drive_component_class()(self._robot)
        self._autonomous_queue = config.create_autonomous_queue()
        self._drive_component.check_input_compatability(self._input_mapping)
        self._drive_component.check_queue_compatability(self._autonomous_queue)

    def _common_setup(self):
        self._drive_component.setup()
    def autonomous_setup(self):
        self._common_setup()
        self._autonomous_queue = config.create_autonomous_queue()
    def autonomous_main(self):
        self._autonomous_queue.tick

    def teleop_setup(self):
        self._common_setup()
    def teleop_main(self);
        input_object = self._input_mapping.generate_input()
        self._drive_component.input_tick(input_object)
