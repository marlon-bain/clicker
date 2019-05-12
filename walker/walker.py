import numpy as np
import cv2 as cv
import image
import mouse
import config
import math
import time

import move_randomly
import orient
import locate


# This class is meant to get you close enough to your target that you can
# just pan around and find them, i.e. this is just minimap navigation
class BankWalker:
    def __init__(self, reverse=False):
        self.current_stage_index = 0
        self.stages = [move_randomly.MoveRandomly(self), orient.Orient(self), locate.Locate(self, reverse=reverse)]
        self.exit = False

        self.mouse = mouse.Mouse()
        self.location = None
        self.settled = True

    def on_message(self, message):
        if config.LOCATION_TAG in message:
            index = message.index(config.LOCATION_TAG) + len(config.LOCATION_TAG)
            coordinates = message[index:].strip().split(",")
            coordinates = map(int, coordinates)

            self.settled = False
            self.location = (coordinates[0], coordinates[1])
        elif config.SETTLED_TAG in message:
            print("Settled")
            self.settled = True
        else:
            if self.current_stage_index == len(self.stages):
                return

            self.stages[self.current_stage_index].on_message(message)

    def on_image(self, img):
        if self.current_stage_index == len(self.stages):
            return

        self.stages[self.current_stage_index].on_image(img)

    def act(self):
        if self.current_stage_index == len(self.stages):
            self.exit = True
            return

        self.stages[self.current_stage_index].act()

        if self.stages[self.current_stage_index].transition():
            print("[Walker] Transitioning to next stage")
            self.current_stage_index += 1

    def transition(self):
        if self.exit and self.settled:
            time.sleep(config.SETTLING_LATENCY_S)
            return True

        return False
