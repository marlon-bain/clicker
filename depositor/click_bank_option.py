import cv2 as cv
import numpy as np
import image
import time
import config


class ClickBankOption:
    def __init__(self, parent):
        self.parent = parent
        self.click_pixel = None
        self.exit = False
        self.pause_before_exit = False

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
        if self.pause_before_exit:
            self.exit = True
        elif self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1])
            self.pause_before_exit = True
            self.click_pixel = None
            time.sleep(config.SETTLING_LATENCY_S)
        else:
            print("Can't find click pixel in click_bank_option")
            exit(1)

    def transition(self):
        if self.parent.settled and self.exit:
            return True

        return False

