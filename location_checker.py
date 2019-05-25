from walker import walker
import config

class LocationChecker:
    def __init__(self, parent, bottom_left, top_right):
        self.parent = parent
        self.bottom_left = bottom_left
        self.top_right = top_right

    def remediate(self):
        location = self.parent.location
        if location is None:
            return None

        a = location[0] < self.bottom_left[0]
        b = location[1] < self.bottom_left[1]
        c = location[0] > self.top_right[0]
        d = location[1] > self.top_right[1]

        if a or b or c or d:
            print("Location invariant violation by {0}; walking to bank first".format(location))
            print("{0}, {1}, {2}, {3}".format(a, b, c, d))
            if config.MAGIC_LOGS:
                exit(1)
            return walker.BankWalker(self.parent)

        return None


