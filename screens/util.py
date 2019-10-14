import pygame
import os


HEIGHT = 720
WIDTH = 1280


def get_image(path, ext='png'):
    return pygame.image.load(os.path.join('assets', 'image',
                                          f'{path}.{ext}')).convert()


def scroll(screen, image, x_pos):
    screen.blit(image, (x_pos, 0))
    screen.blit(image, (-1280 + x_pos, 0))
    return (x_pos + 1270) % 1280


def tick(clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    pygame.display.update()
    clock.tick(120)
    return True


class Easing(object):

    NEWTON_ITERATIONS = 4
    NEWTON_MIN_SLOPE = 0.001
    SUBDIV_PRECISION = 0.0000001
    SUBDIV_MAX_ITER = 10
    k_spline_table_size = 11
    k_sample_step_size = 1 / (k_spline_table_size - 1)

    def __init__(self, ease_prof, steps, start, stop):
        self.ease_prof = ease_prof
        self.steps = steps
        self.step_size = 1 / self.steps
        self.step_frac = 0
        self.cur_step = 0
        self.sample_values = []
        self.start = start
        self.stop = stop
        for i in range(self.k_spline_table_size):
            self.sample_values.append(
                self._calc_bezier(i * self.k_sample_step_size,
                                  self.ease_prof[0], self.ease_prof[2]))

    def _calc_bezier(self, t, a, b):
        return (((1-3*b+3*a)*t+(3*b-6*a))*t+(3*a))*t

    def _get_slope(self, t, a, b):
        return 3*(1-3*b+3*a)*t*t+2*(3*b-6*a)*t+(3*a)

    def _binary_subdivide(self, s, a, b):
        cur_s = 0
        cur_t = 0
        i = 0
        while abs(cur_s) > self.SUBDIV_PRECISION and i < self.SUBDIV_MAX_ITER:
            cur_t = a + (b - a) / 2
            cur_s = self._calc_bezier(cur_t, self.ease_prof[0],
                                      self.ease_prof[2]) - s
            if cur_s > 0:
                b = cur_t
            else:
                a = cur_t
            i += 1
        return cur_t

    def _newton_raphson_iterate(self, s, t):
        for _ in range(self.NEWTON_ITERATIONS):
            cur_slope = self._get_slope(t, self.ease_prof[0],
                                        self.ease_prof[2])
            if cur_slope == 0:
                return t
            cur_s = (self._calc_bezier(t, self.ease_prof[0], self.ease_prof[2])
                     - s)
            t -= cur_s / cur_slope
        return t

    def _get_t_for_s(self, s):
        interval_start = 0
        cur_sample = 1
        last_sample = self.k_spline_table_size - 1
        while cur_sample != last_sample and self.sample_values[cur_sample] < s:
            interval_start += self.k_sample_step_size
            cur_sample += 1
        dist = ((s - self.sample_values[cur_sample - 1]) /
                (self.sample_values[cur_sample]
                 - self.sample_values[cur_sample - 1]))
        t = interval_start + dist * self.k_sample_step_size
        init_slope = self._get_slope(t, self.ease_prof[0], self.ease_prof[2])
        if init_slope >= self.NEWTON_MIN_SLOPE:
            return self._newton_raphson_iterate(s, t)
        elif init_slope == 0:
            return t
        return self._binary_subdivide(s, interval_start, interval_start +
                                      self.k_sample_step_size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur_step == self.steps:
            raise StopIteration
        elif self.cur_step == self.steps - 1:
            res = 1
        elif self.cur_step == 0:
            res = 0
        else:
            res = self._calc_bezier(self._get_t_for_s(self.step_frac),
                                    self.ease_prof[1], self.ease_prof[3])
        self.cur_step += 1
        self.step_frac += self.step_size
        return res * (self.stop - self.start) + self.start


class EaseLinear(Easing):
    def __init__(self, steps, start, stop):
        self.steps = steps
        self.step_size = 1 / self.steps
        self.step_frac = 0
        self.cur_step = 0
        self.sample_values = []
        self.start = start
        self.stop = stop

    def __next__(self):
        if self.cur_step >= self.steps - 1:
            res = 1
        elif self.cur_step == 0:
            res = 0
        else:
            res = self.step_frac
        self.cur_step += 1
        self.step_frac += self.step_size
        return res * (self.stop - self.start) + self.start


class EaseInSine(Easing):
    def __init__(self, steps, start, stop):
        super().__init__([0.47, 0, 0.745, 0.715], steps, start, stop)


class EaseOutSine(Easing):
    def __init__(self, steps, start, stop):
        super().__init__([0.39, 0.575, 0.565, 1], steps, start, stop)