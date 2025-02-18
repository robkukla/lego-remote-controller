import keyboard

POWER_STEP = 10
POWER_MAX = 100 - POWER_STEP
STEER_STEP = 25
STEER_MAX = 100 - STEER_STEP


class KeyboardSteer:
    def __init__(self):
        self.power = 0
        self.steer = 0

    def powerControl(self):
        powerButtonPressed = False
        if keyboard.is_pressed('up'):
            self.power = self.power + POWER_STEP if self.power <= POWER_MAX else self.power
            powerButtonPressed = True
        if keyboard.is_pressed('down'):
            self.power = self.power - POWER_STEP if self.power >= -POWER_MAX else self.power
            powerButtonPressed = True
        if self.power != 0 and not powerButtonPressed:
            self.power = self.power - POWER_STEP if self.power > 0 else self.power + POWER_STEP
        return self.power

    def steerControl(self):
        steerButtonPressed = False
        if keyboard.is_pressed('left'):
            self.steer = self.steer - STEER_STEP if self.steer >= -STEER_MAX else self.steer
            steerButtonPressed = True
        if keyboard.is_pressed('right'):
            self.steer = self.steer + STEER_STEP if self.steer <= STEER_MAX else self.steer
            steerButtonPressed = True
        if self.steer != 0 and not steerButtonPressed:
            self.steer = self.steer - STEER_STEP if self.steer > 0 else self.steer + STEER_STEP
        return self.steer

    def isStop(self):
        if keyboard.is_pressed('space'):
            self.power = 0
            return True
        return False

    def isEscape(self):
        if keyboard.is_pressed('esc'):
            self.power = 0
            self.steer = 0
            return True
        return False

    def isShutdown(self):
        if keyboard.is_pressed('x'):
            self.power = 0
            self.steer = 0
            return True
        return False

    def waitUntilPress(self):
        keyboard.read_event()
