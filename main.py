import asyncio
from bleak import BleakScanner, BleakClient
from KeyboardSteer import KeyboardSteer

HUB_CHARACTERISTIC_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
HUB_DEVICE_NAME = "Pybricks Hub"


async def main():
    def handle_disconnect(_):
        print("Hub was disconnected.")

    def handle_receive(_, data: bytearray):
        if data[0] == 0x01:  # "write stdout" event (0x01)
            payload = data[1:]
            if payload == b"Welcome":
                event.set()
                print("Hub is ready to play!")
            print("Received:", payload)

    async def send(data):
        await client.write_gatt_char(
            HUB_CHARACTERISTIC_UUID,
            b"\x06" + data.encode(),  # prepend "write stdin" command (0x06)
            response=True
        )

    # ------------------

    steer = KeyboardSteer()
    event = asyncio.Event()
    hubDevice = await BleakScanner.find_device_by_name(HUB_DEVICE_NAME)
    if hubDevice is None:
        print(f"Could not find hub with name: {HUB_DEVICE_NAME}")
        return

    async with BleakClient(hubDevice, handle_disconnect) as client:
        print("Connected to BLE device", client.is_connected)
        await client.start_notify(HUB_CHARACTERISTIC_UUID, handle_receive)
        await asyncio.sleep(1)
        print("Press green button on the hub to start ...")
        await event.wait()
        event.clear()
        print("... playing")

        while True:
            steer.waitUntilPress()
            isShutDown = steer.isShutdown()
            isEscape = steer.isEscape()
            dataToSend = f"{steer.powerControl()};{steer.steerControl()};{int(steer.isStop())};{int(isShutDown)}"
            # print(dataToSend)
            await send(dataToSend)
            if isEscape or isShutDown:
                break
            # await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
