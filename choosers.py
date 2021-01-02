import event_loop_handlers
from const import GRAY, PURPLE, WHITE, trellis


def clear():
    # Clear pixels and set up toggle button
    trellis.pixels.fill(0)
    # TODO: Make brightness based on sun elevation
    trellis.pixels.brightness = 0.5
    trellis.pixels[0, 0] = PURPLE
    trellis.pixels[3, 0] = PURPLE
    trellis.pixels[0, 7] = WHITE
    trellis.pixels[1, 7] = GRAY
    trellis.pixels.show()


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
