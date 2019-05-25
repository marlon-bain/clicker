import image
import time
import mouse
import config
import numpy as np
import cv2 as cv
import random

import click_banker
import click_bank_option
import click_deposit
import click_bank_box

class Depositor:
    def __init__(self):
        self.current_stage_index = 0
        self.stages = [
            click_bank_box.ClickBankBox(self),
            click_deposit.ClickDeposit(self)
        ] if config.MAGIC_LOGS else [
            click_banker.ClickBanker(self),
            click_bank_option.ClickBankOption(self),
            click_deposit.ClickDeposit(self)
        ]
        self.mouse = mouse.Mouse()
        self.exit = False

        self.settled = True

    def on_image(self, img):
        if self.current_stage_index == len(self.stages):
            return

        self.stages[self.current_stage_index].on_image(img)

    def on_message(self, message):
        if config.LOCATION_TAG in message:
            self.settled = False
        elif config.SETTLED_TAG in message:
            print("[Depositor] Settled")
            self.settled = True

    def transition(self):
        return self.exit

    def act(self):
        if self.current_stage_index == len(self.stages):
            self.exit = True
            return

        self.stages[self.current_stage_index].act()
        if self.stages[self.current_stage_index].transition():
            print("[Depositor] Transitioning")
            self.current_stage_index += 1
