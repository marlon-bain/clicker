import math


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
