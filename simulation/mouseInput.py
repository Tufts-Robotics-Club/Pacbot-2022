#!/usr/bin/env python3

# NAME: mouseInput.py
# PURPOSE: input module allowing simulation movement via mouse tracking
# AUTHORS: Ryan McFarlane
# NOTES: allows pacman to teleport/move through walls, which can confuse the 
#        game engine. also assumes the simulation window is one the far left
#        side of your screen.

import os, sys, curses
import robomodules as rm
from messages import *
from pacbot.variables import *
from pacbot.grid import *

##### FOR MOUSE TRACKING #######
import pyautogui
import math
################################

ADDRESS = os.environ.get("BIND_ADDRESS", "localhost")    # address of game engine server
# ADDRESS = os.environ.get("BIND_ADDRESS","192.168.0.196")    # address of game engine server
PORT = os.environ.get("BIND_PORT", 11297)               # port game engine server is listening on

SPEED = 5.0 # originally 1.0
FREQUENCY = SPEED * game_frequency

##### FOR MOUSE TRACKING #######
xCells = 26
yCells = 29
xMin = 26
yMin = 800
xMax = 675
yMax = 80
################################

class InputModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        self.loop.add_reader(sys.stdin, self.keypress)
        self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.cur_dir = right
        self.next_dir = right
        self.state = PacmanState()
        self.state.mode = PacmanState.PAUSED
        self.lives = starting_lives
        self.clicks = 0

    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            self.pacbot_pos[0] += 1
            self.cur_dir = direction
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            self.pacbot_pos[0] -= 1
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            self.pacbot_pos[1] += 1
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            self.pacbot_pos[1] -= 1
            self.cur_dir = direction
            return True
        return False


    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        if msg_type == MsgType.FULL_STATE:
            self.state = msg
            if self.state.lives != self.lives:
                self.lives = self.state.lives
                self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]

    

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        if self.state.mode != PacmanState.PAUSED:
            if not self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1]):
                self._move_if_valid_dir(self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])
        pos_buf = PacmanState.AgentState()
        ############################################################  
        # MOUSE TRACKING
        pos = pyautogui.position()
        mouseX = pos[0]
        gridX = math.ceil((mouseX - xMin) * (xCells/(xMax-xMin)))
        mouseY = pos[1]
        gridY = math.ceil((mouseY - yMin) * (yCells/(yMax-yMin)))
        pos_buf.x = gridX
        pos_buf.y = gridY
        ############################################################
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)

    def keypress(self):
        char = sys.stdin.read(1)
        if char == 'a':
            self.next_dir = left
        elif char == 'd':
            self.next_dir = right
        elif char == 'w':
            self.next_dir = up
        elif char == 's':
            self.next_dir = down
        elif char == 'q':
            self.quit()

def main():
    module = InputModule(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()