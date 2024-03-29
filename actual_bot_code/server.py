#!/usr/bin/env python3

# NAME: server.py
# PURPOSE: running local, on-board robomodules server
# AUTHORS: Harvard Undergraduate Robotics Club

import robomodules
import os
from messages import MsgType

###
# BIND_ADDRESS is the IP address of the host computer the server should bind to. The default is localhost,
# which means all connections will be maintained through the computer running this script, 
# which is useful for testing purposes. 
# If attempting to create an externally facing server that your bot can connect to via WiFi, BIND_ADDRESS should
# be the local IP address of the computer running this server. BIND_ADDRESS is an environmental variable, so
# it can be changed with "export BIND_ADDRESS=...".
###
ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")

###
# BIND_PORT is the port the server is listening on. All modules (such as the game engine) should connect
# to this port.
###
PORT = os.environ.get("LOCAL_PORT", 11295)

def main():
    server = robomodules.Server(ADDRESS, PORT, MsgType)
    # server = robomodules.Server("192.168.0.196", PORT, MsgType)
    # print("Address: " + str("192.168.0.196"))
    print("Address: " + str(ADDRESS))
    print("Port: " + str(PORT))
    server.run()

if __name__ == "__main__":
    main()
