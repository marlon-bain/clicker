import random
import numpy as np
import cv2 as cv

def mask_colour(img, colour):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Range for yew magenta
    lower_green = np.array([colour[0], colour[1], colour[2]])
    upper_green = np.array([colour[0] + 1, colour[1], colour[2]])
    mask1 = cv.inRange(hsv, lower_green, upper_green)

    res1 = cv.bitwise_and(img, img, mask=mask1)
    return get_random_masked_pixel(res1)

def get_first_masked_pixel(img):
    result = np.transpose(np.nonzero(img))
    if len(result) == 0:
        return None

    return result[0][:-1]


def get_random_masked_pixel(img):
    result = np.transpose(np.nonzero(img))
    if len(result) == 0:
        return None

    return result[random.randrange(len(result))][:-1]