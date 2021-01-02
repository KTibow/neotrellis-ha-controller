# neotrellis-ha

Turn an Adafruit Neotrellis M4 and a spare ESP8266/ESP32 into a smart home hub!

## Dependencies

- I use [black](https://black.now.sh) to format my code.
- I use [isort](https://pycqa.github.io/isort/docs/quick_start/0.-try/) to format my code, too.
- I use [Mu](https://codewith.mu/en/download) to write my code.
- I use [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701) for terminal commands (`python3 -m black .`, `git add .`)
- I need some way to talk over WiFi, so I use a [Feather ESP8266](https://www.adafruit.com/product/2821), and I connect it with a [stemma cable](https://www.digikey.com/en/products/detail/adafruit-industries-llc/3950/9745249).
- Needs these circuitpython libs (download from https://circuitpython.org/libraries):

```
adafruit_bus_device
adafruit_fancyled
adafruit_trellism4.mpy
neopixel.mpy
adafruit_matrixkeypad.mpy
adafruit_adxl34x.mpy
```

- And the Neotrellis M4 ([https://www.adafruit.com/product/4020](adafruit) [digikey](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4020/9843404)), of course.

## Pre-commit

Run

```
python3 -m black .; python3 -m isort . --profile black; python3 -m pylint code.py utilities.py const.py event_loop_handlers.py images.py --disable=import-error,no-name-in-module
```
