"""Module that contains most stuff used in the main loop."""
# Various imports
import time

import board
import busio

from const import (
    BLUE,
    GRAY,
    PURPLE,
    RED,
    RESEND_CHANGE_DELAY,
    RESEND_STATUS_DELAY,
    WHITE,
    trellis,
)
from images import draw_image

from choosers import choose_brightness, choose_color  # isort:skip
from utilities import draw_status, get_data  # isort:skip

# Set some stuff up
uart = busio.UART(board.SDA, board.SCL, baudrate=115200, timeout=0.01)
current_press = set()
the_payload = ""


def is_pressed():
    """Just returns if any new keys were pressed."""
    pressed = set(trellis.pressed_keys) - current_press
    return len(pressed) > 0


# TODO: Store data on the side of the M4 instead
# Implementation:
# Store payload globally (done already)
# Store list of all entities
# Do the math, and emulate the payload
# Store it and render it
def handle_presses():
    """
    Look at the currently pressed keys.
    If the toggle button is pressed, toggle the entity, and request a report.
    Then store the currently pressed keys,
    so that once a key is pressed, nothing happens until it's released and pressed again.
    """
    global current_press
    did_request_report = False
    # Left/right entity
    pressed = set(trellis.pressed_keys) - current_press
    if len(pressed) > 0:
        if (0, 0) in pressed:
            change_entity(is_previous=True)
            request_report()
            render_screen()
            did_request_report = True
        elif (3, 0) in pressed:
            change_entity(is_previous=False)
            request_report()
            render_screen()
            did_request_report = True
        # TODO: Click on status to re-update
        elif (0, 7) in pressed:
            toggle_entity()
            request_report()
            render_screen()
            did_request_report = True
        elif (1, 7) in pressed:
            brightness_amount = (choose_brightness() + 1) * 12.5
            set_brightness(brightness_amount)
            request_report()
            render_screen()
            did_request_report = True
        elif (2, 7) in pressed:
            hue, sat = choose_color()
            set_color(hue, sat)
            request_report()
            render_screen()
            did_request_report = True
    current_press = set(trellis.pressed_keys)
    return did_request_report


def change_entity(is_previous):
    if is_previous:
        print("Requesting previous entity")
        uart.write(b"p")
    else:
        print("Requesting next entity")
        uart.write(b"n")
    uart.reset_input_buffer()
    trellis.pixels[0 if is_previous else 3, 0] = BLUE
    trellis.pixels.show()
    if is_previous:
        the_payload = get_data(uart, RESEND_CHANGE_DELAY, b"p")
    else:
        the_payload = get_data(uart, RESEND_CHANGE_DELAY, b"n")
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[0 if is_previous else 3, 0] = PURPLE
    trellis.pixels.show()


def toggle_entity():
    """Asks ESP to toggle current entity."""
    print("Toggling entity")
    uart.write(b"t")
    uart.reset_input_buffer()
    trellis.pixels[0, 7] = BLUE
    trellis.pixels.show()
    the_payload = get_data(uart, RESEND_CHANGE_DELAY, b"t")
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[0, 7] = WHITE
    trellis.pixels.show()


def request_report():
    """Asks ESP which entity and its state."""
    print("Requesting report")
    uart.write(b"s")
    uart.reset_input_buffer()
    trellis.pixels[1, 0] = BLUE
    trellis.pixels.show()
    global the_payload
    the_payload = get_data(uart, RESEND_STATUS_DELAY, b"s")
    print("Payload:", the_payload)


def render_screen():
    """
    Renders screen.
    It does this by looking at the last payload sent.
    Then if it's on, it shows that it's on, and vice versa.
    It also renders the entity's icon.
    Then it runs trellis.pixels.show.
    """
    current_status = the_payload.split("|")[0]
    if current_status == "on":
        draw_status(True)
    elif current_status == "off":
        draw_status(False)
    if "|" in the_payload:
        which_entity = the_payload.split("|")[1]
        draw_image(which_entity)
    trellis.pixels.show()


def set_brightness(the_brightness):
    """
    Asks ESP to set brightness.
    Args:
        the_brightness: Brightness to set, 0-100
    """
    print("Setting brightness")
    uart.write(b"b" + str(the_brightness).encode())
    uart.reset_input_buffer()
    trellis.pixels[1, 7] = BLUE
    trellis.pixels.show()
    the_payload = get_data(
        uart, RESEND_STATUS_DELAY, b"b" + str(the_brightness).encode()
    )
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[1, 7] = GRAY
    trellis.pixels.show()


def set_color(the_hue, the_sat):
    """
    Asks ESP to set color.
    Args:
        the_hue: Hue to be passed, 0-360
        the_sat: Saturation to be passed, 0-100
    """
    print("Setting color")
    request_payload = b"c" + str(the_hue).encode() + b"," + str(the_sat).encode()
    uart.write(request_payload)
    uart.reset_input_buffer()
    trellis.pixels[2, 7] = BLUE
    trellis.pixels.show()
    the_payload = get_data(uart, RESEND_STATUS_DELAY, request_payload)
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[2, 7] = RED
    trellis.pixels.show()
