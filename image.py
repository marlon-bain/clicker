import random
import numpy as np


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