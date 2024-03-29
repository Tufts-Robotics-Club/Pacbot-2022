#!/usr/bin/env python3

# NAME: gyroModule.py
# PURPOSE: module for continuously calculating, storing, and sending to other 
#          modules the current angular position of the bot
# AUTHORS: Emma Bethel, Ryan McFarlane

import os
from messages.gyroYaw_pb2 import GyroYaw
import robomodules as rm

from gyro import Gyro
from messages import MsgType, message_buffers

FREQUENCY = 1000

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)


class GyroModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.GYRO_YAW]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.yaw = 0
        self.gyro = Gyro()
    
    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.GYRO_YAW:
            if msg.yaw == 0:
                print(f'got zero msg')
                self.yaw = msg.yaw
    
    def tick(self):
        # update stored yaw based on new angular velocity (Euler's method)
        diff = self.gyro.value * (1.0 / FREQUENCY)
        self.yaw += diff

        # send out new yaw as a GYRO_YAW message
        msg = GyroYaw()
        msg.yaw = self.yaw
        self.write(msg.SerializeToString(), MsgType.GYRO_YAW)


def main():
    module = GyroModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()

