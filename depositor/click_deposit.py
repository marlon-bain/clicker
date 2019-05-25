import cv2 as cv
import numpy as np
import image
import random


class ClickDeposit:
    def __init__(self, parent):
        self.parent = parent
        self.click_pixel = None
        self.exit = False

    def on_message(self):
        pass

    def process_image(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Range for yew magenta
        lower_green = np.array([300 / 2 , 120, 255])
        upper_green = np.array([301 / 2, 150, 255])
        mask1 = cv.inRange(hsv, lower_green, upper_green)

        res1 = cv.bitwise_and(img, img, mask=mask1)
        return image.get_random_masked_pixel(res1)

    def on_image(self, img):
        self.click_pixel = self.process_image(img)

    def act(self):
        if self.click_pixel is not None:
            print("[Click deposit] Clicking deposit")
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1])
            self.exit = True
        else:
            print("Can't find deposit option; exiting")
            exit(1)

    def transition(self):
        return self.exit
