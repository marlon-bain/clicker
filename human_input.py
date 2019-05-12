import time
from sympy.stats import sample, Normal, cdf
import math
import config

# This class contains probability distributions based on human action
class HumanInput:
    def __init__(self):
        self.is_focused = True

        self.focus_loss_density = Normal('focus_loss', config.FOCUS_LENGTH_MEAN, config.FOCUS_LENGTH_STD)
        self.start_time = time.time() + sample(self.focus_loss_density)

        self.click_interval_density_focused = Normal('focused_click', 50, 20)
        self.click_interval_density_unfocused = Normal('unfocused_click', 200, 50)

        self.movement_speed_density = Normal('mouse_movement', 0.5, 0.10)

    def get_mouse_move_progress(self, t):
        assert t >= 0
        assert t <= 1

        return float(cdf(self.movement_speed_density)(t))

    def get_mouse_move_time_ms(self, distance, target_size):
        # Fitt's law
        mean = math.log(2 * distance / float(target_size), 2) * config.MOUSE_SPEED_SCALE
        return int(20 + sample(Normal('temp_mouse_move', abs(mean), abs(mean / 4.0))))

    def get_click_interval_ms(self):
        if time.time() - self.start_time > config.FOCUS_LENGTH_MEAN:
            self.is_focused = not self.is_focused
            self.start_time = time.time() + sample(self.focus_loss_density)

        if self.is_focused:
            return int(sample(self.click_interval_density_focused))
        else:
            return int(sample(self.click_interval_density_unfocused))

def sample_normal(mu, std):
    return int(sample(Normal('temp_normal', mu, std)))

if __name__ == '__main__':
    human = HumanInput()
    for i in range(20):
        print(human.get_mouse_move_progress(0.05 * i))

