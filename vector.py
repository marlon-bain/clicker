import math
import numpy as np


def swap(vector):
    return vector[1], vector[0]

def truncate_magnitude(vector, limit):
    limit = abs(limit)

    magnitude = l2_length(vector)
    if magnitude == 0:
        return vector

    normalized = (vector[0] / magnitude, vector[1] / magnitude)

    if magnitude <= limit:
        return vector
    else:
        return (
            math.floor(normalized[0] * limit),
            math.floor(normalized[1] * limit)
        )


def length(vector):
    return abs(vector[0]) + abs(vector[1])

def l2_length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
