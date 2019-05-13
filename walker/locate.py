import cv2 as cv
import image
import numpy as np
import vector

path_to_bank = [
    (3201, 3503),
    (3196, 3490),
    (3185, 3489),
    (3169, 3488)
]

path_to_trees = [
    (3185, 3489),
    (3196, 3490),
    (3201, 3503),
    (3207, 3503)
]

class Locate:
    def __init__(self, parent, reverse=False):
        self.parent = parent
        self.click_pixel = None
        self.exit = False

        self.path = path_to_trees if reverse else path_to_bank
        self.next_path_index = 0
        self.close_enough = False

        self.is_initialized = False

    def initialize(self):
        self.next_path_index = self.get_path_starting_index()
        self.is_initialized = True

    def get_path_starting_index(self):
        # Find point in path closes to current position
        closest_index = 0
        closest_distance = 100
        for i in range(len(self.path)):
            path_coordinate = self.path[i]
            distance_x = abs(self.parent.location[0] - path_coordinate[0])
            distance_y = abs(self.parent.location[1] - path_coordinate[1])
            if distance_x + distance_y < closest_distance:
                closest_distance = distance_x + distance_y
                closest_index = i

        # print("Based on current location, next target in worldspace is ")
        # print(closest_index)
        return closest_index

    def process_img(self, img):
        print("locate.py process_img")
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Range for compass anchor
        lower_cyan = np.array([180 / 2, 200, 200])
        upper_cyan = np.array([181 / 2, 255, 255])
        mask1 = cv.inRange(hsv, lower_cyan, upper_cyan)

        mask2 = cv.morphologyEx(mask1, cv.MORPH_ERODE, np.ones((20, 20), np.uint8))
        res1 = cv.bitwise_and(img, img, mask=mask2)
        pixel = image.get_first_masked_pixel(res1)

        # Numbers are picked so that current location is at the precise centre
        minimap_height = 132
        minimap_width = 150
        x_start = pixel[1]
        x_end = x_start + minimap_width
        y_start = pixel[0]
        y_end = y_start + minimap_height

        # Visualize this for debug purposes
        # minimap = img[y_start:y_end, x_start:x_end]
        minimap_center_screenspace = (
            int((x_start + x_end) / 2.0),
            int((y_start + y_end) / 2.0)
        )

        print("Navigating to point {0}".format(self.next_path_index))
        next_point = self.path[self.next_path_index]
        world_delta = (next_point[0] - self.parent.location[0], next_point[1] - self.parent.location[1])

        # Scale the vector up since 2 pixels in minimap-space represents 1 tile in RSWorld-space
        minimap_delta = vector.truncate_magnitude((world_delta[0] * 4, world_delta[1] * 4), int(min(minimap_width, minimap_height) / 2.5))
        minimap_next_click_screenspace = (minimap_center_screenspace[0] + minimap_delta[0], minimap_center_screenspace[1] - minimap_delta[1])
        return vector.swap(minimap_next_click_screenspace)

    def set_is_close_enough(self):
        if self.next_path_index == len(self.path):
            return

        next_coordinate = self.path[self.next_path_index]
        world_delta = (self.parent.location[0] - next_coordinate[0], self.parent.location[1] - next_coordinate[1])
        distance = vector.l2_length(world_delta)
        close_enough_radius = 8
        self.close_enough = distance <= close_enough_radius

    def on_image(self, img):
        if not self.parent.settled and not self.close_enough:
            return

        self.click_pixel = self.process_img(img)

    def on_message(self, message):
        pass

    def act(self):
        if not self.is_initialized:
            self.initialize()

        self.set_is_close_enough()

        if self.click_pixel is not None:
            self.parent.mouse.click_in_frame(self.click_pixel[0], self.click_pixel[1], scroll=False)
            self.click_pixel = None

        if self.close_enough:
            print("Close enough now; incrementing point")
            self.next_path_index += 1

            # Don't immediately set this; this way, on_image has a chance to click the next point
            # self.set_is_close_enough()

            if self.next_path_index == len(self.path):
                self.exit = True
                print("Close enough to terminal point")

    def transition(self):
        return self.exit
