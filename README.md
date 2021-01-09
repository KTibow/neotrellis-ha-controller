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

## Get going

1. Get everything in the dependencies section
2. Add `on_the_esp_side/comm.h` to the root of your ESPHome folder and modify the entities
3. Setup your ESP with the file `on_the_esp_side/esp_neotrellis.yaml`
4. Assemble your Neotrellis case
5. Plug in the Stemma cable to your Neotrellis
6. Make these connections:

- Red to 3V on your ESP
- Black to GND on your ESP
- Green to 15 on your ESP
- White to 13 on your ESP

7. Go into your CircuitPython drive
8. Run `git clone [insert this repo's URL] .`
9. It should work. If it doesn't, make an issue.
