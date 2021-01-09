import math
from time import monotonic

import adafruit_fancyled.adafruit_fancyled as fancy

import event_loop_handlers
from const import GRAY, PURPLE, RED, WHITE, trellis
from utilities import scale


def clear():
    # Clear pixels and set up toggle button
    trellis.pixels.fill(0)
    # TODO: Make brightness based on sun elevation
    trellis.pixels.brightness = 0.5
    trellis.pixels[0, 0] = PURPLE
    trellis.pixels[3, 0] = PURPLE
    trellis.pixels[0, 7] = RED
    trellis.pixels[1, 7] = GRAY
    trellis.pixels[2, 7] = RED
    trellis.pixels.show()


def animate():
    tick_size = 1.5
    tick = monotonic() % tick_size
    slow_tick_size = 10.0
    slow_tick = monotonic() % slow_tick_size
    trellis.pixels[1, 7] = [
        scale(math.sin(tick / tick_size * 3.14), (-1, 1), (10, 245))
    ] * 3
    color = fancy.CHSV(round(slow_tick / slow_tick_size * 255))
    packed = color.pack()
    trellis.pixels[2, 7] = packed


# TODO: Only show brightness button if supported
def choose_brightness():
    while len(trellis.pressed_keys) != 0:
        pass
    for x_index in range(4):
        for y_index in range(8):
            brightness = (y_index + 1) * 31.875
            trellis.pixels[x_index, y_index] = (brightness,) * 3
    while len(trellis.pressed_keys) == 0:
        trellis.pixels.show()
    clear()
    event_loop_handlers.render_screen()
    pixel_num = trellis.pressed_keys[0][1]
    while len(trellis.pressed_keys) != 0:
        pass
    return pixel_num


# TODO: Only show color button if supported
def choose_color():
    while len(trellis.pressed_keys) != 0:
        pass
    for x_index in range(4):
        for y_index in range(8):
            if x_index == 0:
                sat = 1.0
            elif x_index == 1:
                sat = 0.9
            elif x_index == 2:
                sat = 0.8
            else:
                sat = 0.0
            color = fancy.CHSV(y_index / 8.0, sat, 1.0)
            packed = color.pack()
            trellis.pixels[x_index, y_index] = packed
    while len(trellis.pressed_keys) == 0:
        trellis.pixels.show()
    clear()
    event_loop_handlers.render_screen()
    hue = round(scale(trellis.pressed_keys[0][1], (0, 8), (0, 360)))
    pressed_x = trellis.pressed_keys[0][0]
    if pressed_x == 0:
        sat = 100
    elif pressed_x == 1:
        sat = 90
    elif pressed_x == 2:
        sat = 80
    else:
        sat = 0
    while len(trellis.pressed_keys) != 0:
        pass
    return hue, sat
