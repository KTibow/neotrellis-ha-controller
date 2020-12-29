from const import BIT_BLUE, BLACK, BROWN, WHITE, YELLOW, trellis


def clear_canvas():
    for x_index in range(4):
        for y_index in range(1, 7):
            trellis.pixels[x_index, y_index] = BLACK


def draw_image(entity_id):
    clear_canvas()
    # TODO: Add more stuff
    if entity_id == "light.outside_lights":
        draw_outside()
    elif entity_id == "light.living_room_lamps":
        draw_living_room()


def draw_outside():
    trellis.pixels[0, 6] = BROWN
    trellis.pixels[0, 5] = BROWN
    trellis.pixels[0, 4] = BROWN
    trellis.pixels[0, 3] = BROWN
    trellis.pixels[0, 2] = BROWN
    trellis.pixels[0, 1] = BROWN
    trellis.pixels[1, 2] = WHITE
    trellis.pixels[2, 2] = WHITE
    trellis.pixels[1, 3] = YELLOW
    trellis.pixels[2, 3] = YELLOW
    trellis.pixels[3, 3] = YELLOW
    trellis.pixels[1, 4] = YELLOW
    trellis.pixels[2, 4] = YELLOW
    trellis.pixels[3, 4] = YELLOW
    trellis.pixels[2, 5] = YELLOW


def draw_living_room():
    trellis.pixels[3, 1] = YELLOW
    trellis.pixels[2, 2] = YELLOW
    trellis.pixels[3, 2] = YELLOW
    trellis.pixels[0, 3] = BIT_BLUE
    trellis.pixels[3, 3] = BIT_BLUE
    trellis.pixels[0, 4] = BIT_BLUE
    trellis.pixels[1, 4] = BIT_BLUE
    trellis.pixels[2, 4] = BIT_BLUE
    trellis.pixels[3, 4] = BIT_BLUE
    trellis.pixels[0, 5] = BIT_BLUE
    trellis.pixels[1, 5] = BIT_BLUE
    trellis.pixels[2, 5] = BIT_BLUE
    trellis.pixels[3, 5] = BIT_BLUE
