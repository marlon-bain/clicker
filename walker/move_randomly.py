import cv2 as cv
import image
import numpy as np
import vector

class MoveRandomly:
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
        pixel = image.get_first_masked_pixel(res1)

        # Numbers are picked so that current location is at the precise centre
        minimap_height = 156
        minimap_width = 174
        x_start = pixel[0]
        x_end = x_start + minimap_height
        y_start = pixel[1]
        y_end = y_start + minimap_width

        world_delta = (5, 5)

        # Scale the vector up since 2 pixels in minimap-space represents 1 tile in RSWorld-space
        minimap_delta = vector.truncate_magnitude((world_delta[0] * 2, world_delta[1] * 2),
                                                min(minimap_width, minimap_height) / 6)
        minimap_center_screenspace = (int((x_start + x_end) / 2.0), int((y_start + y_end) / 2.0))
        minimap_next_click_screenspace = (
        minimap_center_screenspace[0] - minimap_delta[1], minimap_center_screenspace[1] + minimap_delta[0])

        return minimap_next_click_screenspace

    def on_image(self, img):
        self.click_pixel = self.process_img(img)

    def on_message(self, message):
        pass

    def act(self):
        if self.parent.parent.location is not None:
            self.exit = True
            print("Not moving randomly because root already has location")
        elif self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1], scroll=False)
            self.click_pixel = None
            self.exit = True

    def transition(self):
        return self.exit