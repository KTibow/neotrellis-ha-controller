from __main__ import trellis

from const import GREEN, RED


def get_payload(data_string):
    """Get the last bit of info separated by ("""
    return data_string.split("(")[-1]


def draw_status(is_on):
    """Set top middle LEDs to green if passed True"""
    main_color = GREEN if is_on else RED
    trellis.pixels[1, 0] = main_color
    trellis.pixels[2, 0] = main_color
