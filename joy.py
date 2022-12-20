#!/usr/bin/env python
import logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig()
log = logging.getLogger(__name__)
import sys
from subprocess import Popen, PIPE
import time
import configparser

import pygame.joystick
import pygame

from events import *
from inputs import *

class RobotInterface:
    """Interface to RelayBot. Checks that it is running, restarts if it dies. Sends commands over a pipe to stdin"""
    def __init__(self, bot_cmd):
        self.bot_cmd = bot_cmd.split(" ")
        self.relaybot = self._spawn_relaybot()

    def _spawn_relaybot(self):
        return Popen(self.bot_cmd, stdin=PIPE, stdout=sys.stdout)

    def send(self, data):
        if self.relaybot.poll() is not None:
            log.error(f"RelayBot quit with error code {self.relaybot.returncode}")
            self.relaybot = self._spawn_relaybot()
        print(data, file=self.relaybot.stdin)

class Controller:
    """Controller object. The ControllerFactory sets up all the binds.
    Inputs on the controller can register for a tick so that they can emit input even when there isn't an event from the joystick [for mouse movement]
    """
    def __init__(self, controller):
        self.controller = controller
        self.joy = pygame.joystick.Joystick(controller)
        self.joy.init()
        self.tick_listeners = []
        self.axis_map = {}
        self.button_map = {}
        pass

    def add_tick_listener(self, _input):
        """Register an Input element to receive tick events"""
        self.tick_listeners.append(_input)

    def tick(self, i):
        """Run tick on all registered listeners so that they may emit events"""
        for _input in self.tick_listeners:
            _input.tick(i)

    def button_press(self, button, state):
        try:
            self.button_map[button].set_state(state)
        except (AttributeError, KeyError):
            log.exception(f"Failed to register button press for button {button}")
        pass

    def axis_event(self, axis, value):
        try:
            self.axis_map[axis].set_state(value)
        except (AttributeError, KeyError):
            log.exception(f"Failed to register button press for axis {axis}")
        pass

class Config(configparser.ConfigParser):
    """Extension of ConfigParser with some constants"""
    CONTROLLER_SECTION_TEMPLATE = "Controller_{}"
    KEYMAP_SECTION = "keymap"
    BUTTON_MAP_SECTION = "buttonmap"
    AXIS_MAP_SECTION = "axismap"
    MAIN_SECTION = "main"

class ControllerFactory:
    """Returns controllers built from a
