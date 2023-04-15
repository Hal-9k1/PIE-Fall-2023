import math
import chassis
import path
import input
import mock_robot
#from challenges import * # apparently we don't need to have challenges on the robot

chassis_object = None
input_generator = None
auto_main_num = 0
teleop_main_num = 0

def get_robot():
    return mock_robot.MockRobot({"koalabear": 1})
    #return Robot
def create_chassis():
    #return chassis.TestChassis(get_robot(), (0, 0), 0)
    return chassis.QuadChassis(get_robot(), (0, 0), 0)
def create_input_generator():
    return input.TankInputGenerator(gamepad_tolerance=0.06) #input.WeirdInputGenerator()

def autonomous_setup():
    global chassis_object
    chassis_object = create_chassis()
    chassis_object.turn(math.radians(45))
    chassis_object.move((4, 3), 5)
def autonomous_main():
    global auto_main_num
    chassis_object.update()
    auto_main_num += 1
def teleop_setup():
    global chassis_object, input_generator
    if not chassis_object:
        chassis_object = create_chassis()
    input_generator = create_input_generator()
def teleop_main():
    global teleop_main_num
    chassis_object.update_input(input_generator.generate_gamepad())
    teleop_main_num += 1
