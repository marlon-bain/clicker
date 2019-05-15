import cv2 as cv
import numpy as np
import image


class ClickBanker:
    def __init__(self, parent):
        self.parent = parent
        self.click_pixel = None
        self.exit = False

    def on_message(self):
        pass

    def process_image(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Range for yew magenta
        lower_green = np.array([300 / 2, 200, 200])
        upper_green = np.array([301 / 2, 255, 255])
        mask1 = cv.inRange(hsv, lower_green, upper_green)

        mask1 = cv.morphologyEx(mask1, cv.MORPH_ERODE, np.ones((5, 5), np.uint8))

        res1 = cv.bitwise_and(img, img, mask=mask1)
        return image.get_random_masked_pixel(res1)

    def on_image(self, img):
        self.click_pixel = self.process_image(img)

    def act(self):
        if self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1], scroll=False, move_after=False, right=True, fast=True)
            self.exit = True
        else:
            self.parent.mouse.pan()

    def transition(self):
        return self.exit
