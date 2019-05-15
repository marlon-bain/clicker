import cv2 as cv
import image
import numpy as np

class Cut:
    def __init__(self, parent):
        self.parent = parent
        self.click_pixel = None
        self.pan = False

    def process_img(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Range for yew magenta
        lower_green = np.array([300 / 2, 200, 200])
        upper_green = np.array([301 / 2, 255, 255])
        mask1 = cv.inRange(hsv, lower_green, upper_green)

        mask1 = cv.morphologyEx(mask1, cv.MORPH_ERODE, np.ones((40, 40), np.uint8))
        res1 = cv.bitwise_and(img, img, mask=mask1)

        return image.get_random_masked_pixel(res1)

    def on_image(self, img):
        self.click_pixel = self.process_img(img)

    def on_message(self, message):
        pass

    def act(self):
        if self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1], scroll=False, fast=True)
            self.click_pixel = None
            self.pan = False
        else:
            self.pan = True

    def transition(self):
        return True, self.pan, False
