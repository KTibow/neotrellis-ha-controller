from const import GREEN, RED, trellis


def get_payload(data_string):
    """Get the last bit of info separated by ("""
    return data_string.split("(")[-1]


def draw_status(is_on):
    """Set led colors depending on is_on"""
    main_color = GREEN if is_on else RED
    other_color = RED if is_on else GREEN
    trellis.pixels[1, 0] = main_color
    trellis.pixels[2, 0] = main_color
    trellis.pixels[0, 7] = other_color


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]
