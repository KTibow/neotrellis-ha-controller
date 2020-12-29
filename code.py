"""Interactive Home Assistant hub"""
# Various imports
import time

# Get various constants
from const import PURPLE, STATUS_REQUEST_FREQUENCY, WHITE, init

# Set up trellis
init()
from const import trellis

# Various items
last_entity_update = time.monotonic()

# Get functions for loop
from event_loop_handlers import handle_presses, is_pressed, request_report

# Clear pixels and set up toggle button
trellis.pixels.fill(0)
# TODO: Make brightness based on sun elevation
trellis.pixels.brightness = 0.5
trellis.pixels[0, 0] = PURPLE
trellis.pixels[3, 0] = PURPLE
trellis.pixels[0, 7] = WHITE
trellis.pixels.show()

# Event loop
while True:
    time.sleep(0.05)
    # Loop
    trellis.pixels.brightness = 0.2
    if time.monotonic() - last_entity_update > STATUS_REQUEST_FREQUENCY or is_pressed():
        trellis.pixels.show()
    did_update_entity = handle_presses()
    # Report
    # TODO: set last_entity_update on all request_reports, not just this one
    if time.monotonic() - last_entity_update > STATUS_REQUEST_FREQUENCY:
        request_report()
        did_update_entity = True
    if did_update_entity:
        last_entity_update = time.monotonic()
    trellis.pixels.brightness = 0.5
    trellis.pixels.show()
