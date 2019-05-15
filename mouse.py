from scipy import interpolate
from pynput.mouse import Button, Controller
import config
import random
import time
import human_input
import vector
import pickle
import math
import numpy as np

random.seed(time.time())

x_points = [0, 1, 2, 3, 4, 5, 6, 7]
y_points = [0, 2, 22, 39, 85, 92, 98, 100]

x_points = map(lambda x: x / 7.0, x_points)
y_points = map(lambda x: x / 100.0, y_points)


class Mouse:
    def __init__(self):
        self.mouse = Controller()
        self.human_sampler = human_input.HumanInput()
        self.paths = pickle.load(open(config.MOUSE_VECTORS_FILENAME, "rb"))
        if len(self.paths) < 3:
            print("Record some mouse paths first")
            exit(0)

    def f(self, x):
        tck = interpolate.splrep(x_points, y_points)
        return interpolate.splev(x, tck)

    def smooth_move(self, x, y, fast=False):
        # delay = self.human_sampler.get_click_interval_ms() / 1000.0
        # time.sleep(abs(delay))

        self.move_using_path(self.paths[random.randrange(len(self.paths))], (x, y), fast)
        self.mouse.move(4, 4)
        self.mouse.move(-4, -4)

    def click_in_frame(self, x, y, scroll=True, right=False, move_after=True, fast=False):
        if y > config.MONITOR['width']:
            print(y, x)
            print("Attempted to click outside of the frame on the x-axis")
            exit(1)

        if x > config.MONITOR['height']:
            print(y, x)
            print("Attempted to click outside of the frame on the y-axis")
            exit(1)

        original_position = self.mouse.position

        # mouse.position = (y, x + top_offset)
        self.smooth_move(y + config.MONITOR['left'], x + config.MONITOR['top'], fast)

        # Press and release
        if not fast:
            delay = int(human_input.sample_normal(50, 15))/ 1000.0
            time.sleep(abs(delay))

        button = Button.left if not right else Button.right
        if config.DEBUG_CLICK:
            print("[MOUSE DOWN]")
        else:
            self.mouse.press(button)

        delay = int(human_input.sample_normal(50, 15))/ 1000.0
        time.sleep(abs(delay))

        if config.DEBUG_CLICK:
            print("[MOUSE UP]")
        else:
            self.mouse.release(button)

        if move_after:
            self.move_randomly(scroll)
            self.smooth_move(original_position[1], original_position[0])


    def move_randomly(self, scroll):
        width = config.MONITOR['width']
        height = config.MONITOR['height']

        should_scroll = scroll and (random.randint(0, 2) == 0)
        if should_scroll:
            self.mouse.press(Button.middle)

        self.smooth_move(random.randrange(height), random.randrange(width))

        if should_scroll:
            self.mouse.release(Button.middle)


    def pan(self):
        width = config.MONITOR['width']
        height = config.MONITOR['height']

        starting_x = random.randrange(int(width / 3.0), int(2 * width / 3.0))
        starting_y = random.randrange(int(height / 3.0), int(2 * height / 3.0))

        ending_x = int(starting_x / 2.0) + random.randrange(-int(width / 6.0), int(width / 6.0))
        ending_y = random.randrange(int(height / 8.0))

        self.smooth_move(starting_x, starting_y)
        self.mouse.press(Button.middle)
        self.smooth_move(ending_x, ending_y)
        self.mouse.release(Button.middle)

    def position(self):
        print(self.mouse.position)


    def move_using_path(self, path, end, fast=False):
        start = self.mouse.position
        # Contingent on recorded paths having an l2 length of sqrt(2) since they go from (0, 0) to (1, 1)

        target = (end[0] - start[0], end[1] - start[1])
        rotate_counter = target[1] < target[0]
        scale_factor = vector.l2_length(target) / math.sqrt(2)
        scale = np.eye(2) * scale_factor

        theta = vector.angle_between(target, (10.0, 10.0))
        if rotate_counter:
            theta = -theta

        c, s = np.cos(theta), np.sin(theta)
        rotate = np.array(((c,-s), (s, c)))

        pause = 0.01 if fast else 0.02
        for point in path:
            point_vector = [[point[0]], [point[1]]]
            transformed_point = scale.dot(rotate).dot(point_vector)
            x = int(transformed_point[0][0] + start[0])
            y = int(transformed_point[1][0] + start[1])
            self.mouse.position = (x, y)
            time.sleep(pause)

        self.mouse.position = end
