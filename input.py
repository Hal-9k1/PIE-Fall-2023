class TankInputGenerator:
    def generate_keyboard():
        return {
            drive: {
                left: (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0),
                right: (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
            },
            turn: 0
        }
    def generate_gamepad():
        raise NotImplementedError
        return {
            drive: {
                left: drive,
                right: drive
            },
            turn: (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        }
class WeirdInputController:
    def generate_keyboard():
        drive = (1 if Keyboard.get_value("w") else 0) - (1 if Keyboard.get_value("s") else 0)
        return {
            drive: {
                left: drive,
                right: drive
            },
            turn: (1 if Keyboard.get_value("d") else 0) - (1 if Keyboard.get_value("a") else 0)
        }
    def generate_gamepad():
        drive = Gamepad.get_value("joystick_left_y")
        return {
            drive: {
                left: drive,
                right: drive
            },
            turn: Gamepad.get_value("joystick_left_x")
        }
