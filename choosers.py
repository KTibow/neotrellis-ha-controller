from const import PURPLE, WHITE, GRAY, trellis


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


def choose_brightness():
    while len(trellis.pressed_keys) != 0:
        pass
    for x_index in range(4):
        for y_index in range(8):
            brightness = (y_index + 1) * 31
            trellis.pixels[x_index, y_index] = (brightness,) * 3
    while len(trellis.pressed_keys) == 0:
        trellis.pixels.show()
    clear()
    print(trellis.pressed_keys[0][1])
    return trellis.pressed_keys[0]
