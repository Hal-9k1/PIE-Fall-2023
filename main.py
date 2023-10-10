# main.py: holds PiE's entry point functions.

from robotcontroller import RobotController

# Wrap in a top-level function so the preprocessor uses enhanced error reporting.
def create_robot_controller():
    return RobotController()

robot_controller = create_robot_controller()

# Entry point functions:
def autonomous_setup():
    robot_controller.autonomous_setup()
def autonomous_main():
    robot_controller.autonomous_main()
def teleop_setup():
    robot_controller.teleop_setup()
def teleop_main():
    robot_controller.teleop_main()
