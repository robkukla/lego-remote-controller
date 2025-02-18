# LEGO Remote Controller

## Description
This project is a remote controller for LEGO Technic Hub. It uses BLE (Bluetooth Low Energy) to communicate with the hub and sends commands to control the motors.

## Requirements
- Python 3.7
  - libraries
    - bleak
    - keyboard
    - asyncio
- LEGO Technic Hub

## Installation
1. Install hub controller script using pybricsk.com (hub/controller.py)
2. Turn on Technic Hub
3. Run main.py
4. When script connect to hub, press green 
5. Use keyboard to control motors (using arrow keys and space as break)
6. To exit press ESC
7. To shut down hub press x