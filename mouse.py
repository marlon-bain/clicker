from scipy import interpolate
from pynput.mouse import Button, Controller
import config
import random
import time
import human_input
import math

random.seed(time.time())

x_points = [0, 1, 2, 3, 4, 5, 6, 7]
y_points = [0, 2, 22, 39, 85, 92, 98, 100]

x_points = map(lambda x: x / 7.0, x_points)
y_points = map(lambda x: x / 100.0, y_points)

class Mouse:
    def __init__(self):
        self.mouse = Controller()
        self.human_sampler = human_input.HumanInput()

    def f(self, x):
        tck = interpolate.splrep(x_points, y_points)
        return interpolate.splev(x, tck)

    def smooth_move(self, x, y):
        delay = self.human_sampler.get_click_interval_ms() / 1000.0
        print("Sleeping for " + str(delay))
        time.sleep(abs(delay))

        original = self.mouse.position
        direction = (x - original[0], y - original[1])

        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        movement_time = self.human_sampler.get_mouse_move_time_ms(int(distance), 50)
        if movement_time % 2 == 1:
            movement_time += 1

        granularity = 1
        for t in range(0, movement_time, granularity):
            t = t / float(movement_time)
            t = self.human_sampler.get_mouse_move_progress(t)
            self.mouse.position = (original[0] + t * direction[0], original[1] + t * direction[1])
            time.sleep(0.005)

        self.mouse.position = (x, y)
        self.mouse.move(4, 4)
        self.mouse.move(-4, -4)

    def click_in_frame(self, x, y, scroll=True, right=False, move_after=True):
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
        self.smooth_move(y + config.MONITOR['left'], x + config.MONITOR['top'])

        # Press and release
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
            self.smooth_move(original_position[0], original_position[1])


    def move_randomly(self, scroll):
        width = config.MONITOR['width']
        height = config.MONITOR['height']

        for n in range(random.randrange(3)):
            should_scroll = scroll and (random.randint(0, 2) == 0)

            if should_scroll:
                self.mouse.press(Button.middle)

            self.smooth_move(random.randrange(width), random.randrange(height))

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