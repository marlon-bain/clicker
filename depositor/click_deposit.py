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

        # Range for compass anchor
        lower_cyan = np.array([180 / 2, 200, 200])
        upper_cyan = np.array([181 / 2, 255, 255])
        mask1 = cv.inRange(hsv, lower_cyan, upper_cyan)

        mask2 = cv.morphologyEx(mask1, cv.MORPH_ERODE, np.ones((20, 20), np.uint8))
        res1 = cv.bitwise_and(img, img, mask=mask2)
        pixel = image.get_first_masked_pixel(res1)

        # Numbers are picked so that current location is at the precise centre
        minimap_height = 15
        minimap_width = 15
        x_offset = 505
        y_offset = -190
        x_start = pixel[0] + x_offset
        x_end = x_start + minimap_height
        y_start = pixel[1] + y_offset
        y_end = y_start + minimap_width

        minimap_point_screenspace = (random.randrange(x_start, x_end), random.randrange(y_start, y_end))
        return minimap_point_screenspace

    def on_image(self, img):
        self.click_pixel = self.process_image(img)

    def act(self):
        if self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1])
            self.exit = True
        else:
            print("Can't find deposit option; exiting")

    def transition(self):
        return self.exit
