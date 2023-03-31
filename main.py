import math
import chassis
import path
import input
from challenges import *

chassis_object = None
input_controller = None

def create_chassis():
    return chassis.TestChassis((0, 0), 0)

def autonomous_setup():
    global chassis_object
    chassis_object = create_chassis()
    chassis_object.turn(math.radians(45))
    # chassis_object.move((4, 3), 5)

def autonomous_main():
    chassis_object.update()

def teleop_setup():
    global chassis_object, input_controller
    chassis_object = chassis_object or create_chassis()
    input_controller = input.WeirdInputController()

def teleop_main():
    chassis_object.update_input(input_controller.generate_gamepad())
