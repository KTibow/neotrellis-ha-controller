"""
Various constants, including how often to do stuff,
colors, and other things.
"""

import adafruit_trellism4

# UART
UART_READ_LENGTH = 35
# Frequencies (in seconds)
RESEND_CHANGE_DELAY = 5
RESEND_STATUS_DELAY = 3
STATUS_REQUEST_FREQUENCY = 12
# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BIT_BLUE = (25, 25, 230)
PURPLE = (64, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)
BROWN = (35, 22, 0)
# Entities
ALL_ENTITIES = []
# Inited stuff
def init():
    global trellis
    trellis = adafruit_trellism4.TrellisM4Express(rotation=270)
    trellis.pixels.auto_write = False
