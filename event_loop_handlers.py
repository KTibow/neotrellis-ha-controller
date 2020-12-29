# Various imports
import time

import board
import busio
from __main__ import trellis

from const import (
    BLUE,
    PURPLE,
    RESEND_CHANGE_DELAY,
    RESEND_STATUS_DELAY,
    UART_READ_LENGTH,
    WHITE,
)
from images import draw_image
from utilities import draw_status, get_payload

# Set some stuff up
uart = busio.UART(board.SDA, board.SCL, baudrate=115200, timeout=0.01)
current_press = set()


def is_pressed():
    pressed = set(trellis.pressed_keys) - current_press
    return len(pressed) > 0


# TODO: Store data on the side of the M4 instead
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
        elif (3, 0) in pressed:
            change_entity(is_previous=False)
            request_report()
        # TODO: Click on status to re-update
        elif (0, 7) in pressed:
            toggle_entity()
            request_report()
            did_request_report = True
    current_press = set(trellis.pressed_keys)
    return did_request_report


# TODO: Move this segment of code into utilities.py
def get_data(resend_timeout, resend_string):
    last_request = time.monotonic()
    data_string = uart.read(UART_READ_LENGTH)
    while data_string is None:
        if time.monotonic() - last_request > resend_timeout:
            print("Re-sending" + resend_string.decode())
            uart.write(resend_string)
            last_request = time.monotonic()
        data_string = uart.read(UART_READ_LENGTH)
    data_string = data_string.decode()
    return get_payload(data_string)


def change_entity(is_previous):
    if is_previous:
        print("Requesting previous entity")
        uart.write(b"prev_entity")
    else:
        print("Requesting next entity")
        uart.write(b"next_entity")
    uart.reset_input_buffer()
    trellis.pixels[0 if is_previous else 3, 0] = BLUE
    trellis.pixels.show()
    if is_previous:
        the_payload = get_data(RESEND_CHANGE_DELAY, b"prev_entity")
    else:
        the_payload = get_data(RESEND_CHANGE_DELAY, b"next_entity")
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[0 if is_previous else 3, 0] = PURPLE
    trellis.pixels.show()


def toggle_entity():
    print("Toggling entity")
    uart.write(b"toggle_entity")
    uart.reset_input_buffer()
    trellis.pixels[0, 7] = BLUE
    trellis.pixels.show()
    the_payload = get_data(RESEND_CHANGE_DELAY, b"toggle_entity")
    print("Payload:", the_payload)
    time.sleep(1.5)
    trellis.pixels[0, 7] = WHITE
    trellis.pixels.show()


def request_report():
    print("Requesting report")
    uart.write(b"send_report")
    uart.reset_input_buffer()
    trellis.pixels[1, 0] = BLUE
    trellis.pixels.show()
    the_payload = get_data(RESEND_STATUS_DELAY, b"send_report")
    print("Payload:", the_payload)
    current_status = the_payload.split("|")[0]
    if current_status == "on":
        draw_status(True)
    elif current_status == "off":
        draw_status(False)
    if "|" in the_payload:
        which_entity = the_payload.split("|")[1]
        draw_image(which_entity)
    trellis.pixels.show()
