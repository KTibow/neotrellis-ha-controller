"""Interactive Home Assistant controller"""
# Various imports
import time

# Get various constants
from const import STATUS_REQUEST_FREQUENCY, init

# Set up trellis
init()
from const import trellis

# Various items
last_entity_update = time.monotonic()

# Get functions for loop
from event_loop_handlers import (
    handle_presses,
    is_pressed,
    render_screen,
    request_report,
)

from choosers import animate, clear  # isort:skip

clear()

# Event loop
while True:
    starting_sleep = time.monotonic()
    while time.monotonic() - starting_sleep < 0.05:
        pass
    # Loop
    trellis.pixels.brightness = 0.2
    if time.monotonic() - last_entity_update > STATUS_REQUEST_FREQUENCY or is_pressed():
        trellis.pixels.show()
    did_update_entity = handle_presses()
    # Report
    # TODO: set last_entity_update on all request_reports, not just this one
    if time.monotonic() - last_entity_update > STATUS_REQUEST_FREQUENCY:
        request_report()
        render_screen()
        did_update_entity = True
    if did_update_entity:
        last_entity_update = time.monotonic()
    trellis.pixels.brightness = 0.5
    trellis.pixels.show()
    animate()
