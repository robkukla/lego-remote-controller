# use https://code.pybricks.com
from usys import stdin, stdout
from uselect import poll
from pybricks.tools import wait, read_input_byte
from pybricks.parameters import Color, Port, Direction
from pybricks.hubs import TechnicHub
from pybricks.robotics import Car
from pybricks.pupdevices import Motor

hub = TechnicHub()
keyboard = poll()
keyboard.register(stdin)

rearMotor = Motor(Port.A)
frontMotor = Motor(Port.B)
steer = Motor(Port.D)
car = Car(steer, [frontMotor, rearMotor])

stdout.buffer.write(b"Welcome")
hub.light.blink(Color.BROWN, [250, 250])

dataBuffer = []

def readAllIncomingData():
    global dataBuffer
    b = read_input_byte()
    if not b:
        return False
    dataBuffer.append(b)
    return True

def getMovePower(data):
    return int(data[0])

def getSteer(data):
    return int(data[1])

def getStop(data):
    return bool(int(data[2]))

def getShutdown(data):
    return bool(int(data[3]))

while True:
    while not keyboard.poll(0):
        # waiting for incoming data
        wait(10)

    while readAllIncomingData():
        pass

    try:
        inputData = "".join(map(chr, dataBuffer))
        steeringData = inputData.split(';')
        if len(steeringData) < 4:
            raise Exception
    except:
        stdout.buffer.write(b"INPUT DATA ERROR")
        steeringData = None
        continue
    finally:
        dataBuffer.clear()

    try:
        if getStop(steeringData):
            hub.light.on(Color.RED)
            car.drive_power(0)
        else:
            if getMovePower(steeringData) < 0:
                hub.light.on(Color.WHITE)
            else:
                hub.light.on(Color.GREEN)
            car.drive_power(getMovePower(steeringData))
            car.steer(getSteer(steeringData))
        if getShutdown(steeringData):
            hub.light.blink(Color.BLUE, [100, 100])
            wait(1000)
            hub.system.shutdown()
    except:
        stdout.buffer.write(b"STEERING ERROR")
        continue

    returnData = f"c:{hub.battery.current()};v:{hub.battery.voltage()}"
    stdout.buffer.write(returnData)
