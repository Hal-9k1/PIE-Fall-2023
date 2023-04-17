import math
import chassis
import path
import input
import util
import peripherals
import devices
import mock_robot
#from challenges import * # apparently we don't need to have challenges on the robot

chassis_object = None
input_generator = None
debug_logger = None
hand = None
arm = None

def get_robot():
    #return mock_robot.MockRobot(debug_logger, {"koalabear": 1})
    return Robot
def create_debug_logger():
    global debug_logger
    if not debug_logger:
        debug_logger = util.DebugLogger(10000)
def create_chassis():
    global chassis_object
    if not chassis_object:
        chassis_object = chassis.QuadChassis(get_robot(), debug_logger, (0, 0), 0)
        #chassis_object = chassis.TestChassis(get_robot(), (0, 0), 0)
def create_input_generator():
    global input_generator
    if not input_generator:
        input_generator = input.TankInputGenerator(gamepad_tolerance=0.06) #input.WeirdInputGenerator()
def create_hand():
    global hand
    if not hand:
        hand = peripherals.Hand(debug_logger, devices.Servo(get_robot(), "4_1577456710271169891",
            "0"))
def create_arm():
    global arm
    if not arm:
        arm = peripherals.Arm(debug_logger, get_robot()) 

def autonomous_setup():
    create_debug_logger()
    create_chassis()
    create_arm()
    create_hand()
    chassis_object.turn(math.radians(45))
    chassis_object.move((4, 3), 5)
    chassis_object.peripheral_action(arm, lambda x: x.set_goal_height(0.5, 0.5))
def autonomous_main():
    debug_logger.tick()
    chassis_object.update()
def teleop_setup():
    create_debug_logger()
    create_chassis()
    create_arm()
    create_hand()
    create_input_generator()
def teleop_main():
    debug_logger.tick()
    input_object = input_generator.generate_gamepad()
    chassis_object.update_input(input_object)
    arm.update_input(input_object)
    hand.update_input(input_object)
