import cv2 as cv
import image
import numpy as np
import vector

class Orient:
    def __init__(self, parent):
        self.parent = parent
        self.click_pixel = None
        self.exit = False

    def process_img(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Range for compass anchor
        lower_cyan = np.array([180 / 2, 200, 200])
        upper_cyan = np.array([181 / 2, 255, 255])
        mask1 = cv.inRange(hsv, lower_cyan, upper_cyan)

        mask2 = cv.morphologyEx(mask1, cv.MORPH_ERODE, np.ones((20, 20), np.uint8))
        res1 = cv.bitwise_and(img, img, mask=mask2)
        return image.get_random_masked_pixel(res1)

    def on_image(self, img):
        print("Attempting to get compass data")
        if self.parent.location is None:
            print("Waiting for location data")
            return

        self.click_pixel = self.process_img(img)
        if self.click_pixel is None:
            print("Can't find compass; exiting")
            exit(1)

    def on_message(self, message):
        pass

    def act(self):
        if self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1], scroll=False)
            self.click_pixel = None
            self.exit = True

    def transition(self):
        return self.exit
